from collections import defaultdict
from datetime import datetime, date

from flask import request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from ...extensions import db
from ...models.studyLogs import StudyLog
from ...models.fields import Field
from . import study_bp

# ホーム画面表示
@study_bp.route('/index/<user_id>', methods=['GET'])
@login_required
def index_view(user_id):
    this_year = datetime.now().year
    this_month = datetime.now().month

    return render_template(
        'study/index.html',
        this_year=this_year,
        this_month=this_month
        )

@study_bp.route('/graph/<user_id>', methods=['POST'])
def get_graph_stats(user_id):
    data = request.get_json(silent=True) or {}
    period = data.get('period')
    year_str = data.get('year')
    month_year_str = data.get('month-year')
    month_str = data.get('month')
    horizontalAxis = data.get('horizontalAxis')
    verticalAxis = data.get('verticalAxis')
    graphType = data.get('graphType')

    # print(data, period, year_str, month_year_str, month_str, horizontalAxis, verticalAxis, graphType)

    svg = None
    total_day = 0
    total_hour = 0.00
    avg_hour = 0.00

    # 今週の学習グラフ、学習日数、時間の取得
    if period == 'this_week':
        svg = StudyLog.get_this_week_graph(user_id, period, horizontalAxis, verticalAxis, graphType)
        this_week_stats = StudyLog.get_this_week_stats(user_id)
        total_day = this_week_stats['study_days']
        total_hour = this_week_stats['total_hours']
        avg_hour = this_week_stats['average_per_day']

    # 先週の学習グラフ、学習日数、時間の取得
    elif period == 'last_week':
        svg = StudyLog.get_last_week_graph(user_id, period, horizontalAxis, verticalAxis, graphType)
        last_week_stats = StudyLog.get_last_week_stats(user_id)
        total_day = last_week_stats['study_days']
        total_hour = last_week_stats['total_hours']
        avg_hour = last_week_stats['average_per_day']

    # 月間の学習グラフ、学習日数、時間の取得
    elif period == 'month' and month_year_str and month_str:
        svg = StudyLog.get_month_graph(user_id, period, horizontalAxis, verticalAxis, graphType, month_year_str, month_str)
        month_stats = StudyLog.get_month_stats(user_id, month_year_str, month_str)
        total_day = month_stats['study_days']
        total_hour = month_stats['total_hours']
        avg_hour = month_stats['average_per_day']

    # 年間の学習グラフ、学習日数、時間の取得
    elif period == 'year' and year_str:
        svg = StudyLog.get_year_graph(user_id, period, horizontalAxis, verticalAxis, graphType, year_str)
        year_stats = StudyLog.get_year_stats(user_id, year_str)
        total_day = year_stats['study_days']
        total_hour = year_stats['total_hours']
        avg_hour = year_stats['average_per_day']

    # 全期間の学習グラフ、学習日数、時間の取得
    elif period == 'all':
        svg = StudyLog.get_all_time_graph(user_id, period, horizontalAxis, verticalAxis, graphType)
        total_day = StudyLog.get_total_day(user_id)
        total_hour = StudyLog.get_total_hour(user_id)
        avg_hour = round(total_hour / total_day, 1) if total_day else 0.0

    if svg:
        # print('svgあり')
        return jsonify({
        "svg": svg,
        "total_day": total_day,
        "total_hour": total_hour,
        "avg_hour": avg_hour
        })
    else:
        # print('svg無し')
        return jsonify({
        "svg": svg,
        "total_day": total_day,
        "total_hour": total_hour,
        "avg_hour": avg_hour
        })



# 学習登録画面表示、日付に応じて学習履歴変更
@study_bp.route('/study-logs/<user_id>', methods=['GET', 'POST'])
@login_required
def study_logs_view(user_id):
    if request.method == 'GET':
        today = date.today().strftime('%Y-%m-%d')
        date_str = request.args.get('selected_date') or today
        return render_template('study/study_logs.html', selected_date=date_str)
    
    elif request.method == 'POST':
        data = request.get_json(silent=True) or {}
        date_str = data.get('study_date')
        study_logs = StudyLog.get_study_logs_by_study_date(user_id, date_str)
        if study_logs:
            study_dicts = [] # 辞書の初期化
            for row in study_logs:
                d = row_to_dict(row)
                study_dicts.study_bpend(d)
            return jsonify({
                "studyDicts": study_dicts,
                "selectedDate": date_str
            })
        else:
            return jsonify({
                "studyDicts": study_logs,
                "selectedDate": date_str
            })

