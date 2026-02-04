import os
import sys
import subprocess
from flask import Flask, request, send_file, jsonify, Response
import threading
import time

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# Store the Streamlit process
streamlit_process = None

def run_streamlit():
    """Run Streamlit in background"""
    global streamlit_process
    
    # Start Streamlit on port 8501
    cmd = [
        sys.executable, "-m", "streamlit", "run", 
        "app.py", 
        "--server.port=8501",
        "--server.headless=true",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false",
        "--browser.serverAddress=0.0.0.0",
        "--browser.gatherUsageStats=false"
    ]
    
    streamlit_process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for Streamlit to start
    time.sleep(5)
    print("Streamlit started on port 8501")

# Start Streamlit when app starts
threading.Thread(target=run_streamlit, daemon=True).start()

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SmartScan EduPad Pro</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: 'Poppins', sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                color: white;
            }
            .container {
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 10px;
            }
            .btn {
                display: inline-block;
                background: linear-gradient(90deg, #FF512F, #DD2476);
                color: white;
                padding: 15px 30px;
                border-radius: 50px;
                text-decoration: none;
                font-weight: bold;
                margin-top: 20px;
                transition: transform 0.3s;
            }
            .btn:hover {
                transform: scale(1.05);
            }
            .loader {
                border: 5px solid #f3f3f3;
                border-top: 5px solid #FF512F;
                border-radius: 50%;
                width: 50px;
                height: 50px;
                animation: spin 1s linear infinite;
                margin: 20px auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    </head>
    <body>
        <div class="container">
            <h1>📱 SmartScan EduPad Pro</h1>
            <p>AI-Powered E-Assessment System</p>
            <div class="loader"></div>
            <p>Loading your application...</p>
            <a href="/app" class="btn">🚀 Launch Application</a>
            <p style="margin-top: 20px; font-size: 0.9rem; opacity: 0.8;">
                B.Tech Final Year Project 2024-2025
            </p>
        </div>
        <script>
            // Auto-redirect after 3 seconds
            setTimeout(() => {
                window.location.href = "/app";
            }, 3000);
        </script>
    </body>
    </html>
    """

@app.route('/app')
def streamlit_proxy():
    """Proxy to Streamlit"""
    import requests
    try:
        response = requests.get('http://localhost:8501', timeout=10)
        return Response(response.content, mimetype='text/html')
    except:
        return """
        <html>
        <body style="background: #667eea; color: white; font-family: sans-serif; padding: 40px;">
            <h1>Application Starting...</h1>
            <p>Please wait a moment and refresh the page.</p>
            <p>If this persists, check the deployment logs.</p>
        </body>
        </html>
        """

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "SmartScan EduPad"})

@app.route('/api/status')
def status():
    """API status endpoint"""
    return jsonify({
        "app": "running",
        "version": "1.0.0",
        "timestamp": time.time(),
        "endpoints": ["/", "/app", "/health", "/api/status"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)