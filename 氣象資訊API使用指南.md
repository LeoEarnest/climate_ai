# 🌐 API 使用指南 – 取得歷史與預測氣候資料

## 1️⃣ API 概覽

目前後端提供兩組資料查詢 API：

| API 類型 | 路徑格式                                      | 說明                                   |
|----------|---------------------------------------------|--------------------------------------|
| 歷史資料 | `/data/history/<year>/<month>/<column_id>+<row_id>` | 依指定年月與格點 ID 查詢歷史氣候資料       |
| 預測資料 | `/data/prediction/<year>/<month>/<column_id>+<row_id>` | 依指定年月與格點 ID 查詢預測氣候資料（2025–2035） |

`column_id` 與 `row_id` 對應到地理網格，可在 `index_table` 查詢經緯度對應。

---

## 2️⃣ 請求範例

### 取得歷史資料

```bash
GET http://localhost:5000/data/history/2020/7/15+23
```

- 2020 → 年份  
- 7 → 月份  
- 15 → column_id  
- 23 → row_id  

回應範例：

```json
{
  "Year": 2020,
  "Month": 7,
  "column_id": 15,
  "row_id": 23,
  "Humidity": 78.5,
  "Solar": 5.6,
  "Temperature": 27.4,
  "Pressure": 1012.3,
  "Wind": 3.4,
  "High_Temp": 31.2,
  "Low_Temp": 24.5,
  "Rain": 128.0,
  "Vegetation_Coverage": 0.35,
  "Water_Body_Coverage": 0.05
}
```

---

### 取得預測資料

```bash
GET http://localhost:5000/data/prediction/2028/1/15+23
```

- 2028 → 年份（介於 2025–2035）  
- 1 → 月份  
- 15 → column_id  
- 23 → row_id  

回應範例：

```json
{
  "Year_Target": 2028,
  "Month_Target": 1,
  "column_id": 15,
  "row_id": 23,
  "High_Temp_Predicted": 32.1,
  "Low_Temp_Predicted": 25.4,
  "Temperature_Predicted": 28.7,
  "Apparent_Temperature_Predicted": 30.1,
  "Humidity_Predicted": 76.2,
  "Solar_Predicted": 6.0,
  "Pressure_Predicted": 1010.9,
  "Wind_Predicted": 3.0,
  "Rain_Predicted": 110.5,
  "Vegetation_Coverage_Predicted": 0.32
}
```

---

## 3️⃣ 注意事項

- Response 格式為 JSON，適合直接被前端處理與渲染。  
- 年份與月份需為數字，月份 1–12。  
- 若查無資料，會回傳空物件 `{}`。  
- API 預設無分頁功能，單次請求只會返回單一格點、單一月份的資料。  
- `column_id`、`row_id` 可透過查詢 `index_table` 取得對應的經緯度（`new_LON`、`new_LAT`）。  

