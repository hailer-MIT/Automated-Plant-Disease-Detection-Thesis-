# 🌿 Automated Plant Disease Detection Using CNN

## 🧠 Problem Statement

Manual identification of plant diseases is time-consuming, error-prone, and inaccessible to small-scale farmers. Early detection is crucial for minimizing crop loss, yet many lack the tools for efficient disease diagnosis.

## ✅ Solution

This project implements a **Convolutional Neural Network (CNN)** to automate the detection of plant diseases from leaf images. Built as part of a thesis project, it aims to support sustainable agriculture through accessible AI-driven diagnosis.

## 🔧 Approach

We trained a CNN model using a Kaggle-hosted dataset of healthy and diseased plant leaf images. The model was optimized for high accuracy using image augmentation and dropout layers to prevent overfitting. A backend (Django REST API) and a Flutter-based mobile interface were developed to make the system accessible to end-users, including farmers.

The approach includes:
- Image preprocessing & augmentation
- CNN architecture with 4 convolutional layers
- TensorFlow/Keras model training
- Integration with mobile frontend using Flutter
- Backend API built using Django for model inference

## 🧪 Results

- **Training Accuracy:** ~98%
- **Validation Accuracy:** ~95%
- Successfully deployed in a mobile interface for testing.
- Selected for presentation at a Science and Technology international conference.

## ⚙️ Tools & Libraries Used

- TensorFlow, Keras
- OpenCV
- Kaggle Datasets
- Flutter (Frontend)
- Django (Backend)
- Python

## 📁 Dataset

- **Source:** [Cactus Dataset on my Kaggle account](https://www.kaggle.com/datasets/hailom/cactus)
- Not included in this repo due to size. Please download it from Kaggle and place it in the `data/` folder.

## ▶️ How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/hailer-MIT/Automated-Plant-Disease-Detection-Thesis-.git
cd Automated-Plant-Disease-Detection-Thesis-

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# 3. Install required packages
pip install -r requirements.txt

# 4. Open the notebook
jupyter notebook Automated-Plant-Disease-Detection-Thesis.ipynb
