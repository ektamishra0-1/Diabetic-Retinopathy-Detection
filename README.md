# 🩺 Diabetic Retinopathy Detection using Deep Learning

> An AI-powered web application that detects Diabetic Retinopathy from retinal fundus images using a deep learning model, enabling quick and accessible screening for early diagnosis.

<p align="center">
<img src="images/homepage.png" width="800">
</p>

---

# 📌 Overview

Diabetic Retinopathy (DR) is one of the leading causes of preventable blindness among diabetic patients.

Early diagnosis plays a crucial role in preventing permanent vision loss. However, retinal screening often requires trained ophthalmologists and specialized medical equipment.

This project leverages Deep Learning and Computer Vision to automatically analyze retinal fundus images and classify whether signs of diabetic retinopathy are present.

The system allows users to upload a retinal image through a simple web interface and receive an AI-generated prediction within seconds.

---

# 🚀 Features

✅ Upload retinal fundus images

✅ AI-based Diabetic Retinopathy prediction

✅ User-friendly web interface

✅ Fast inference

✅ End-to-end Deep Learning pipeline

✅ Responsive frontend

---

# 📸 Screenshots

## Home Page

![Home](screenshots/home.png)

---

## Upload Image

![Upload](screenshots/upload.png)

---

## Prediction Result

![Prediction](screenshots/result.png)

---

# 🧠 Tech Stack

## Machine Learning

- Python
- TensorFlow / Keras
- NumPy
- OpenCV
- Pillow
- Scikit-learn

## Web Development

- Flask
- HTML5
- CSS3
- JavaScript

## Data Visualization

- Matplotlib
- Seaborn

## Development Tools

- VS Code
- Git
- GitHub
- Jupyter Notebook

---

# 🏗️ System Architecture

```
Retinal Image
       │
       ▼
Image Preprocessing
       │
       ▼
Deep Learning Model
       │
       ▼
Prediction
       │
       ▼
Display Result on Web App
```

---

# 📂 Project Structure

```
Diabetic-Retinopathy-Detection/

│
├── model/
│
├── static/
│
├── templates/
│
├── uploads/
│
├── app.py
│
├── requirements.txt
│
├── train_model.ipynb
│
├── README.md
│
└── ...
```

---

# 📊 Dataset

The model was trained using retinal fundus images for Diabetic Retinopathy detection.

Dataset contains labeled retinal images representing different stages of diabetic retinopathy.

Typical classes include:

- No DR
- Mild
- Moderate
- Severe
- Proliferative DR

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/ektamishra0-1/Diabetic-Retinopathy-Detection.git
```

Move inside project

```bash
cd Diabetic-Retinopathy-Detection
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run the Project

```bash
python app.py
```

Open browser

```
http://127.0.0.1:5000
```

---

# 🔍 Model Pipeline

1. Image Upload
2. Image Preprocessing
3. Image Resizing
4. Normalization
5. Deep Learning Prediction
6. Classification
7. Display Result

---

# 📈 Results

The model successfully identifies diabetic retinopathy from retinal fundus images and provides rapid predictions through an intuitive web interface.

This project demonstrates the practical application of Deep Learning in medical image analysis and AI-assisted healthcare.

---

# 💡 Future Improvements

- Multi-class DR severity prediction
- Confidence score visualization
- Explainable AI using Grad-CAM
- Mobile application
- Cloud deployment
- Doctor dashboard
- Patient history management

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository

2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👩‍💻 Author

**Ekta Mishra**

AI • Machine Learning • Data Science • Healthcare AI

GitHub:
https://github.com/ektamishra0-1

LinkedIn:
(Add your LinkedIn)

---

⭐ If you found this project useful, consider giving it a Star!
