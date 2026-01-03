from flask import jsonify, request
from flask_login import login_required, current_user

from .. import study_bp
from ....usecases.study.get_graph_stats import get_graph_stats_usecase

# グラフ、統計値の取得
@study_bp.route('/graph/<user_id>', methods=['POST'])
@login_required
def get_graph_stats(user_id :str):
    if user_id != str(current_user.id):
        return jsonify({"error": "forbidden"}), 403
    
    data = request.get_json(silent=True) or {}
    svg, total_day, total_hour, avg_hour = get_graph_stats_usecase(
        user_id=user_id,
        period=data.get('period'),
        year=data.get('year'),
        month_year=data.get('month-year'),
        month=data.get('month'),
        horizontalAxis=data.get('horizontalAxis'),
        verticalAxis=data.get('verticalAxis'),
        graphType=data.get('graphType')
        )
    
    return jsonify({
        'svg': svg,
        'total_day': total_day,
        'total_hour': total_hour,
        'avg_hour': avg_hour,
    })
