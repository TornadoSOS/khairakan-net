from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_khairakan_triple_tg_2026'

# База данных теперь хранит посты, чаты И объявления (market) по комнатам
rooms_data = {
    'Общий канал': {'posts': [{'avatar': '', 'text': 'Официальная анонимная стена Хайыракана!'}], 'messages': [], 'market': [{'avatar': '', 'text': 'Школьный маркет. Выкладывайте сюда объявления или поиски вещей!'}]},
    '5 А': {'posts': [], 'messages': [], 'market': []}, '5 Б': {'posts': [], 'messages': [], 'market': []},
    '6 А': {'posts': [], 'messages': [], 'market': []}, '6 Б': {'posts': [], 'messages': [], 'market': []},
    '7 А': {'posts': [], 'messages': [], 'market': []}, '7 Б': {'posts': [], 'messages': [], 'market': []},
    '8 А': {'posts': [], 'messages': [], 'market': []}, '8 Б': {'posts': [], 'messages': [], 'market': []},
    '9 А': {'posts': [], 'messages': [], 'market': []}, '9 Б': {'posts': [], 'messages': [], 'market': []},
    '10 А': {'posts': [], 'messages': [], 'market': []}, '10 Б': {'posts': [], 'messages': [], 'market': []},
    '11 А': {'posts': [], 'messages': [], 'market': []}, '11 Б': {'posts': [], 'messages': [], 'market': []}
}

