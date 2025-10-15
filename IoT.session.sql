CREATE TABLE sensor_giroscopio (
  id_sensor SERIAL PRIMARY KEY,
  sensor_value_ax FLOAT NULL,
  sensor_value_ay FLOAT NULL,
  sensor_value_az FLOAT NULL,
  sensor_value_gx FLOAT NULL,
  sensor_value_gy FLOAT NULL,
  sensor_value_gz FLOAT NULL,
  date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL  
);