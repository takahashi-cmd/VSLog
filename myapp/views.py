from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .app import app, db
from .models import User, Field, StudyLog
from datetime import datetime, date
import re
import uuid

# 定数定義
EMAIL_PATTERN = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+$'
PASSWORD_PATTERN = r'^.{8,16}$'

# ルーティング
# ログイン画面表示
@app.route('/login', methods=['GET'])
def login_view():
    return render_template('login.html')

# ログイン処理
@app.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or password == '':
        flash('空のフォームがあります')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('メールアドレスの形式になっていません')
    elif re.match(PASSWORD_PATTERN, password) is None:
        flash('パスワードは8文字以上16文字以内で入力してください')
    else:
        user = User.select_by_email(email)
        if user is None:
            flash('登録されていないメールアドレスです')
            return redirect(url_for('login_view'))
        else:
            if check_password_hash(user.password, password):
                flash('ログインに成功しました')
                login_user(user)
                return redirect(url_for('index_view'))
            else:
                flash('異なるパスワードです')
                return redirect(url_for('login_view'))

# 新規登録画面表示
@app.route('/signup', methods=['GET'])
def signup_view():
    return render_template('signup.html')

# 新規登録処理
@app.route('/signup', methods=['POST'])
def signup_process():
    username = request.form.get('username')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if username == '' or email == '' or password1 == '' or password2 == '':
        flash('空のフォームがあります')
    elif password1 != password2:
        flash('パスワードが一致しません')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('メールアドレスの形式になっていません')
    elif re.match(PASSWORD_PATTERN, password1) is None:
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

# パスワード再設定画面表示
@app.route('/password-reset', methods=['GET'])
def password_reset_view():
    return render_template('password_reset.html')

# パスワード再設定処理
@app.route('/password-reset', methods=['POST'])
def password_reset_process():
    email = request.form.get('email')
    new_password1 = request.form.get('new_password1')
    new_password2 = request.form.get('new_password2')

    if email == '' or new_password1 == '' or new_password2 == '':
        flash('空のフォームがあります')
    elif new_password1 != new_password2:
        flash('パスワードが一致しません')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('メールアドレスの形式になっていません')
    elif re.match(PASSWORD_PATTERN, new_password1) is None:
        flash('パスワードは8文字以上16文字以内で入力してください')
    else:
        DBuser = User.select_by_email(email)
        if DBuser == None:
            flash('登録されていないメールアドレスです') 
        else:
            try:
                DBuser.password = generate_password_hash(new_password1)
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            return redirect(url_for('login_view'))
    return redirect(url_for('password_reset_view'))

# ホーム画面表示
@app.route('/index', methods=['GET'])
def index_view():
    print('hello world')
