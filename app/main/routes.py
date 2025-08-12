from flask import render_template, jsonify
from app.main import bp
from app import db
from app.models import HistoryData, PredictionDecade

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='主页')


@bp.route('/data/<string:data_type>/<int:year>/<int:month>/<string:colrow>', methods=['GET'])
def get_data(data_type, year, month, colrow):
    try:
        # 選擇對應模型與欄位
        if data_type == "history":
            model = HistoryData
            year_field = "Year"
            month_field = "Month"
        elif data_type == "prediction":
            model = PredictionDecade
            year_field = "Year_Target"
            month_field = "Month_Target"
        else:
            return jsonify({"error": "Invalid data_type, use 'history' or 'prediction'"}), 400

        # 檢查 column_id+row_id 格式
        if '+' not in colrow:
            return jsonify({"error": "Invalid format, expected column_id+row_id"}), 400

        column_id_str, row_id_str = colrow.split('+', 1)
        column_id = int(column_id_str)
        row_id = int(row_id_str)

        # 查詢資料
        filter_args = {
            year_field: year,
            month_field: month,
            "column_id": column_id,
            "row_id": row_id
        }
        record = model.query.filter_by(**filter_args).first()

        if not record:
            return jsonify({"error": "Data not found"}), 404

        # 回傳所有欄位
        return jsonify({col.name: getattr(record, col.name) for col in record.__table__.columns})

    except Exception as e:
        return jsonify({"error": str(e)}), 500