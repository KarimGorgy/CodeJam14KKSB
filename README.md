# CodeJam14KKSB

# How to Run the Application

This application consists of a Flask backend and a React frontend. Follow these steps to run both parts of the application and use ngrok to expose your local backend for DialogFlow:

## 1. **Run the Flask Backend**
The Flask backend is implemented in the `App2.py` file. To start the backend:

1. Open a terminal and navigate to the directory containing `App2.py`.
2. *(Optional)* Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Flask backend:
   ```bash
   python App2.py
   ```
5. The backend should now be running on `http://127.0.0.1:5000` (or as defined in your Flask configuration).

---

## 2. **Expose Flask Backend to DialogFlow**
DialogFlow requires a public URL to communicate with the backend. Use ngrok to expose your Flask backend:

1. Download and install ngrok from [ngrok's website](https://ngrok.com/download).
2. Start ngrok and point it to your Flask server:
   ```bash
   ngrok http 5000
   ```
3. Copy the public URL provided by ngrok (e.g., `https://your-ngrok-url.ngrok.io`).
4. Update your DialogFlow webhook settings to use the ngrok public URL.

---

## 3. **Run the React Frontend**
The React frontend is located in the `frontend` folder. To start the frontend:

1. Open a new terminal and navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install the required dependencies:
   ```bash
   npm install
   ```
3. Start the React development server:
   ```bash
   npm run dev
   ```
4. The frontend should now be running on `http://localhost:5173` (or another port if configured).

---

## 4. **Access the Application**
1. Open your browser and navigate to `http://localhost:5173` to use the frontend interface.
2. Ensure that the Flask backend and ngrok are running, as the frontend communicates with the backend.

---

## 5. **Development Notes**
- **Backend**: Ensure that your Flask backend is configured to handle requests from the ngrok public URL.
- **Frontend**: Make sure the API calls in the React project use the correct backend URL (either local or the ngrok URL).
- **DialogFlow**: Update the webhook settings in DialogFlow to match the current ngrok URL each time ngrok restarts.

---

## 6. **Common Commands**
Here are the key commands you’ll use frequently:

- **Start Flask Backend**:
  ```bash
  python App2.py
  ```
- **Expose Backend via ngrok**:
  ```bash
  ngrok http 5000
  ```
- **Start React Frontend**:
  ```bash
  cd frontend
  npm run dev
  
