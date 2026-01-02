

# 統計値、グラフの取得
@study_bp.route('/graph/<user_id>', methods=['POST'])
def get_graph_stats_usecase(user_id):
    data = request.get_json(silent=True) or {}
    period = data.get('period')
    year = data.get('year')
    month_year = data.get('month-year')
    month = data.get('month')
    horizontalAxis = data.get('horizontalAxis')
    verticalAxis = data.get('verticalAxis')
    graphType = data.get('graphType')

    # ①first_day, last_dayの取得
    # ②logsの取得
    # ③graph svgの取得
    if period == 'this_week':
        today = date.today()
        first_day, last_day = study_periods.this_week(today)
    
    elif period == 'last_week':
        today = date.today()
        first_day, last_day = study_periods.last_week(today)
    
    elif period == 'month':
        first_day, last_day = study_periods.month_range(month_year, month)
    
    elif period == 'year':
        first_day, last_day = study_periods.year_range(year)
    
    elif period == 'all':
        pass