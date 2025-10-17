from app.db.conection import db_connection
import logging


class IotgiroscopioController:
    def __init__(self):
        self.db = db_connection

    def index(self):
        return {'message': 'Hello, World!'}

    def insert_giroscopio(self, ax=None, ay=None, az=None, gx=None, gy=None, gz=None):
        """Insert gyroscope sensor values into DB. Missing/invalid map to NULL."""
        try:
            result = self.db.insert_giroscopio_data(
                sensor_value_ax=ax,
                sensor_value_ay=ay,
                sensor_value_az=az,
                sensor_value_gx=gx,
                sensor_value_gy=gy,
                sensor_value_gz=gz,
            )
            return {
                'message': 'Gyroscope data saved',
                'success': True,
                'data': {
                    'id_sensor': result['id_sensor'],
                    'date_uploaded': result['date_uploaded'].isoformat() if result['date_uploaded'] else None,
                    'ax': ax,
                    'ay': ay,
                    'az': az,
                    'gx': gx,
                    'gy': gy,
                    'gz': gz,
                },
            }
        except Exception as e:
            logging.error(f"Error inserting gyroscope data: {e}")
            return {
                'error': 'Failed to save gyroscope data',
                'details': str(e),
                'success': False,
            }
    def show_last_data(self):
        """Show last gyroscope sensor data."""
        try:
            query = """
                SELECT id_sensor, sensor_value_ax, sensor_value_ay, sensor_value_az,
                       sensor_value_gx, sensor_value_gy, sensor_value_gz, date_uploaded
                FROM sensor_giroscopio
                ORDER BY id_sensor DESC
                LIMIT 1
            """
            result = self.db.execute_query(query)
            row = result.fetchone()
            if row:
                return {
                    'id_sensor': row[0],
                    'ax': row[1],
                    'ay': row[2],
                    'az': row[3],
                    'gx': row[4],
                    'gy': row[5],
                    'gz': row[6],
                    'date_uploaded': row[7].isoformat() if row[7] else None,
                }
            else:
                return {'message': 'No gyroscope data found'}
        except Exception as e:
            logging.error(f"Error fetching last gyroscope data: {e}")
            return {
                'error': 'Failed to fetch last gyroscope data',
                'details': str(e),
            }
            
    def show_last_day_data(self):
        """Show gyroscope sensor data from the last 24 hours."""
        try:
            query = """
                SELECT id_sensor, sensor_value_ax, sensor_value_ay, sensor_value_az,
                       sensor_value_gx, sensor_value_gy, sensor_value_gz, date_uploaded
                FROM sensor_giroscopio
                WHERE date_uploaded >= NOW() - INTERVAL '1 day'
                ORDER BY date_uploaded DESC
            """
            result = self.db.execute_query(query)
            rows = result.fetchall()
            data = []
            for row in rows:
                data.append({
                    'id_sensor': row[0],
                    'ax': row[1],
                    'ay': row[2],
                    'az': row[3],
                    'gx': row[4],
                    'gy': row[5],
                    'gz': row[6],
                    'date_uploaded': row[7].isoformat() if row[7] else None,
                })
            return data if data else {'message': 'No gyroscope data found in the last 24 hours'}
        except Exception as e:
            logging.error(f"Error fetching last day gyroscope data: {e}")
            return {
                'error': 'Failed to fetch last day gyroscope data',
                'details': str(e),
            }