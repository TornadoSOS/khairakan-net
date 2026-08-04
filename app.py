from flask import Flask, render_template, request, redirect, url_for, session
import uuid

app = Flask(__name__, template_folder='.')
app.secret_key = 'super_secret_khairakan_dark_net_2026'

# База данных для школ района и глобальных признавашек
rooms_data = {
    'Общий канал района': {'posts': [{'avatar': '', 'text': 'Добро пожаловать в единую темную сеть Улуг-Хемского района!', 'sid': 'system', 'author': 'Система'}], 'messages': [], 'market': []},
    'СОШ с. Хайыракан': {'posts': [], 'messages': [], 'market': []},
    'Шагонар — СОШ №1': {'posts': [], 'messages': [], 'market': []},
    'Шагонар — СОШ №2': {'posts': [], 'messages': [], 'market': []},
    'Шагонар — СОШ №3': {'posts': [], 'messages': [], 'market': []},
    'Шагонар — Гимназия': {'posts': [], 'messages': [], 'market': []},
    'СОШ с. Торгалыг': {'posts': [], 'messages': [], 'market': []},
    'СОШ с. Арыг-Узю': {'posts': [], 'messages': [], 'market': []},
    'СОШ с. Ийи-Тал': {'posts': [], 'messages': [], 'market': []}
}

ulug_xem_priznavashki = []
private_chats = {}

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    if username:
        session['username'] = username
        session['user_avatar'] = ''
        session['user_sid'] = str(uuid.uuid4())
    return redirect(url_for('index'))

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if session.get('user_sid'):
        session['username'] = request.form.get('username', 'Аноним').strip()
        session['user_avatar'] = request.form.get('avatar_url', '').strip()
    return '', 204

@app.route('/admin_auth', methods=['POST'])
def admin_auth():
    session['is_admin'] = True
    return '', 204

@app.route('/delete_item')
def delete_item():
    if session.get('is_admin'):
        dtype = request.args.get('type')
        cat = request.args.get('cat')
        try:
            idx = int(request.args.get('index'))
            if cat in rooms_data and dtype in rooms_data[cat]:
                rooms_data[cat][dtype].pop(idx)
        except: pass
    return redirect(url_for('index', branch='schools', cat=request.args.get('cat'), mode=request.args.get('type', 'posts')))

@app.route('/delete_prizn')
def delete_prizn():
    if session.get('is_admin'):
        try:
            idx = int(request.args.get('index'))
            ulug_xem_priznavashki.pop(idx)
        except: pass
    return redirect(url_for('index', branch='priznavashki'))

@app.route('/open_dm')
def open_dm():
    my_sid = session.get('user_sid')
    target_sid = request.args.get('target_sid')
    if not my_sid or not target_sid or my_sid == target_sid:
        return redirect(url_for('index'))
    pair_key = "-".join(sorted([my_sid, target_sid]))
    if pair_key not in private_chats:
        private_chats[pair_key] = []
    return redirect(url_for('view_dm_chat', pair_key=pair_key, cat=request.args.get('cat', 'Общий канал района')))

@app.route('/view_dm_chat')
def view_dm_chat():
    pair_key = request.args.get('pair_key')
    cat = request.args.get('cat', 'Общий канал района')
    my_sid = session.get('user_sid')
    if not pair_key or not my_sid:
        return redirect(url_for('index', branch='schools', cat=cat, mode='dm'))
    sids = pair_key.split('-')
    if my_sid not in sids and not session.get('is_admin'):
        return redirect(url_for('index', branch='schools', cat=cat, mode='dm'))
    target_sid = sids[1] if sids[0] == my_sid else sids[0]
    dm_messages = private_chats.get(pair_key, [])
    return render_template('index.html', current_branch='schools', current_mode='dm_chat', dm_messages=dm_messages, current_pair_key=pair_key, target_display_id=target_sid[:6], current_cat=cat, categories=list(rooms_data.keys()))

