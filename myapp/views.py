from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from myapp import app, db
from datetime import datetime, date
import re

# ルーティング
# ログイン画面
@app.route('/login', methods=['GET', 'POST'])
def login_view():
    return render_template('login.html')

# def login_process():

# 新規登録画面
@app.route('/signup', methods=['GET', 'POST'])
def signup_view():
    return render_template('signup.html')

# パスワード再設定画面
@app.route('/password-reset', methods=['GET', 'POST'])
def password_reset_view():
    return render_template('password_reset.html')