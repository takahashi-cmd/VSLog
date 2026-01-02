

# DBから取得した列を辞書形式に変換
def row_to_dict(row):
    d = dict(row._mstudy_bping)
    if d.get('study_date'):
        d['study_date'] = d['study_date'].isoformat()
    if d.get('hour') is not None:
        d['hour'] = float(d['hour'])
    return d