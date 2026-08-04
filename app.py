import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Главная страница входа
@app.route('/')
def login_page():
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>KHAIRAKAN NET</title>
    </head>
    <body style="background-color: #121212; color: white; font-family: sans-serif; text-align: center; padding-top: 50px;">
        <h1 style="color: #bc13fe; text-shadow: 0 0 10px #bc13fe; font-size: 32px;">⚔️ KHAIRAKAN NET ⚔️</h1>
        <p style="color: #aaa;">Тайный чат нашей школы. Вход без кринжа и цензуры.</p>
        
        <form action="/enter_chat" method="POST" style="margin-top: 40px;">
            <input type="text" name="nickname" placeholder="Придумай крутой ник..." required 
                   style="padding: 12px; width: 260px; border-radius: 8px; border: 2px solid #bc13fe; background: #222; color: white; font-size: 16px;"><br><br>
            <button type="submit" style="padding: 12px 24px; background-color: #bc13fe; color: white; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; box-shadow: 0 0 15px #bc13fe;">
                ВОЙТИ В ЧАТ 🚀
            </button>
        </form>
    </body>
    </html>
    """
    return render_template_string(html_code)

# Страница чата
@app.route('/enter_chat', methods=['POST'])
def enter_chat():
    username = request.form['nickname']
    return f"""
    <body style="background-color: #121212; color: white; font-family: sans-serif; text-align: center; padding-top: 50px;">
        <h2 style="color: #bc13fe;">Привет, {username}!</h2>
        <p>Ты успешно зашел в систему <b>KHAIRAKAN NET</b>.</p>
        <p style="color: #555;">[Тут скоро будет запущен внутренний шоп и общие чаты]</p>
        <br>
        <a href="/" style="color: #bc13fe; text-decoration: none;">⬅️ Выйти</a>
    </body>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
