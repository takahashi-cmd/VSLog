import re
import uuid

from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash

from ...extensions import db
from ...models.users import User

# 定数定義
EMAIL_PATTERN = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+$'
PASSWORD_PATTERN = r'^.{8,16}$'

from . import auth_bp

# ルーティング
# ログイン画面表示
@auth_bp.route('/login', methods=['GET'])
def login_view():
    return render_template('auth/login.html')

# ログイン処理
@auth_bp.route('/login', methods=['POST'])
def login_process():
    email = request.form.get('email')
    password = request.form.get('password')

    if email == '' or password == '':
        flash('空のフォームがあります', 'エラー')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('メールアドレスの形式になっていません', 'エラー')
    elif re.match(PASSWORD_PATTERN, password) is None:
        flash('パスワードは8文字以上16文字以内で入力してください', 'エラー')
    else:
        user = User.select_by_email(email)
        if user is None:
            flash('登録されていないメールアドレスです', 'エラー')
            return redirect(url_for('auth.login_view'))
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                flash('ログインしました', '正常')
                return redirect(url_for('study.index_view', user_id=user.user_id))
            else:
                flash('パスワードが違います', 'エラー')
                return redirect(url_for('auth.login_view'))
    return redirect(url_for('auth.login_view'))

# ログアウト
@auth_bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('ログアウトしました', '正常')
    return redirect(url_for('auth.login_view'))

# 新規登録画面表示
@auth_bp.route('/signup', methods=['GET'])
def signup_view():
    return render_template('auth/signup.html')

# 新規登録処理
@auth_bp.route('/signup', methods=['POST'])
def signup_process():
    username = request.form.get('username')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if username == '' or email == '' or password1 == '' or password2 == '':
        flash('ユーザー名、メールアドレス、パスワードのいずれかが空です', 'エラー')
    elif password1 != password2:
        flash('パスワードが一致しません', 'エラー')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('メールアドレスの形式になっていません', 'エラー')
    elif re.match(PASSWORD_PATTERN, password1) is None:
        flash('パスワードは8文字以上16文字以内で入力してください', 'エラー')
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
            flash('既に登録されているメールアドレスです', 'エラー')
        else:
            try:
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            flash('新規登録が完了しました', '正常')
            return redirect(url_for('auth.login_view'))
    return redirect(url_for('auth.signup_view'))

# パスワード再設定画面表示
@auth_bp.route('/password-reset', methods=['GET'])
def password_reset_view():
    return render_template('auth/password_reset.html')

# パスワード再設定処理
@auth_bp.route('/password-reset', methods=['POST'])
def password_reset_process():
    email = request.form.get('email')
    new_password1 = request.form.get('new_password1')
    new_password2 = request.form.get('new_password2')

    if email == '' or new_password1 == '' or new_password2 == '':
        flash('空のフォームがあります', 'エラー')
    elif new_password1 != new_password2:
        flash('パスワードが一致しません', 'エラー')
    elif re.match(EMAIL_PATTERN, email) is None:
        flash('メールアドレスの形式になっていません', 'エラー')
    elif re.match(PASSWORD_PATTERN, new_password1) is None:
        flash('パスワードは8文字以上16文字以内で入力してください', 'エラー')
    else:
        DBuser = User.select_by_email(email)
        if DBuser == None:
            flash('登録されていないメールアドレスです', 'エラー') 
        else:
            try:
                DBuser.password = generate_password_hash(new_password1)
                db.session.commit()
            except:
                db.session.rollback()
                raise
            finally:
                db.session.close()
            flash('パスワード再設定が完了しました', '正常')
            return redirect(url_for('auth.login_view'))
    return redirect(url_for('auth.password_reset_view'))

