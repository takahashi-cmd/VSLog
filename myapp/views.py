from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .app import app, db
from .models import User, Field, StudyLog
from datetime import datetime, date
import re
import uuid

# ルーティング
# ログイン画面
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

# def login_process():

# 新規登録画面
@app.route('/signup', methods=['GET'])
def signup_view():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup_process():
    username = request.form.get('username')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+$'
    password_pattern = r'^.{8,16}$'

    if username == '' or email == '' or password1 == '' or password2 == '':
        flash('空のフォームがあります')
    elif password1 != password2:
        flash('パスワードが一致しません')
    elif re.match(email_pattern, email) is None:
        flash('メールアドレスの形式になっていません')
    elif re.match(password_pattern, password1) is None:
        flash('パスワードは8文字以上16文字以内で入力してください')
    else:
        user_id = uuid.uuid4()
        user = User(
            user_id = user_id,
            username = username,
            email = email,
            password = password1
        )

        DBuser = User.select_by_email(email)
        if DBuser != None:
            flash('登録済みのユーザーです') 
        
        else:
            try:
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            return redirect(url_for('login_view'))
    return redirect(url_for('signup_view'))

# パスワード再設定画面
@app.route('/password-reset', methods=['GET'])
def password_reset_view():
    return render_template('password_reset.html')