@app.route('/send_private_msg', methods=['POST'])
def send_private_msg():
    my_sid = session.get('user_sid')
    pair_key = request.form.get('pair_key')
    cat = request.form.get('category', 'Общий канал района')
    text = request.form.get('message', '').strip()
    if my_sid and pair_key and text and pair_key in private_chats:
        private_chats[pair_key].append({'sender': my_sid, 'text': text})
    return redirect(url_for('view_dm_chat', pair_key=pair_key, cat=cat))

@app.route('/')
def index():
    current_branch = request.args.get('branch', 'schools')
    current_cat = request.args.get('cat', 'Общий канал района')
    current_mode = request.args.get('mode', 'posts')
    if current_cat not in rooms_data:
        current_cat = 'Общий канал района'
    user_session_id = session.get('user_sid', '')
    categories_list = list(rooms_data.keys())
    posts = rooms_data[current_cat]['posts']
    market = rooms_data[current_cat].get('market', [])
    raw_messages = rooms_data[current_cat]['messages']
    messages = []
    for i, m in enumerate(raw_messages):
        messages.append({'text': m['text'], 'avatar': m['avatar'], 'author': m.get('author', 'Аноним'), 'sid': m['sid'], 'is_admin_msg': m.get('admin', False), 'is_me': m['sid'] == user_session_id, 'original_index': i})
    dialogs = []
    for key in private_chats.keys():
        sids = key.split('-')
        if user_session_id in sids:
            target_sid = sids[1] if sids[0] == user_session_id else sids[0]
            dialogs.append({'key': key, 'display_id': target_sid[:6]})
        elif session.get('is_admin'):
            dialogs.append({'key': key, 'display_id': f"{sids[0][:4]} ⇄ {sids[1][:4]}"})
    return render_template('index.html', current_branch=current_branch, categories=categories_list, current_cat=current_cat, current_mode=current_mode, posts=posts, messages=messages, market=market, dialogs=dialogs, priznavashki=ulug_xem_priznavashki)

@app.route('/add_priznavashki', methods=['POST'])
def add_priznavashki():
    text = request.form.get('text', '').strip()
    user_session_id = session.get('user_sid', '')
    if text and user_session_id:
        ulug_xem_priznavashki.append({'text': text, 'sid': user_session_id})
    return redirect(url_for('index', branch='priznavashki'))

@app.route('/add_post', methods=['POST'])
def add_post():
    category = request.form.get('category', 'Общий канал района')
    text = request.form.get('text', '').strip()
    user_session_id = session.get('user_sid', '')
    if text and category in rooms_data:
        rooms_data[category]['posts'].append({'text': text, 'avatar': session.get('user_avatar', ''), 'author': session.get('username', 'Аноним'), 'sid': user_session_id, 'admin': session.get('is_admin', False)})
    return redirect(url_for('index', branch='schools', cat=category, mode='posts'))

@app.route('/add_message', methods=['POST'])
def add_message():
    category = request.form.get('category', 'Общий канал района')
    text = request.form.get('message', '').strip()
    user_session_id = session.get('user_sid', '')
    if text and category in rooms_data:
        rooms_data[category]['messages'].append({'text': text, 'avatar': session.get('user_avatar', ''), 'author': session.get('username', 'Аноним'), 'sid': user_session_id, 'admin': session.get('is_admin', False)})
    return redirect(url_for('index', branch='schools', cat=category, mode='chat'))

@app.route('/add_market', methods=['POST'])
def add_market():
    category = request.form.get('category', 'Общий канал района')
    text = request.form.get('text', '').strip()
    user_session_id = session.get('user_sid', '')
    if text and category in rooms_data:
        if 'market' not in rooms_data[category]:
            rooms_data[category]['market'] = []
        rooms_data[category]['market'].append({'text': text, 'avatar': session.get('user_avatar', ''), 'author': session.get('username', 'Аноним'), 'sid': user_session_id, 'admin': session.get('is_admin', False)})
    return redirect(url_for('index', branch='schools', cat=category, mode='market'))

if __name__ == '__main__':
    app.run(debug=True)
