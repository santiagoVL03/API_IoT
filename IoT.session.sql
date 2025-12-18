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


CREATE TABLE sensor_humedad (
  id_sensor SERIAL PRIMARY KEY,
  sensor_value_humedad FLOAT NULL,
  sensor_value_temperatura FLOAT NULL,
  date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP NULL  
);

CREATE TABLE fire_sensor_alerts (
  id_alert SERIAL PRIMARY KEY,
  ip_camera VARCHAR(50),
  date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  alert_status VARCHAR(50)
);