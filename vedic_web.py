#!/usr/bin/env python3
import http.server
import socketserver
import subprocess
import urllib.parse
import json

PORT = 8080

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Vedic AI</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: #ffd700;
            font-family: Arial, sans-serif;
            padding: 20px;
            text-align: center;
        }
        .container { max-width: 600px; margin: 0 auto; }
        textarea {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            border-radius: 10px;
            background: #2d2d44;
            color: white;
            border: none;
        }
        button {
            background: #ffd700;
            color: #1a1a2e;
            padding: 12px 30px;
            border: none;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
        }
        .answer {
            background: #2d2d44;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            text-align: left;
            color: #eee;
        }
        .om { font-size: 48px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="om">🕉️</div>
        <h1>Vedic AI</h1>
        <p>74 Algorithms | 100% Offline</p>
        <textarea id="question" rows="3" placeholder="Ask anything..."></textarea>
        <button onclick="ask()">Ask</button>
        <div id="answer" class="answer" style="display:none"></div>
    </div>
    <script>
        async function ask() {
            const q = document.getElementById('question').value;
            if (!q) return;
            const btn = event.target;
            btn.disabled = true;
            btn.textContent = 'Thinking...';
            document.getElementById('answer').style.display = 'none';
            
            const resp = await fetch('/ask?q=' + encodeURIComponent(q));
            const data = await resp.json();
            
            document.getElementById('answer').innerHTML = '<strong>Answer:</strong><br>' + data.answer;
            document.getElementById('answer').style.display = 'block';
            btn.disabled = false;
            btn.textContent = 'Ask';
        }
    </script>
</body>
</html>
'''

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML.encode())
        elif self.path.startswith('/ask'):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query).get('q', [''])[0]
            result = subprocess.run(f'~/vai "{query}"', shell=True, capture_output=True, text=True)
            answer = result.stdout.strip()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'answer': answer}).encode())
    
    def log_message(self, format, *args):
        pass

print("Vedic AI Web Server starting...")
print("Open http://localhost:8080 in your browser")
socketserver.TCPServer(('0.0.0.0', PORT), Handler).serve_forever()
