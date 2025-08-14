# spaCy NLU Server – Documentation

## Overview

This project is a Natural Language Understanding (NLU) server built with Python, Flask, and spaCy. It provides a REST API for user registration, authentication, and protected NLP parsing endpoints. The NLU model is trained using custom data and can extract entities and detect user intent for educational/administrative queries.

---

## Table of Contents

1.  [Requirements](#requirements)
2.  [Installation](#installation)
3.  [Project Structure](#project-structure)
4.  [Configuration](#configuration)
5.  [Training the spaCy Model](#training-the-spacy-model)
6.  [Running the Server](#running-the-server)
7.  [API Endpoints](#api-endpoints)
8.  [Operating the System](#operating-the-system)
9.  [Troubleshooting](#troubleshooting)
10. [Notes](#notes)

---

## 1. Requirements

-   Python 3.10+
-   pip (Python package manager)
-   (Optional) Node.js (if you plan to use any JS dependencies)
-   Windows 10+ (as per your environment)
-   Recommended: Use a virtual environment

---

## 2. Installation

1.  **Clone or Download the Project**

    Place the project folder (`spacy_nlu_server`) on your machine.

2.  **Set up a Python Virtual Environment**

    ```sh
    python -m venv venv
    ```

3.  **Activate the Virtual Environment**

    -   On Windows:
        ```sh
        venv\Scripts\activate
        ```

4.  **Install Python Dependencies**

    ```sh
    pip install -U pip
    pip install flask flask-cors flask-jwt-extended flask-sqlalchemy spacy
    ```

    -   If you need to install additional dependencies, check `package.json` and install with:
        ```sh
        pip install -r requirements.txt
        ```
        *(You may need to create `requirements.txt` if not present.)*

5.  **(Optional) Install Node.js Dependencies**

    If you plan to use any JS tools/scripts:
    ```sh
    npm install
    ```

---

## 3. Project Structure
spacy_nlu_server/
│
├── app.py               # Main Flask server
├── train.py             # Script to train the spaCy model
├── generate_data.py     # Script to generate training data with indices
├── training_data.py     # Python file with training data
├── training_data.spacy  # Binary training data for spaCy
├── config.cfg           # spaCy model configuration
├── output_model_*/      # Trained model output directories
│   └── model-best/      # Best model for inference
├── instance/
│   ├── app_data.db      # App database (if used)
│   └── users.db         # User authentication database
├── venv/                # Python virtual environment
├── package.json         # Node.js dependencies (if any)
├── package-lock.json
└── node_modules/        # Node.js modules (if any)

---

## 4. Configuration

-   **spaCy Model Config:** `config.cfg`
-   **Flask App Config:** Set in `app.py` (e.g., JWT secret, DB URI)
-   **Databases:** SQLite files in `instance/` directory

You can set environment variables for sensitive data (e.g., `JWT_SECRET_KEY`).

---

## 5. Training the spaCy Model

### a. Prepare Training Data

-   Edit `generate_data.py` and `training_data.py` to add or modify training examples.
-   To generate `training_data.py` with correct character indices, run:
    ```sh
    python generate_data.py
    ```

### b. Train the Model

-   Run the training script:
    ```sh
    python train.py
    ```
-   This will:
    -   Validate your training data
    -   Convert it to spaCy's binary format (`training_data.spacy`)
    -   Train a new model and save it in a timestamped `output_model_*` directory

---

## 6. Running the Server

1.  **Ensure the Model is Trained**

    -   The server loads the latest model from the `output_model_*` directory.
    -   If no model is found, it will run with limited NLP features.

2.  **Start the Flask Server**

    ```sh
    python app.py
    ```

    -   The server will run on `http://localhost:5005` by default.

---

## 7. API Endpoints

### 1. **User Registration**

-   **POST** `/api/register`
-   **Body:** `{ "username": "yourname", "password": "yourpassword" }`
-   **Response:** Success or error message

### 2. **User Login**

-   **POST** `/api/login`
-   **Body:** `{ "username": "yourname", "password": "yourpassword" }`
-   **Response:** `{ "access_token": "..." }`

### 3. **Parse Message (Protected)**

-   **POST** `/api/parse`
-   **Headers:** `Authorization: Bearer <access_token>`
-   **Body:** `{ "text": "your query here" }`
-   **Response:** `{ "action": "...", "parameters": {...} }`

---

## 8. Operating the System

### **User Flow**

1.  **Register a new user** via `/api/register`.
2.  **Login** to get a JWT token via `/api/login`.
3.  **Use the token** to access `/api/parse` for NLP parsing.

### **Model Update**

-   Add or modify training data in `generate_data.py`/`training_data.py`.
-   Regenerate and retrain the model as described above.
-   Restart the server to load the new model.

### **Database**

-   User data is stored in `instance/users.db` (SQLite).
-   The database is auto-created on first run.

---

## 9. Troubleshooting

-   **Model not found:** Ensure you have trained the model at least once.
-   **Dependency errors:** Double-check your Python environment and installed packages.
-   **Port conflicts:** Change the port in `app.py` if `5005` is in use.
-   **JWT errors:** Ensure you use the correct token and secret key.

---

## 10. Notes

-   The server is set to `debug=True` for development. For production, set `debug=False` and use a production WSGI server.
-   You can expand the training data and intent/entity logic for more advanced NLU.
-   The project is modular: you can add more endpoints, models, or database features as needed.

---

**For further customization or deployment, consult the Flask and spaCy documentation.**