COMBINED_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Khairakan Core v3</title>
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Nunito:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Nunito', sans-serif; }
        body { background-color: #f4f4f5; color: #222222; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        
        .header-bar {
            background: #ffffff; width: 100%; max-width: 550px; padding: 15px 20px;
            display: flex; align-items: center; justify-content: space-between;
            border-bottom: 1px solid #dae1e8; position: sticky; top: 0; z-index: 10;
        }
        .header-title { font-weight: 800; font-size: 18px; color: #24A1DE; }
        
        .avatar-box {
            width: 42px; height: 42px; border-radius: 50%; background: #24A1DE; overflow: hidden;
            cursor: pointer; display: flex; justify-content: center; align-items: center; color: white; font-weight: 700;
            border: 2px solid #ffffff; box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }
        .avatar-img { width: 100%; height: 100%; object-fit: cover; }
        
        .class-menu {
            background: #ffffff; width: 100%; max-width: 550px; padding: 10px 15px 5px;
            display: flex; gap: 8px; overflow-x: auto; white-space: nowrap;
        }
        .class-menu::-webkit-scrollbar { height: 0px; }
        .class-link {
            background: #f1f3f4; padding: 6px 14px; border-radius: 20px;
            text-decoration: none; color: #5f6368; font-size: 14px; font-weight: 600;
        }
        .class-link.active { background: #24A1DE; color: #ffffff; }
        
        /* ТРИ ВКЛАДКИ */
        .mode-switch {
            background: #ffffff; width: 100%; max-width: 550px; padding: 5px 15px 10px;
            display: flex; gap: 6px; border-bottom: 1px solid #dae1e8;
        }
        .mode-btn {
            flex: 1; text-align: center; padding: 8px 4px; background: #f1f3f4;
            border-radius: 12px; text-decoration: none; color: #5f6368; font-size: 13px; font-weight: 700;
        }
        .mode-btn.active { background: #e1f3fc; color: #24A1DE; border: 1px solid #24A1DE; }
        
        .main-container { width: 100%; max-width: 550px; padding: 15px; display: flex; flex-direction: column; gap: 15px; flex: 1; }
        .post-form-card { background: #ffffff; padding: 16px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.02); display: flex; flex-direction: column; gap: 12px; }
        textarea { width: 100%; height: 80px; border: 1px solid #dae1e8; border-radius: 12px; padding: 12px; font-size: 15px; outline: none; resize: none; background: #f9fafb; font-weight: 500;}
        textarea:focus { border-color: #24A1DE; background: #ffffff; }
        .btn-publish { background: #24A1DE; color: white; border: none; padding: 12px; border-radius: 12px; font-size: 15px; font-weight: 600; cursor: pointer; }
        
        .post-card { background: #ffffff; padding: 16px; border-radius: 16px; box-shadow: 0 2px 12px rgba(0,0,0,0.02); display: flex; gap: 12px; }
        .post-avatar { width: 38px; height: 38px; border-radius: 50%; background: #24A1DE; overflow: hidden; display: flex; justify-content: center; align-items: center; color: white; font-size: 11px; font-weight: 700; flex-shrink: 0; }
        .post-content { flex: 1; }
        .post-meta { font-size: 13px; font-weight: 700; color: #24A1DE; margin-bottom: 4px; }
        .post-text { font-size: 15px; line-height: 1.45; color: #1c1e21; word-break: break-word; font-weight: 500; }
        
        .chat-box { background: #e7ebf0; border-radius: 18px; min-height: 400px; max-height: 60vh; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.03); }
        .msg-area { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 8px; }
        .msg-row { display: flex; gap: 8px; align-items: flex-end; max-width: 85%; }
        .msg-row.me { align-self: flex-end; flex-direction: row-reverse; }
        .bubble { background: #ffffff; padding: 8px 14px 7px; border-radius: 14px; box-shadow: 0 1px 1px rgba(0,0,0,0.05); }
        .msg-row.me .bubble { background: #e1f3fc; }
        .bubble-author { font-size: 12px; font-weight: 700; color: #3a82c4; margin-bottom: 2px; }
        .chat-input-bar { background: #ffffff; padding: 10px; display: flex; gap: 8px; border-top: 1px solid #e0e0e0; }
        .chat-input { flex: 1; padding: 10px 14px; border: 1px solid #dae1e8; border-radius: 10px; outline: none; font-size: 15px; font-weight: 500; }
        .btn-send { background: #24A1DE; color: white; border: none; padding: 0 16px; border-radius: 10px; font-weight: 600; cursor: pointer; }
        .footer-brand { font-size: 11px; color: #bcc0c4; text-align: center; margin: 20px 0; text-transform: uppercase; letter-spacing: 1px; font-weight: 700; }
    </style>
</head> <body>

    <div class="header-bar">
        <div class="header-title">[ KHAIRAKAN // CORE v3 ]</div>
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
    
    <!-- ТРИ ВКЛАДКИ -->
    <div class="mode-switch">
        <a href="{{ url_for('index', cat=current_cat, mode='posts') }}" class="mode-btn {% if current_mode == 'posts' %}active{% endif %}">📢 Стенгазета</a>
        <a href="{{ url_for('index', cat=current_cat, mode='chat') }}" class="mode-btn {% if current_mode == 'chat' %}active{% endif %}">💬 Живой Чат</a>
        <a href="{{ url_for('index', cat=current_cat, mode='market') }}" class="mode-btn {% if current_mode == 'market' %}active{% endif %}">🛍️ Маркет</a>
    </div>
    
    <div class="main-container">
        
        {% if current_mode == 'posts' %}
        <!-- 1 ВКЛАДКА: СТЕНА СПЛЕТЕН -->
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
        
        {% elif current_mode == 'chat' %}
        <!-- 2 ВКЛАДКА: ЖИВОЙ ЧАТ -->
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
        
        {% else %}
        <!-- 3 ВКЛАДКА: ШКОЛЬНЫЙ МАРКЕТ -->
        <form action="{{ url_for('add_market') }}" method="POST" class="post-form-card">
            <input type="hidden" name="category" value="{{ current_cat }}">
            <textarea name="text" placeholder="Объявление, продажа или поиск вещи в {{ current_cat }}..." required autocomplete="off"></textarea>
            <button type="submit" class="btn-publish">Подать объявление</button>
        </form>
        
        {% for item in market|reverse %}
        <div class="post-card" style="border-left: 4px solid #24A1DE;">
            <div class="post-avatar">
                {% if item.avatar %}
                    <img src="{{ item.avatar }}" class="avatar-img" alt="m-av">
                {% else %}
                    🛍️
                {% endif %}
            </div>
            <div class="post-content">
                <div class="post-meta" style="color: #24A1DE;">Объявление • {{ current_cat }}</div>
                <div class="post-text">{{ item.text }}</div>
            </div>
        </div>
        {% endfor %}
        
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
    market = rooms_data[current_cat].get('market', [])
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
        messages=messages,
        market=market
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

@app.route('/add_market', methods=['POST'])
def add_market():
    category = request.form.get('category', 'Общий канал')
    text = request.form.get('text', '').strip()
    if text and category in rooms_data:
        if 'market' not in rooms_data[category]:
            rooms_data[category]['market'] = []
        rooms_data[category]['market'].append({
            'text': text,
            'avatar': session.get('user_avatar', '')
        })
    return redirect(url_for('index', cat=category, mode='market'))

if __name__ == '__main__':
    app.run(debug=True)
