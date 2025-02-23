

License Plate Recognition System 🚗🔍

📌 Overview
This project implements a **License Plate Recognition System** using **OpenCV**, **Tesseract OCR**, and **Flask**. The system detects a vehicle's license plate from an image and extracts the characters using Optical Character Recognition (OCR).
 🏗 Features
- 📸 **Image Upload & Processing**: Users can upload an image containing a vehicle's license plate.
- 🏷 **License Plate Detection**: OpenCV is used to detect the license plate in the image.
- 🔠 **Character Recognition**: Tesseract OCR extracts alphanumeric characters from the detected plate.
- 🌐 **Web Interface**: A simple and user-friendly Flask-based web application.
- 📊 **Results Display**: Displays the detected license plate and recognized text.

⚙️ System Requirements

 🖥 Hardware Requirements
- A computer with at least **4GB RAM**.
- A **webcam** or **image file input** for testing.
- Sufficient storage space for libraries and models.

 🖥 Software Requirements
- **Python 3.6+**
- **OpenCV** (`cv2`)
- **Tesseract OCR**
- **Flask** (for web interface)
- **NumPy**
- **pytesseract**

🚀 Installation & Setup

📥 Clone Repository
git clone https://github.com/yourusername/license-plate-recognition.git
cd license-plate-recognition


📦 Install Dependencies
Make sure you have Python installed, then install the required libraries:

pip install -r requirements.txt


🔧 Configure Tesseract OCR
1. **Windows Users**: Download and install **Tesseract OCR** from [here](https://github.com/UB-Mannheim/tesseract/wiki).
2. Add the Tesseract installation path to your system environment variables:
      setx TESSDATA_PREFIX "C:\Program Files\Tesseract-OCR\tessdata"
   
3. Verify installation:
   
   tesseract -v
   

 Run the Application
The application will be available at **http://127.0.0.1:5000/**.

## 📸 Sample Output
| Input Image  | License Plate Detection | Recognized Text |
|-------------|------------------------|----------------|
| ![Input](sample_input.jpg) | ![Detected](sample_detected.jpg) | `KA-19-MF-1234` |

## 🏗 Project Structure
```
license-plate-recognition/
│── static/
│   ├── styles.css           # CSS for UI styling
│   ├── images/              # Sample images
│── templates/
│   ├── index.html           # Web interface
│── app.py                   # Main Flask application
│── detect_plate.py          # License plate detection and OCR
│── requirements.txt         # List of required Python libraries
│── README.md                # Project documentation
```

## 🛠 Future Enhancements
- 🎥 **Real-time Video Stream Support**
- 🤖 **Deep Learning-Based OCR for Improved Accuracy**
- 🔒 **Database Integration for License Plate Storage**

## 📜 License
This project is **open-source** under the **MIT License**.


💡 *Contributions are welcome! Feel free to fork this repository and improve the project.* 🚀


How to Add to GitHub?
1. Create a `README.md` file in your project directory.
2. Copy and paste the above content into the file.
3. Add, commit, and push it to your GitHub repository:
   ```sh
   git add README.md
   git commit -m "Added README file"
   git push origin main
   ```

