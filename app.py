from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_khairakan_key_2026_v3'

# Интерфейс с мягким шрифтом Nunito и кастомной подписью
TG_STYLE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Khairakan Core</title>
    <!-- Подключаем мягкий округлый шрифт Nunito -->
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Nunito:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Nunito', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        body {
            background-color: #f4f4f5;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #222222;
        }
        .login-card {
            background: #ffffff;
            width: 100%;
            max-width: 380px;
            padding: 40px 25px 30px;
            border-radius: 20px; /* Более мягкие закруглённые углы */
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.04);
            text-align: center;
        }
        .tg-badge {
            width: 72px;
            height: 72px;
            background: #24A1DE;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0 auto 20px;
            color: white;
            font-size: 26px;
            font-weight: 700;
        }
        h1 {
            font-size: 22px;
            color: #212121;
            margin-bottom: 8px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        p {
            font-size: 15px;
            color: #707579;
            margin-bottom: 28px;
            line-height: 1.4;
            font-weight: 500;
        }
        input[type="text"] {
            width: 100%;
            padding: 14px 18px;
            border: 1px solid #dae1e8;
            border-radius: 12px; /* Мягкое закругление */
            font-size: 16px;
            outline: none;
            background: #ffffff;
            transition: border-color 0.15s ease;
            font-weight: 500;
        }
        input[type="text"]:focus {
            border-color: #24A1DE;
        }
        .btn-tg {
            width: 100%;
            padding: 14px;
            background: #24A1DE;
            border: none;
            border-radius: 12px; /* Мягкое закругление */
            color: white;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            margin-top: 16px;
            letter-spacing: 0.3px;
            transition: background 0.15s ease;
        }
        .btn-tg:hover {
            background: #1d8abf;
        }
        .footer-text {
            margin-top: 35px;
            font-size: 13px;
            color: #a1a5a9;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        /* Экран Чата */
        .chat-layout {
            background: #e7ebf0;
            width: 100%;
            height: 100vh;
            max-width: 520px;
            display: flex;
            flex-direction: column;
            box-shadow: 0 0 40px rgba(0,0,0,0.05);
        }
        .chat-bar {
            background: #ffffff;
            padding: 12px 20px;
            border-bottom: 1px solid #dcdcdc;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .chat-info-title {
            font-weight: 700;
            font-size: 17px;
            color: #212121;
        }
        .chat-info-count {
            font-size: 13px;
            color: #707579;
            margin-top: 2px;
            font-weight: 500;
        }
        .btn-exit {
            color: #e53e3e;
            text-decoration: none;
            font-size: 14px;
            font-weight: 600;
        }
        .message-area {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .bubble {
            background: #ffffff;
            padding: 8px 14px 7px;
            border-radius: 14px;
            max-width: 80%;
            align-self: flex-start;
            box-shadow: 0 1px 1px rgba(0,0,0,0.08);
            position: relative;
        }
        .bubble.me {
            background: #e1f3fc;
            align-self: flex-end;
        }
        .bubble-author {
            font-size: 13px;
            font-weight: 700;
            color: #3a82c4;
            margin-bottom: 3px;
        }
        .bubble-text {
            font-size: 15px;
            line-height: 1.4;
            color: #000000;
            word-break: break-word;
            font-weight: 500;
        }
        .input-bar {
            background: #ffffff;
            padding: 12px;
            display: flex;
            gap: 10px;
            align-items: center;
            border-top: 1px solid #e0e0e0;
        }
    </style>
</head>
<body>

    {% if not session.get('username') %}
    <!-- Экран Входа -->
    <div class="login-card">
        <div class="tg-badge">//</div>
        <h1>[ KHAIRAKAN // CORE ]</h1>
        <p>Для подключения к внутренней сети введите ваш идентификатор.</p>
        <form action="{{ url_for('login') }}" method="POST">
            <input type="text" name="username" placeholder="Идентификатор (ID / Имя)" required autocomplete="off">
            <button type="submit" class="btn-tg">Connect</button>
        </form>
        <!-- Твоя фирменная подпись внизу -->
        <div class="footer-text">Чат тыва хайыракан</div>
    </div>
    {% else %}
    <!-- Экран Чата -->
    <div class="chat-layout">
        <div class="chat-bar">
            <div>
                <div class="chat-info-title">Внутренний канал</div>
                <div class="chat-info-count">session: {{ session['username'] }}</div>
            </div>
            <a href="{{ url_for('logout') }}" class="btn-exit">Disconnect</a>
        </div>
        
        <div class="message-area">
            <div class="bubble" style="align-self: center; background: rgba(230,235,240,0.8); box-shadow: none; border: 1px solid #c9d2db;">
                <div class="bubble-text" style="color: #667380; font-size: 12px; text-align: center; letter-spacing: 0.5px; font-weight: 600;">
                    SECURE CONNECTION ESTABLISHED. MESSAGES ARE TEMPORARY.
                </div>
            </div>
            
            {% for m in messages %}
            <div class="bubble {% if m.author == session['username'] %}me{% endif %}">
                {% if m.author != session['username'] %}
                <div class="bubble-author">{{ m.author }}</div>
                {% endif %}
                <div class="bubble-text">{{ m.text }}</div>
            </div>
            {% endfor %}
        </div>
        
        <form action="{{ url_for('send') }}" method="POST" class="input-bar">
            <input type="text" name="message" placeholder="Написать сообщение..." required autocomplete="off">
            <button type="submit" class="btn-tg" style="width: auto; margin-top: 0; padding: 12px 20px;">Отправить</button>
        </form>
    </div>
    {% endif %}

</body>
</html>
"""

global_messages = []

@app.route('/')
def index():
    return render_template_string(TG_STYLE_TEMPLATE, messages=global_messages)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    if username:
        session['username'] = username
    return redirect(url_for('index'))

@app.route('/send', methods=['POST'])
def send():
    if 'username' in session:
        msg_text = request.form.get('message', '').strip()
        if msg_text:
            global_messages.append({
                'author': session['username'],
                'text': msg_text
            })
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
