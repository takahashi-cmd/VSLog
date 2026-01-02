from datetime import datetime

from flask import render_template
from flask_login import login_required

from ..import study_bp

# ダッシュボード画面表示
@study_bp.route('/dashboard/<user_id>', methods=['GET'])
@login_required
def dashboard_view(user_id: str):
    this_year = datetime.now().year
    this_month = datetime.now().month

    return render_template(
        'study/dashboard.html',
        this_year=this_year,
        this_month=this_month
        )
