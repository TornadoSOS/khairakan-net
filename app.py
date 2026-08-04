from flask import Flask, render_template_string, request, redirect, url_for, session
import uuid

app = Flask(__name__)
app.secret_key = 'super_secret_khairakan_easy_2026'

# Самая простая база данных в памяти
rooms_data = {
    'Общий канал района': [],
    'Признавашки Улуг-Хем': [],
    'СОШ с. Хайыракан': [],
    'Шагонар — СОШ №1': [],
    'Шагонар — СОШ №2': [],
    'Шагонар — Гимназия': []
}

# Компактный шаблон "Всё в одном" в стиле ночного ТГ
EASY_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Khairakan Dark Net</title>
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Nunito:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Nunito', sans-serif; }
        body { background-color: #17212b; color: #f5f6f7; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        
        .header { background: #242f3d; width: 100%; max-width: 500px; padding: 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #101921; position: sticky; top: 0; z-index: 10; }
        .title { font-weight: 900; color: #5288c1; font-size: 18px; }
        
        .menu { background: #242f3d; width: 100%; max-width: 500px; padding: 10px; display: flex; gap: 8px; overflow-x: auto; white-space: nowrap; border-bottom: 1px solid #101921; }
        .menu::-webkit-scrollbar { height: 0px; }
        .tab-link { background: #17212b; padding: 6px 14px; border-radius: 20px; text-decoration: none; color: #7f91a4; font-size: 13px; font-weight: 700; border: 1px solid #2f3e4e; }
        .tab-link.active { background: #5288c1; color: white; border-color: #5288c1; }
        
        .container { width: 100%; max-width: 500px; padding: 15px; display: flex; flex-direction: column; gap: 12px; flex: 1; }
        .card { background: #242f3d; padding: 14px; border-radius: 14px; border: 1px solid #2f3e4e; display: flex; flex-direction: column; gap: 8px; }
        
        textarea, input[type="text"] { width: 100%; padding: 12px; border: 1px solid #2f3e4e; border-radius: 10px; background: #17212b; color: white; font-size: 15px; outline: none; }
        textarea { height: 70px; resize: none; }
        input[type="text"]:focus, textarea:focus { border-color: #5288c1; }
        
        .btn { background: #5288c1; color: white; border: none; padding: 12px; border-radius: 10px; font-size: 15px; font-weight: 700; cursor: pointer; }
        
        .msg-box { background: #242f3d; padding: 10px 14px; border-radius: 12px; border: 1px solid #2f3e4e; line-height: 1.4; }
        .msg-meta { font-size: 12px; color: #5288c1; font-weight: 700; margin-bottom: 2px; display: flex; justify-content: space-between; }
        .msg-text { font-size: 15px; color: #dfe2e4; font-weight: 500; }
        
        .footer { font-size: 11px; color: #5288c1; text-align: center; margin: 20px 0; font-weight: 800; letter-spacing: 1px; }
    </style>
</head>
<body>

    {% if not session.get('username') %}
    <!-- ПРОСТОЙ ВХОД -->
    <div class="card" style="margin-top: 20vh; max-width: 360px; width: 100%; text-align: center; padding: 30px 20px;">
        <h2 style="color: #5288c1; font-weight: 900; margin-bottom: 8px;">KHAIRAKAN NET</h2>
        <p style="color: #7f91a4; font-size: 13px; margin-bottom: 20px;">Введите ваш никнейм для входа</p>
        <form action="{{ url_for('login') }}" method="POST" style="display: flex; flex-direction: column; gap: 12px;">
            <input type="text" name="username" placeholder="Ваш никнейм" required autocomplete="off">
            <button type="submit" class="btn">Войти в сеть</button>
        </form>
    </div>
    {% else %}
    
    <!-- ГЛАВНЫЙ ЭКРАН -->
    <div class="header">
        <div class="title">🕶️ {{ session['username'] }}</div>
        <div style="display: flex; gap: 10px; align-items: center;">
            {% if session.get('is_admin') %}
                <span style="color: #e54242; font-size: 11px; font-weight: 800;">[БОГ]</span>
            {% else %}
                <span style="color: #2f3e4e; font-size: 10px; cursor: pointer;" onclick="adminLogin()">🔑</span>
            {% endif %}
            <a href="{{ url_for('logout') }}" style="color: #7f91a4; text-decoration: none; font-size: 13px; font-weight: 700;">Выйти</a>
        </div>
    </div>
    
    <!-- СЕЛЕКТОР ВЕТОК И КАНАЛОВ -->
    <div class="menu">
        {% for room in rooms %}
        <a href="{{ url_for('index', room=room) }}" class="tab-link {% if room == current_room %}active{% endif %}">
            {{ room }}
        </a>
        {% endfor %}
    </div>
    
    <div class="container">
        <!-- ФОРМА ОТПРАВКИ -->
        <form action="{{ url_for('send') }}" method="POST" class="post-form-card">
            <input type="hidden" name="room" value="{{ current_room }}">
            <textarea name="message" placeholder="Напишите анонимное сообщение в {{ current_room }}..." required autocomplete="off"></textarea>
            <button type="submit" class="btn">Опубликовать в {{ current_room }}</button>
        </form>
        
        <!-- ЛЕНТА СООБЩЕНИЙ -->
        {% if not messages %}
            <div style="text-align: center; color: #7f91a4; font-size: 14px; margin-top: 20px; opacity: 0.7;">Здесь пока тихо... Напишите что-нибудь первым!</div>
        {% endif %}
        
        {% for m in messages|reverse %}
        <div class="msg-box">
            <div class="msg-meta">
                <span>{{ m.author }} [ID: {{ m.sid[:6] }}]</span>
                {% if session.get('is_admin') %}
                    <a href="{{ url_for('delete_msg', room=current_room, index=messages.index(m)) }}" style="color: #e53e3e; text-decoration: none;">Удалить</a>
                {% endif %}
            </div>
            <div class="msg-text">{{ m.text }}</div>
        </div>
        {% endfor %}
        
        <div class="footer">ЧАТ ТЫВА ХАЙЫРАКАН</div>
    </div>

    <script>
        function adminLogin() {
            let pass = prompt("Введите секретный ключ админа:");
            if (pass === "777") {
                fetch('/admin_auth', { method: 'POST' }).then(() => { window.location.reload(); });
            } else if (pass !== null) {
                alert("Неверный ключ!");
            }
        }
    </script>
    {% endif %}

</body>
</html>
"""

@app.route('/')
def index():
    current_room = request.args.get('room', 'Общий канал района')
    if current_room not in rooms_data:
        current_room = 'Общий канал района'
    
    if not session.get('user_sid'):
        session['user_sid'] = str(uuid.uuid4())
        
    return render_template_string(EASY_TEMPLATE, rooms=list(rooms_data.keys()), current_room=current_room, messages=rooms_data[current_room])

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    if username:
        session['username'] = username
        session['user_sid'] = str(uuid.uuid4())
    return redirect(url_for('index'))

@app.route('/admin_auth', methods=['POST'])
def admin_auth():
    session['is_admin'] = True
    return '', 204

@app.route('/send', methods=['POST'])
def send():
    room = request.form.get('room', 'Общий канал района')
    text = request.form.get('message', '').strip()
    if text and room in rooms_data:
        rooms_data[room].append({
            'text': text,
            'author': session.get('username', 'Аноним'),
            'sid': session.get('user_sid', 'unknown')
        })
    return redirect(url_for('index', room=room))

@app.route('/delete_msg')
def delete_msg():
    if session.get('is_admin'):
        room = request.args.get('room')
        try:
            idx = int(request.args.get('index'))
            if room in rooms_data:
                rooms_data[room].pop(idx)
        except: pass
    return redirect(url_for('index', room=room))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
