from flask import render_template, jsonify
from app.main import bp
from app import db
from app.models import HistoryData, PredictionDecade, NDVITemp

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='主頁')


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
            return jsonify({"error": "Invalid data_type, use 'history' or 'prediction' 資料型態錯誤，請輸入'history' or 'prediction "}), 400

        # 檢查 column_id+row_id 格式
        if '+' not in colrow:
            return jsonify({"error": "Invalid format, expected column_id+row_id 無效格式，請輸入column ID+row ID"}), 400

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
            return jsonify({"error": "Data not found 查無資料"}), 404

        # 回傳所有欄位
        return jsonify({col.name: getattr(record, col.name) for col in record.__table__.columns})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/NDVI/<int:month>/<path:veg>/<string:colrow>', methods=['GET'])
def get_ndvi_by_month_veg(month, veg, colrow):
    """
    Example:
      /NDVI/7/0.3/10+0           -> 精確比對 Vegetation_Coverage == 0.3
      /NDVI/7/min0.3/10+0        -> Vegetation_Coverage >= 0.3
      /NDVI/7/max0.3/10+0        -> Vegetation_Coverage <= 0.3

    備註：沒有指定年份，會回傳所有年份的符合資料（依 Year 升冪）。
    """
    try:
        # 解析 col+row
        if '+' not in colrow:
            return jsonify({"error": "Invalid format, expected <col>+<row> 無效格式"}), 400
        col_str, row_str = colrow.split('+', 1)
        column_id = int(col_str)
        row_id = int(row_str)

        # 解析 veg 參數：支援 minX / maxX / 精確值
        mode = 'eq'
        val_str = str(veg)
        if isinstance(veg, str):
            if val_str.startswith('min'):
                mode = 'min'
                val_str = val_str[3:]
            elif val_str.startswith('max'):
                mode = 'max'
                val_str = val_str[3:]
        try:
            veg_val = float(val_str)
        except ValueError:
            return jsonify({"error": "Invalid Vegetation_Coverage; use number, or minX/maxX"}), 400

        # 組查詢
        q = NDVITemp.query.filter_by(Month=month, column_id=column_id, row_id=row_id)
        if mode == 'eq':
            q = q.filter(NDVITemp.Vegetation_Coverage == veg_val)
        elif mode == 'min':
            q = q.filter(NDVITemp.Vegetation_Coverage >= veg_val)
        elif mode == 'max':
            q = q.filter(NDVITemp.Vegetation_Coverage <= veg_val)

        rows = q.order_by(NDVITemp.Year.asc(), NDVITemp.id.asc()).all()
        if not rows:
            return jsonify({"error": "Data not found 查無資料"}), 404

        # 回傳為 list[dict]
        out = []
        for r in rows:
            out.append({c.name: getattr(r, c.name) for c in r.__table__.columns})
        return jsonify(out), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/NDVI/<string:colrow>', methods=['GET'])
def get_ndvi_by_cell(colrow):
    """
    Return all records for the given grid cell (column_id+row_id), across all months/years.
    Output ONLY these fields per row:
      - Month
      - High_Temp_Predicted
      - Low_Temp_Predicted
      - Temperature_Predicted
      - Apparent_Temperature
      - Apparent_Temperature_High
      - Apparent_Temperature_Low
      - Vegetation_Coverage
    Example:
      /NDVI/10+0
    """
    try:
        if '+' not in colrow:
            return jsonify({"error": "Invalid format, expected <col>+<row> 無效格式"}), 400
        col_str, row_str = colrow.split('+', 1)
        column_id = int(col_str)
        row_id = int(row_str)

        fields = [
            "Month",
            "High_Temp_Predicted",
            "Low_Temp_Predicted",
            "Temperature_Predicted",
            "Apparent_Temperature",
            "Apparent_Temperature_High",
            "Apparent_Temperature_Low",
            "Vegetation_Coverage"
        ]

        rows = (
            NDVITemp.query
            .filter_by(column_id=column_id, row_id=row_id)
            .order_by(NDVITemp.Year.asc(), NDVITemp.Month.asc(), NDVITemp.id.asc())
            .all()
        )
        if not rows:
            return jsonify({"error": "Data not found 查無資料"}), 404

        out = []
        for r in rows:
            item = {}
            for f in fields:
                item[f] = getattr(r, f)
            out.append(item)

        return jsonify(out), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500