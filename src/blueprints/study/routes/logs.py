from datetime import date

from flask import jsonify, redirect, render_template, request, url_for
from flask_login import login_required

from ..import study_bp
from ....usecases.study.get_logs_by_date import get_logs_by_date_usecase
from ....usecases.study.upsert_logs_bulk import upsert_logs_bulk_usecase

# 学習登録画面表示、日付に応じて学習履歴変更
@study_bp.route('/study-logs/<user_id>', methods=['GET', 'POST'])
@login_required
def study_logs_view(user_id: str):
    if request.method == 'GET':
        today = date.today().strftime('%Y-%m-%d')
        date_str = request.args.get('selected_date') or today
        return render_template('study/study_logs.html', selected_date=date_str)
    
    data = request.get_json(silent=True) or {}
    date_str = data.get('study_date')
    result = get_logs_by_date_usecase(user_id=user_id, date_str=date_str)
    return jsonify(result)

# 学習記録登録・編集・削除
@study_bp.route('/study-logs_process/<user_id>', methods=['POST'])
@login_required
def study_logs_process(user_id: str):
    result = upsert_logs_bulk_usecase(user_id=user_id, form=request.form)
    return redirect(url_for('study.study_logs_view', user_id=user_id, selected_date=result["selected_date"]))

