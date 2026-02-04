import os
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
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
                margin: 0;
            }
            .container {
                text-align: center;
                background: white;
                padding: 50px;
                border-radius: 25px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 800px;
                margin: 20px;
            }
            h1 {
                background: linear-gradient(90deg, #FF512F, #DD2476);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 3.5rem;
                margin-bottom: 10px;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 40px 0;
            }
            .feature-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 15px;
                text-align: center;
                transition: transform 0.3s;
            }
            .feature-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            .feature-icon {
                font-size: 2.5rem;
                margin-bottom: 15px;
            }
            .btn {
                display: inline-block;
                background: linear-gradient(90deg, #FF512F, #DD2476);
                color: white;
                padding: 15px 30px;
                border-radius: 50px;
                text-decoration: none;
                font-weight: bold;
                margin: 20px 10px;
                border: none;
                cursor: pointer;
                font-size: 1.1rem;
                transition: transform 0.3s;
            }
            .btn:hover {
                transform: scale(1.05);
            }
            .demo-link {
                color: #667eea;
                text-decoration: none;
                font-weight: bold;
            }
            .demo-link:hover {
                text-decoration: underline;
            }
        </style>
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    </head>
    <body>
        <div class="container">
            <h1>📱 SmartScan EduPad Pro</h1>
            <p style="color: #666; font-size: 1.2rem; margin-bottom: 30px;">
                AI-Powered E-Assessment System | B.Tech Final Year Project 2024-2025
            </p>
            
            <div class="features">
                <div class="feature-card">
                    <div class="feature-icon">📷</div>
                    <h3>AI-Powered Scanning</h3>
                    <p>Advanced image recognition</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <h3>Instant Evaluation</h3>
                    <p>Real-time results in seconds</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">📊</div>
                    <h3>Smart Analytics</h3>
                    <p>Interactive dashboards</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">☁️</div>
                    <h3>Cloud Native</h3>
                    <p>Auto-scaling infrastructure</p>
                </div>
            </div>
            
            <div style="margin: 40px 0;">
                <h2>🚀 Live Demo Options</h2>
                <p style="color: #666; margin-bottom: 20px;">
                    Choose your preferred demo method:
                </p>
                
                <div>
                    <a href="https://smartscan-edupad.streamlit.app" class="btn" target="_blank">
                        🌐 View Streamlit Demo
                    </a>
                    <button class="btn" onclick="showLocalDemo()">
                        🖥️ Run Local Simulation
                    </button>
                </div>
                
                <div id="localDemo" style="display: none; margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 15px;">
                    <h3>🖥️ Local Simulation Demo</h3>
                    <p>This simulates the SmartScan EduPad interface:</p>
                    <div id="simulationResult"></div>
                    <button class="btn" onclick="runSimulation()" style="background: #4CAF50;">
                        ▶️ Start Simulation
                    </button>
                </div>
            </div>
            
            <div style="background: linear-gradient(90deg, #1a237e, #0d47a1); color: white; padding: 30px; border-radius: 20px; margin-top: 40px;">
                <h3 style="color: white; margin-bottom: 20px;">🎓 B.Tech Final Year Project</h3>
                <p>Department of Computer Science & Engineering</p>
                <p>MLR Institute of Technology | Batch 04</p>
                <p>Guide: Dr. K. Jaya Sri</p>
            </div>
        </div>
        
        <script>
            function showLocalDemo() {
                document.getElementById('localDemo').style.display = 'block';
            }
            
            function runSimulation() {
                const steps = [
                    "📄 Loading answer sheet...",
                    "📷 Capturing image...",
                    "⚡ Processing image...",
                    "🔍 Extracting answers...",
                    "✅ Evaluation complete!"
                ];
                
                const resultDiv = document.getElementById('simulationResult');
                resultDiv.innerHTML = '';
                
                let i = 0;
                function nextStep() {
                    if (i < steps.length) {
                        resultDiv.innerHTML += `<div style="padding: 10px; margin: 5px; background: #e3f2fd; border-radius: 5px; animation: fadeIn 0.5s;">
                            ${steps[i]}
                        </div>`;
                        i++;
                        setTimeout(nextStep, 1000);
                    } else {
                        resultDiv.innerHTML += `<div style="padding: 15px; margin: 10px; background: #4CAF50; color: white; border-radius: 5px; font-weight: bold;">
                            🎉 Simulation Complete! Processed 25 sheets in 45 seconds.
                        </div>`;
                    }
                }
                
                nextStep();
            }
        </script>
        
        <style>
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    </body>
    </html>
    """)

@app.route('/api/status')
def status():
    return {"status": "running", "service": "SmartScan EduPad", "version": "1.0.0"}

@app.route('/health')
def health():
    return {"health": "ok"}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
