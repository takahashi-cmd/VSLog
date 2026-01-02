from flask import jsonify, request
from flask_login import login_required

from ..import study_bp
from ....usecases.study.get_graph_stats import get_graph_stats_usecase

# 統計値、グラフの取得
@study_bp.route('/graph/<user_id>', methods=['POST'])
def get_graph_stats(user_id :str):
    data = request.get_json(silent=True) or {}
    result = get_graph_stats_usecase(
        user_id=user_id,
        period=data.get('period'),
        year=data.get('year'),
        month_year=data.get('month-year'),
        month=data.get('month'),
        horizontalAxis=data.get('horizontalAxis'),
        verticalAxis=data.get('verticalAxis'),
        graphType=data.get('graphType')
        )

    return jsonify(result)
