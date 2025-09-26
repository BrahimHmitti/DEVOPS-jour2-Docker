from flask import Flask, request, jsonify, render_template_string
import redis
import os
from datetime import datetime

app = Flask(__name__)

# Configuration Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

# Template HTML intégré
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flask Guestbook</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #e8f4fd; padding: 20px; border-radius: 10px; }
        input, button { padding: 10px; margin: 5px; font-size: 16px; }
        .message { background: white; padding: 10px; margin: 5px 0; border-radius: 5px; }
        .status { color: green; font-weight: bold; }
        .python-badge { background: #3776ab; color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐍 Flask Guestbook MODIFIÉ AVEC HOT RELOAD ! <span class="python-badge">Python + Hot Reload</span></h1>
        <div>
            <input type="text" id="messageInput" placeholder="Votre message..." />
            <button onclick="addMessage()">Ajouter</button>
        </div>
        <div id="status"></div>
        <div id="messages"></div>
    </div>

    <script>
        async function loadMessages() {
            try {
                const response = await fetch('/api/messages');
                const messages = await response.json();
                const container = document.getElementById('messages');
                container.innerHTML = messages.map(msg => `<div class="message">${msg}</div>`).join('');
            } catch (error) {
                document.getElementById('status').innerText = 'Erreur lors du chargement des messages';
            }
        }

        async function addMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;

            try {
                const response = await fetch('/api/messages', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });

                if (response.ok) {
                    input.value = '';
                    document.getElementById('status').innerText = '✅ Message ajouté !';
                    setTimeout(() => document.getElementById('status').innerText = '', 2000);
                    loadMessages();
                }
            } catch (error) {
                document.getElementById('status').innerText = '❌ Erreur lors de l\\'ajout';
            }
        }

        loadMessages();
        setInterval(loadMessages, 5000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        messages = r.lrange('flask_messages', 0, -1)
        return jsonify(list(reversed(messages)))
    except Exception as e:
        print(f"Error getting messages: {e}")
        return jsonify([])

@app.route('/api/messages', methods=['POST'])
def add_message():
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        full_message = f"{timestamp}: {message}"
        
        r.lpush('flask_messages', full_message)
        return jsonify({'success': True, 'message': full_message})
        
    except Exception as e:
        print(f"Error adding message: {e}")
        return jsonify({'error': 'Failed to add message'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3002))
    print(f"🚀 Flask server starting on port {port}")
    print(f"🔥 Hot reloading enabled with Flask debug mode")
    app.run(host='0.0.0.0', port=port, debug=True)
