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
from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_khairakan_combined_v3'

# База данных для постов и чатов по комнатам
rooms_data = {
    'Общий канал': {'posts': [{'avatar': '', 'text': 'Официальная анонимная стена Хайыракана!'}], 'messages': []},
    '5 А': {'posts': [], 'messages': []}, '5 Б': {'posts': [], 'messages': []},
    '6 А': {'posts': [], 'messages': []}, '6 Б': {'posts': [], 'messages': []},
    '7 А': {'posts': [], 'messages': []}, '7 Б': {'posts': [], 'messages': []},
    '8 А': {'posts': [], 'messages': []}, '8 Б': {'posts': [], 'messages': []},
    '9 А': {'posts': [], 'messages': []}, '9 Б': {'posts': [], 'messages': []},
    '10 А': {'posts': [], 'messages': []}, '10 Б': {'posts': [], 'messages': []},
    '11 А': {'posts': [], 'messages': []}, '11 Б': {'posts': [], 'messages': []}
}

COMBINED_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Khairakan Core v2</title>
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Nunito', sans-serif; }
        body { background-color: #f0f2f5; color: #222222; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        .header-bar {
            background: #ffffff; width: 100%; max-width: 550px; padding: 15px 20px;
            display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid #e0e0e0; position: sticky; top: 0; z-index: 10;
        }
        .header-title { font-weight: 800; font-size: 18px; color: #ff3b30; }
        .avatar-box {
            width: 42px; height: 42px; border-radius: 50%; background: #ff3b30; overflow: hidden;
            cursor: pointer; display: flex; justify-content: center; align-items: center; color: white; font-weight: 700;
        }
        .avatar-img { width: 100%; height: 100%; object-fit: cover; }
        .class-menu {
            background: #ffffff; width: 100%; max-width: 550px; padding: 10px 15px 5px;
            display: flex; gap: 8px; overflow-x: auto; white-space: nowrap;
        }
        .class-menu::-webkit-scrollbar { height: 0px; }
        .class-link {
            background: #f0f2f5; padding: 6px 14px; border-radius: 20px;
            text-decoration: none; color: #4b4f56; font-size: 14px; font-weight: 600;
        }
        .class-link.active { background: #ff3b30; color: #ffffff; }
        .mode-switch {
            background: #ffffff; width: 100%; max-width: 550px; padding: 5px 15px 10px;
            display: flex; gap: 10px; border-bottom: 1px solid #e4e6eb;
        }
        .mode-btn {
            flex: 1; text-align: center; padding: 8px; background: #f0f2f5;
            border-radius: 10px; text-decoration: none; color: #4b4f56; font-size: 14px; font-weight: 700;
        }
        .mode-btn.active { background: #e1f3fc; color: #24A1DE; border: 1px solid #24A1DE; }
        .main-container { width: 100%; max-width: 550px; padding: 15px; display: flex; flex-direction: column; gap: 15px; flex: 1; }
        .post-form-card { background: #ffffff; padding: 16px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.02); display: flex; flex-direction: column; gap: 12px; }
        textarea { width: 100%; height: 80px; border: 1px solid #e4e6eb; border-radius: 12px; padding: 12px; font-size: 15px; outline: none; resize: none; background: #f9fafb; font-weight: 500;}
        textarea:focus { border-color: #ff3b30; background: #ffffff; }
        .btn-publish { background: #ff3b30; color: white; border: none; padding: 12px; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; }
        .post-card { background: #ffffff; padding: 16px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.02); display: flex; gap: 12px; }
        .post-avatar { width: 38px; height: 38px; border-radius: 50%; background: #999; overflow: hidden; display: flex; justify-content: center; align-items: center; color: white; font-size: 11px; font-weight: 700; flex-shrink: 0; }
        .post-content { flex: 1; }
        .post-meta { font-size: 13px; font-weight: 700; color: #65676b; margin-bottom: 4px; }
        .post-text { font-size: 15px; line-height: 1.45; color: #1c1e21; word-break: break-word; font-weight: 500; }
        .chat-box { background: #e7ebf0; border-radius: 16px; min-height: 400px; max-height: 60vh; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.03); }
        .msg-area { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
        .msg-row { display: flex; gap: 8px; align-items: flex-end; max-width: 85%; }
        .msg-row.me { align-self: flex-end; flex-direction: row-reverse; }
        .bubble { background: #ffffff; padding: 8px 14px 7px; border-radius: 14px; box-shadow: 0 1px 1px rgba(0,0,0,0.05); }
        .msg-row.me .bubble { background: #e1f3fc; }
        .bubble-author { font-size: 12px; font-weight: 700; color: #3a82c4; margin-bottom: 2px; }
        .chat-input-bar { background: #ffffff; padding: 10px; display: flex; gap: 8px; border-top: 1px solid #e0e0e0; }
        .chat-input { flex: 1; padding: 10px 14px; border: 1px solid #dae1e8; border-radius: 10px; outline: none; font-size: 15px; }
        .btn-send { background: #24A1DE; color: white; border: none; padding: 0 16px; border-radius: 10px; font-weight: 600; cursor: pointer; }
        .footer-brand { font-size: 11px; color: #bcc0c4; text-align: center; margin: 20px 0; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
    </style>
</head> <body>

    <div class="header-bar">
        <div class="header-title">[ ХАЙЫРАКАН // CORE v2 ]</div>
        <div class="avatar-box" onclick="changeUserAvatar()">
            {% if session.get('user_avatar') %}
                <img src="{{ session['user_avatar'] }}" class="avatar-img" alt="av">
            {% else %}
                ANON
            {% endif %}
        </div>
    </div>
    
    <div class="class-menu">
        {% for cat in categories %}
        <a href="{{ url_for('index', cat=cat, mode=current_mode) }}" class="class-link {% if cat == current_cat %}active{% endif %}">
            {{ cat }}
        </a>
        {% endfor %}
    </div>
    
    <div class="mode-switch">
        <a href="{{ url_for('index', cat=current_cat, mode='posts') }}" class="mode-btn {% if current_mode == 'posts' %}active{% endif %}">📢 Стена сплетен</a>
        <a href="{{ url_for('index', cat=current_cat, mode='chat') }}" class="mode-btn {% if current_mode == 'chat' %}active{% endif %}">💬 Живой Чат</a>
    </div>
    
    <div class="main-container">
        
        {% if current_mode == 'posts' %}
        <form action="{{ url_for('add_post') }}" method="POST" class="post-form-card">
            <input type="hidden" name="category" value="{{ current_cat }}">
            <textarea name="text" placeholder="Напишите анонимную сплетню в {{ current_cat }}..." required autocomplete="off"></textarea>
            <button type="submit" class="btn-publish">Опубликовать анонимно</button>
        </form>
        
        {% for post in posts|reverse %}
        <div class="post-card">
            <div class="post-avatar">
                {% if post.avatar %}
                    <img src="{{ post.avatar }}" class="avatar-img" alt="p-av">
                {% else %}
                    ANON
                {% endif %}
            </div>
            <div class="post-content">
                <div class="post-meta">Сплетня • {{ current_cat }}</div>
                <div class="post-text">{{ post.text }}</div>
            </div>
        </div>
        {% endfor %}
        
        {% else %}
        <div class="chat-box">
            <div class="msg-area">
                <div class="bubble" style="align-self: center; background: rgba(255,255,255,0.7); box-shadow: none;">
                    <div style="color: #707579; font-size: 11px; text-align: center; font-weight: 700;">
                        ДОБРО ПОЖАЛОВАТЬ В АНОНИМНЫЙ ЧАТ: {{ current_cat.upper() }}
                    </div>
                </div>
                
                {% for m in messages %}
                <div class="msg-row {% if m.is_me %}me{% endif %}">
                    <div class="post-avatar" style="width:30px; height:30px;">
                        {% if m.avatar %}
                            <img src="{{ m.avatar }}" class="avatar-img" alt="m-av">
                        {% else %}
                            ?
                        {% endif %}
                    </div>
                    <div class="bubble">
                        <div class="bubble-author">Аноним</div>
                        <div class="post-text" style="font-size:14px;">{{ m.text }}</div>
                    </div>
                </div>
                {% endfor %}
            </div>
            
            <form action="{{ url_for('add_message') }}" method="POST" class="chat-input-bar">
                <input type="hidden" name="category" value="{{ current_cat }}">
                <input type="text" name="message" class="chat-input" placeholder="Написать в чат {{ current_cat }}..." required autocomplete="off">
                <button type="submit" class="btn-send">Отправить</button>
            </form>
        </div>
        {% endif %}
        
        <div class="footer-brand">Чат тыва хайыракан</div>
    </div>

    <script>
        function changeUserAvatar() {
            let url = prompt("Вставьте прямую ссылку на картинку из интернета для вашей аватарки:", "{{ session.get('user_avatar', '') }}");
            if (url !== null) {
                fetch('/set_combined_avatar', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                    body: 'avatar_url=' + encodeURIComponent(url)
                }).then(() => { window.location.reload(); });
            }
        }
        const msgArea = document.querySelector('.msg-area');
        if(msgArea) { msgArea.scrollTop = msgArea.scrollHeight; }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    current_cat = request.args.get('cat', 'Общий канал')
    current_mode = request.args.get('mode', 'posts')
    if current_cat not in rooms_data:
        current_cat = 'Общий канал'
    categories_list = list(rooms_data.keys())
    posts = rooms_data[current_cat]['posts']
    raw_messages = rooms_data[current_cat]['messages']
    messages = []
    user_session_id = session.get('user_sid', '')
    if not user_session_id:
        import uuid
        session['user_sid'] = str(uuid.uuid4())
        user_session_id = session['user_sid']
    for m in raw_messages:
        messages.append({
            'text': m['text'],
            'avatar': m['avatar'],
            'is_me': m['sid'] == user_session_id
        })
    return render_template_string(
        COMBINED_TEMPLATE, 
        categories=categories_list, 
        current_cat=current_cat, 
        current_mode=current_mode,
        posts=posts,
        messages=messages
    )

@app.route('/set_combined_avatar', methods=['POST'])
def set_combined_avatar():
    avatar_url = request.form.get('avatar_url', '').strip()
    session['user_avatar'] = avatar_url
    return '', 204

@app.route('/add_post', methods=['POST'])
def add_post():
    category = request.form.get('category', 'Общий канал')
    text = request.form.get('text', '').strip()
    if text and category in rooms_data:
        rooms_data[category]['posts'].append({
            'text': text,
            'avatar': session.get('user_avatar', '')
        })
    return redirect(url_for('index', cat=category, mode='posts'))

@app.route('/add_message', methods=['POST'])
def add_message():
    category = request.form.get('category', 'Общий канал')
    text = request.form.get('message', '').strip()
    user_session_id = session.get('user_sid', '')
    if text and category in rooms_data:
        rooms_data[category]['messages'].append({
            'text': text,
            'avatar': session.get('user_avatar', ''),
            'sid': user_session_id
        })
    return redirect(url_for('index', cat=category, mode='chat'))

if __name__ == '__main__':
    app.run(debug=True)
