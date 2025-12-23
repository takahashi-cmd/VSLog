import re

from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_bcrypt import generate_password_hash, check_password_hash

from ...extensions import db
from . import profile_bp

EMAIL_PATTERN = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+$'
PASSWORD_PATTERN = r'^.{8,16}$'

# プロフィール編集画面表示
@profile_bp.route('/profile-edit/<user_id>', methods=['GET'])
@login_required
def profile_edit_view(user_id):
    return render_template('profile/profile_edit.html')

# プロフィール編集
@profile_bp.route('/profile-edit/<user_id>', methods=['POST'])
@login_required
def profile_edit_process(user_id):
    new_username = request.form.get('new_username')
    new_email = request.form.get('new_email')

    if new_username == '' or new_email == '':
        flash('空のフォームがあります', 'エラー')
    elif re.match(EMAIL_PATTERN, new_email) is None:
        flash('メールアドレスの形式になっていません', 'エラー')
    else:
        try:
            current_user.username = new_username
            current_user.email = new_email
            db.session.commit()
            flash('プロフィール編集が完了しました', '正常')
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        return redirect(url_for('profile.profile_edit_view', user_id=user_id))
    return redirect(url_for('profile.profile_edit_view', user_id=user_id))

# パスワード変更画面表示
@profile_bp.route('/password-update/<user_id>', methods=['GET'])
@login_required
def password_update_view(user_id):
    return render_template('profile/password_update.html')

# パスワード変更
@profile_bp.route('/password-update/<user_id>', methods=['POST'])
@login_required
def password_update_process(user_id):
    current_password = request.form.get('current_password')
    new_password1 = request.form.get('new_password1')
    new_password2 = request.form.get('new_password2')

    if current_password == '' or new_password1 == '' or new_password2 == '':
        flash('空のフォームがあります', 'エラー')
    elif not check_password_hash(current_user.password, current_password):
        flash('現在のパスワードが正しくありません', 'エラー')
    elif new_password1 != new_password2:
        flash('新しいパスワードと新しいパスワード（確認用）が一致しません', 'エラー')
    elif re.match(PASSWORD_PATTERN, new_password1) is None:
        flash('パスワードは8文字以上16文字以内で入力してください', 'エラー')
    else:
        try:
            current_user.password = generate_password_hash(new_password1)
            db.session.commit()
            flash('パスワード変更が完了しました', '正常')
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
        return redirect(url_for('profile.password_update_view', user_id=user_id))
    return redirect(url_for('profile.password_update_view', user_id=user_id))
