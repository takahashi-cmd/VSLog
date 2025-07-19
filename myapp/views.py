from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
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
                login_user(user)
                return redirect(url_for('index_view', user_id=user.user_id))
            else:
                flash('異なるパスワードです')
                return redirect(url_for('login_view'))
    return redirect(url_for('login_view'))

# ログアウト
@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    flash('ログアウトしました')
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

# ーーーーーーーーーーーーーーーーーーー以降認証後画面ーーーーーーーーーーーーーーーーーーーーーーーーーーーー

# ホーム画面表示
@app.route('/index/<user_id>', methods=['GET'])
@login_required
def index_view(user_id):
    return render_template('index.html')

# マイページ画面表示
@app.route('/mypage/<user_id>', methods=['GET'])
@login_required
def mypage_view(user_id):
    return render_template('mypage.html')

# プロフィール編集画面表示
@app.route('/profile-edit/<user_id>', methods=['GET'])
@login_required
def profile_edit_view(user_id):
    return render_template('profile_edit.html')

# プロフィール編集
@app.route('/profile-edit/<user_id>', methods=['POST'])
@login_required
def profile_edit_process(user_id):
    new_username = request.form.get('new_username')
    new_email = request.form.get('new_email')

    if new_username == '' or new_email == '':
        flash('空のフォームがあります')
    elif re.match(EMAIL_PATTERN, new_email) is None:
        flash('メールアドレスの形式になっていません')
    else:
        try:
            current_user.username = new_username
            current_user.email = new_email
            db.session.commit()
            flash('プロフィール編集が完了しました')
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        return redirect(url_for('profile_edit_view', user_id=user_id))
    return redirect(url_for('profile_edit_view', user_id=user_id))

# パスワード変更画面表示
@app.route('/password-update/<user_id>', methods=['GET'])
@login_required
def password_update_view(user_id):
    return render_template('password_update.html')

# パスワード変更
@app.route('/password-update/<user_id>', methods=['POST'])
@login_required
def password_update_process(user_id):
    current_password = request.form.get('current_password')
    new_password1 = request.form.get('new_password1')
    new_password2 = request.form.get('new_password2')

    if current_password == '' or new_password1 == '' or new_password2 == '':
        flash('空のフォームがあります')
    elif generate_password_hash(current_password) == current_user.password:
        flash('現在のパスワードが正しくありません')
    elif new_password1 != new_password2:
        flash('新しいパスワードと新しいパスワード（確認用）が一致しません')
    elif re.match(PASSWORD_PATTERN, new_password1) is None:
        flash('パスワードは8文字以上16文字以内で入力してください')
    else:
        try:
            current_user.password = generate_password_hash(new_password1)
            db.session.commit()
            flash('パスワード変更が完了しました')
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        return redirect(url_for('password_update_view', user_id=user_id))
    return redirect(url_for('password_update_view', user_id=user_id))

# 学習登録画面表示
@app.route('/study-logs/<user_id>', methods=['GET'])
@login_required
def study_logs_view(user_id):
    return render_template('study_logs.html')

# 学習登録
@app.route('/study-logs/<user_id>', methods=['POST'])
@login_required
def study_logs_process(user_id):
    study_dates = request.form.getlist('study_dates[]')
    hours = request.form.getlist('hours[]')
    fieldnames = request.form.getlist('fieldname[]')
    contents = request.form.getlist('contents[]')

    registered = False

    try:
        for study_date, hour, fieldname, content in zip(study_dates, hours, fieldnames, contents):
            # 登録
            if study_date and hour and fieldname:
                study_log = StudyLog(
                    user_id = user_id,
                    field_id = Field.get_field_id(user_id, fieldname),
                    study_date = study_date,
                    hour = hour,
                    content = content
                )
                db.session.add(study_log)
                registered = True
        db.session.commit()
        if registered:
            flash('学習記録の登録が完了しました')
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
    
    return redirect(url_for('study_logs_view', user_id=user_id))




# 学習分野画面表示
@app.route('/study-fields/<user_id>', methods=['GET'])
@login_required
def study_fields_view(user_id):
    return render_template('study_fields.html')

# 学習分野登録・編集・削除
@app.route('/study-fields/<user_id>/', methods=['POST'])
@login_required
def study_fields_process(user_id):
    fieldnames = request.form.getlist('fieldname[]')
    color_codes = request.form.getlist('color_code[]')
    field_ids = request.form.getlist('field_id[]')
    row_actions = request.form.getlist('row_action[]')

    registered = False
    DBfields = Field.get_fields_all(user_id)
    existing_names = [f.fieldname.lower() for f in DBfields]

    try:
        for fieldname, color_code, field_id, row_action in zip(fieldnames, color_codes, field_ids, row_actions):
            # 登録
            if row_action == 'new' and fieldname.strip():
                if fieldname in existing_names:
                    flash(f'{fieldname}は既に登録されています')
                else:
                    field = Field(
                        user_id = user_id,
                        fieldname = fieldname,
                        color_code = color_code
                    )
                    db.session.add(field)
                    registered = True
            # 編集
            elif row_action == 'update' and fieldname.strip() and field_id:
                field = Field.query.get(field_id)
                if field and field.user_id == user_id:
                    field.fieldname = fieldname
                    field.color_code = color_code
                    registered = True
            # 削除
            elif row_action == 'delete' and field_id:
                field = Field.query.get(field_id)
                if field and field.user_id == user_id:
                    db.session.delete(field)
        db.session.commit()
        if registered:
            flash('学習分野の更新に成功しました')
    except IntegrityError as e:
        db.session.rollback()
        flash('データベースに登録できませんでした（重複または制約違反）')
    except Exception as e:
        db.session.rollback()
        flash('予期しないエラーが発生しました')
    finally:
        db.session.close()

    return redirect(url_for('study_fields_view', user_id=user_id))

# 学習履歴一覧画面表示
@app.route('/study-logs-list/<user_id>', methods=['GET'])
@login_required
def study_logs_list(user_id):
    return render_template('study_logs_list.html')

