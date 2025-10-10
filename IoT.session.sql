CREATE TABLE sensor_data_raw (
  id_sensor SERIAL PRIMARY KEY,
  type_sensor VARCHAR(50) NULL,
  sensor_value VARCHAR(50) NULL,
  date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL
);