# 学習記録登録・編集・削除
@study_bp.route('/study-logs_process/<user_id>', methods=['POST'])
@login_required
def study_logs_process(user_id):
    study_dates = request.form.getlist('study_dates[]')
    hours = request.form.getlist('hours[]')
    fieldnames = request.form.getlist('fieldname[]')
    contents = request.form.getlist('contents[]')
    study_log_ids = request.form.getlist('study_log_id[]')
    row_actions = request.form.getlist('row_action[]')
    selected_date = ''.join(set(study_dates)) # study_datesから日付を取得

    # print("DEBUG:", study_dates, hours, fieldnames, contents, study_log_ids, row_actions)
    registered = False

    try:
        for study_date, hour, fieldname, content, study_log_id, row_action in zip(study_dates, hours, fieldnames, contents, study_log_ids, row_actions):
            study_date = datetime.strptime(study_date, "%Y-%m-%d").date() if study_date else None
            # print("DEBUG:", study_date, hour, fieldname, study_log_id, row_action)
            # 登録
            if fieldname.strip() and fieldname.strip() not in [f.fieldname for f in current_user.fields]:
                flash(f'{fieldname.strip()}が登録されていません。先に学習分野の登録をお願いします。', 'エラー')
                continue
            elif row_action == 'new' and study_date and hour and fieldname.strip():
                study_log = StudyLog(
                    user_id = user_id,
                    field_id = Field.get_field_id(user_id, fieldname),
                    study_date = study_date,
                    hour = hour,
                    content = content
                )
                db.session.add(study_log)
                registered = True
            # 編集
            elif row_action == 'update' and study_log_id:
                study_log = StudyLog.query.get(study_log_id)
                if study_log and study_log.user_id == user_id:
                    study_log.field_id = Field.get_field_id(user_id, fieldname)
                    study_log.study_date = study_date
                    study_log.hour = hour
                    study_log.content = content
                    registered = True
            # 削除
            elif row_action == 'delete' and study_log_id:
                study_log = StudyLog.query.get(study_log_id)
                if study_log and study_log.user_id == user_id:
                    db.session.delete(study_log)
                    registered = True
        db.session.commit()
        if registered:
            flash('学習記録の更新が完了しました', '正常')
    except IntegrityError as e:
        db.session.rollback()
        flash('学習記録の更新ができませんでした（重複または制約違反）', 'エラー')
    except Exception as e:
        db.session.rollback()
        flash('予期しないエラーが発生しました', 'エラー')
    finally:
        db.session.close()
    
    return redirect(url_for('study.study_logs_view', user_id=user_id, selected_date=selected_date))

# 学習分野画面表示
@study_bp.route('/study-fields/<user_id>', methods=['GET'])
@login_required
def study_fields_view(user_id):
    return render_template('study/study_fields.html')

# 学習分野登録・編集・削除
@study_bp.route('/study-fields/<user_id>/', methods=['POST'])
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
                if fieldname.strip().lower() in existing_names:
                    flash(f'{fieldname}は既に登録されています', 'エラー')
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
            flash('学習分野の更新に成功しました', '正常')
    except IntegrityError as e:
        db.session.rollback()
        flash('学習分野の更新ができませんでした（重複または制約違反）', 'エラー')
    except Exception as e:
        db.session.rollback()
        flash('予期しないエラーが発生しました', 'エラー')
    finally:
        db.session.close()

    return redirect(url_for('study.study_fields_view', user_id=user_id))

# 学習履歴一覧画面表示
@study_bp.route('/study-logs-list/<user_id>', methods=['GET'])
@login_required
def study_logs_list_view(user_id):
    this_year = datetime.now().year
    this_month = datetime.now().month
    this_month_year = date(this_year, this_month, 1).strftime('%Y-%m')
    return render_template('study/study_logs_list.html', this_year=this_year, this_month=this_month,selected_date=this_month_year)

@study_bp.route('/study-logs-list/<user_id>', methods=['POST'])
@login_required
def study_logs_list_process(user_id):
    data = request.get_json(silent=True) or {}
    selected_date = data.get('study_date')
    year_str, month_str = selected_date.split('-')
    study_logs = StudyLog.get_study_logs_by_study_month(user_id, year_str, month_str)
    study_dicts = defaultdict(list) # 辞書の初期化
    for row in study_logs:
        d = row_to_dict(row)
        study_dicts[d['study_date']].study_bpend(d)
    return jsonify({
        "selectedDate": selected_date,
        "studyDicts": study_dicts,
    })

# DBから取得した列を辞書形式に変換
def row_to_dict(row):
    d = dict(row._mstudy_bping)
    if d.get('study_date'):
        d['study_date'] = d['study_date'].isoformat()
    if d.get('hour') is not None:
        d['hour'] = float(d['hour'])
    return d

