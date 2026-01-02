from datetime import datetime, date

from flask import jsonify, render_template, request
from flask_login import login_required

from .. import study_bp
from ....usecases.study.get_logs_by_month import get_logs_by_month_usecase

# 学習履歴一覧画面表示
@study_bp.route('/study-logs-list/<user_id>', methods=['GET'])
@login_required
def study_logs_list_view(user_id: str):
    this_year = datetime.now().year
    this_month = datetime.now().month
    this_month_year = date(this_year, this_month, 1).strftime('%Y-%m')
    return render_template('study/study_logs_list.html', this_year=this_year, this_month=this_month,selected_date=this_month_year)

# 月に応じた学習履歴の表示
@study_bp.route('/study-logs-list/<user_id>', methods=['POST'])
@login_required
def study_logs_list_process(user_id: str):
    data = request.get_json(silent=True) or {}
    selected_date = data.get('study_date')
    result = get_logs_by_month_usecase(user_id=user_id, selected_date=selected_date)
    return jsonify(result)
