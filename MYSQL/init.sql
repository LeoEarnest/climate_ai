-- Climate AI Database Structure
CREATE DATABASE IF NOT EXISTS climate_metadata;
USE climate_metadata;

-- 創建 grid_metadata 表 (主要的網格資訊表)
CREATE TABLE IF NOT EXISTS grid_metadata (
    grid_id INT PRIMARY KEY,
    latitude DECIMAL(8, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    region_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 創建 environmental_data 表 (環境數據表)
CREATE TABLE IF NOT EXISTS environmental_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grid_id INT,
    date DATE NOT NULL,
    temperature DECIMAL(5, 2),
    humidity DECIMAL(5, 2),
    rainfall DECIMAL(8, 2),
    wind_speed DECIMAL(5, 2),
    solar DECIMAL(8, 2),
    pressure DECIMAL(7, 2),
    elevation DECIMAL(8, 2),
    ndvi DECIMAL(6, 4),
    water_coverage DECIMAL(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grid_id) REFERENCES grid_metadata(grid_id) ON DELETE CASCADE
);

-- 創建 model_predictions 表 (模型預測結果表)
CREATE TABLE IF NOT EXISTS model_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    grid_id INT,
    prediction_date DATE NOT NULL,
    predicted_temperature DECIMAL(5, 2),
    predicted_humidity DECIMAL(5, 2),
    predicted_rainfall DECIMAL(8, 2),
    model_version VARCHAR(50),
    confidence_score DECIMAL(5, 4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (grid_id) REFERENCES grid_metadata(grid_id) ON DELETE CASCADE
);

-- 插入測試資料到 grid_metadata
INSERT INTO grid_metadata (grid_id, latitude, longitude, region_name) VALUES
(1, 25.033, 121.565, '台北市'),
(2, 22.628, 120.301, '高雄市'),
(3, 24.148, 120.674, '台中市'),
(4, 22.997, 120.214, '台南市'),
(5, 24.802, 120.971, '新竹市');

-- 插入測試資料到 environmental_data
INSERT INTO environmental_data (grid_id, date, temperature, humidity, rainfall, wind_speed, solar, pressure, elevation, ndvi, water_coverage) VALUES
(1, '2023-01-15', 18.5, 75.2, 2.3, 3.1, 4.5, 1013.2, 150.0, 0.65, 0.12),
(1, '2023-01-16', 19.2, 73.8, 0.0, 2.8, 5.2, 1014.1, 150.0, 0.65, 0.12),
(2, '2023-01-15', 24.1, 68.5, 0.5, 4.2, 6.8, 1012.8, 25.0, 0.45, 0.08),
(2, '2023-01-16', 25.3, 66.2, 0.0, 3.9, 7.1, 1013.5, 25.0, 0.45, 0.08),
(3, '2023-01-15', 21.8, 72.1, 1.2, 2.5, 5.9, 1013.7, 84.0, 0.58, 0.15);

-- 插入測試資料到 model_predictions
INSERT INTO model_predictions (grid_id, prediction_date, predicted_temperature, predicted_humidity, predicted_rainfall, model_version, confidence_score) VALUES
(1, '2023-01-17', 20.1, 71.5, 0.8, 'v1.2.3', 0.8642),
(1, '2023-01-18', 19.8, 73.2, 1.5, 'v1.2.3', 0.8234),
(2, '2023-01-17', 26.2, 64.8, 0.2, 'v1.2.3', 0.9012),
(2, '2023-01-18', 27.1, 63.5, 0.0, 'v1.2.3', 0.8876),
(3, '2023-01-17', 22.5, 70.3, 0.5, 'v1.2.3', 0.8567);
