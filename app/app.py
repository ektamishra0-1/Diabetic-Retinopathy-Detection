from flask import Flask, request, jsonify, render_template
import tensorflow as tf
import numpy as np
import cv2
import os
import base64
import sqlite3

from database import db
from models import Patient

app = Flask(__name__, template_folder='templates')

# ================= CONFIG ================= #
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def _ensure_sqlite_columns(db_file_path: str):
    # Lightweight auto-migration for SQLite (adds columns if missing).
    if not os.path.exists(db_file_path):
        return
    conn = sqlite3.connect(db_file_path)
    try:
        cur = conn.cursor()
        cur.execute("PRAGMA table_info(patient);")
        existing = {row[1] for row in cur.fetchall()}

        def add_col(name: str, sql_type: str):
            if name not in existing:
                cur.execute(f"ALTER TABLE patient ADD COLUMN {name} {sql_type};")

        add_col("pregnancy", "VARCHAR(30)")
        add_col("smoking", "VARCHAR(30)")
        add_col("hba1c", "VARCHAR(50)")
        add_col("bp", "VARCHAR(50)")
        add_col("cholesterol", "VARCHAR(50)")
        add_col("duration", "VARCHAR(50)")
        conn.commit()
    finally:
        conn.close()

with app.app_context():
    db.create_all()
    # Flask-SQLAlchemy places relative SQLite DBs under app.instance_path
    _ensure_sqlite_columns(os.path.join(app.instance_path, "patients.db"))

# ================= TEMP STORAGE ================= #
last_image_path = None
last_prediction = None
last_confidence = None
last_heatmap = None

# ================= LOAD MODEL ================= #
MODEL_PATH = "/Users/ektamishra/Desktop/dti_project_final copy/model/elite_retina_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# ================= CLASS LABELS ================= #
CLASS_NAMES = [
    "No DR",
    "Mild",
    "Moderate",
    "Severe",
    "Proliferative DR"
]

# ================= PREPROCESS ================= #
def preprocess_image(image_path):
    img = cv2.imread(image_path)

    if img is None:
        raise ValueError("Image not loaded properly.")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (224, 224))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)

    return img

# ================= PREDICTION ================= #
def predict_image(image_path):
    img = preprocess_image(image_path)
    preds = model.predict(img)

    class_index = int(np.argmax(preds))
    confidence = float(np.max(preds))

    return {
        "class": CLASS_NAMES[class_index],
        "confidence": confidence
    }

# ================= GRAD-CAM ================= #
def get_last_conv_layer_name(model):
    for layer in reversed(model.layers):
        if "conv" in layer.name:
            return layer.name
    raise ValueError("No Conv layer found in model")


def get_gradcam_heatmap(img_array, model, last_conv_layer_name):
    grad_model = tf.keras.models.Model(
        [model.inputs],
        [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img_array)
        pred_index = tf.argmax(predictions[0])
        loss = predictions[:, pred_index]

    grads = tape.gradient(loss, conv_outputs)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    conv_outputs = conv_outputs[0]
    heatmap = conv_outputs @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)

    return heatmap.numpy()


def overlay_heatmap(image_path, heatmap, alpha=0.4):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (224, 224))

    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(img, 1 - alpha, heatmap, alpha, 0)

    return overlay


def image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

# ================= ROUTES ================= #

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/patient')
def patient():
    global last_image_path
    return render_template('patient.html', image_path=last_image_path)


@app.route('/dashboard')
def dashboard():
    patient = Patient.query.order_by(Patient.timestamp.desc()).first()
    return render_template('dashboard.html', patient=patient)


@app.route('/report')
def report():
    patient = Patient.query.order_by(Patient.timestamp.desc()).first()
    return render_template('report.html', patient=patient)

# ================= PREDICT ================= #

@app.route('/predict', methods=['POST'])
def predict_route():

    global last_image_path, last_prediction, last_confidence, last_heatmap

    if 'image' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['image']

    upload_folder = os.path.join("static", "uploads")
    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(upload_folder, file.filename)
    file.save(filepath)

    # Prediction
    result = predict_image(filepath)

    # Grad-CAM
    img = preprocess_image(filepath)
    last_conv_layer_name = get_last_conv_layer_name(model)

    heatmap = get_gradcam_heatmap(img, model, last_conv_layer_name)
    overlay = overlay_heatmap(filepath, heatmap)

    heatmap_base64 = image_to_base64(overlay)

    # ✅ STORE DATA (CRITICAL FIX)
    last_image_path = filepath
    last_prediction = result["class"]
    last_confidence = result["confidence"]
    last_heatmap = heatmap_base64

    return jsonify({
        "prediction": last_prediction,
        "confidence": last_confidence,
        "heatmap": last_heatmap,
        "image_path": last_image_path
    })

# ================= SAVE PATIENT ================= #

@app.route('/save_patient', methods=['POST'])
def save_patient():

    global last_image_path, last_prediction, last_confidence, last_heatmap

    data = request.get_json()

    new_patient = Patient(
        name=data.get("name"),
        age=data.get("age"),
        gender=data.get("gender"),
        pregnancy=data.get("pregnancy"),
        smoking=data.get("smoking"),
        hba1c=data.get("hba1c"),
        bp=data.get("bp"),
        cholesterol=data.get("cholesterol"),
        duration=data.get("duration"),

        image_path=last_image_path,
        prediction=last_prediction,
        confidence=last_confidence,
        heatmap=last_heatmap
    )

    db.session.add(new_patient)
    db.session.commit()

    return jsonify({"status": "saved"})

# ================= RUN ================= #

if __name__ == '__main__':
    port = int(os.environ.get("PORT", "5001"))
    app.run(debug=True, port=port)