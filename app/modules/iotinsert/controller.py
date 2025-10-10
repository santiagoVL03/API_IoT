from app.db.conection import db_connection
import logging

class IotinsertController:
    def __init__(self):
        self.db = db_connection
    
    def index(self):
        return {'message':'Hello, World!'}
    
    def process_sensor_data(self, type_sensor, sensor_value):
        """Process and save sensor data to PostgreSQL database"""
        try:
            # Validate input parameters
            if not type_sensor or not sensor_value:
                return {
                    'error': 'Missing required parameters: type_sensor and sensor_value are required',
                    'success': False
                }
            
            # Insert data into database
            result = self.db.insert_sensor_data(type_sensor, sensor_value)
            
            return {
                'message': 'Sensor data processed and saved successfully!',
                'success': True,
                'data': {
                    'id_sensor': result['id_sensor'],
                    'type_sensor': result['type_sensor'],
                    'sensor_value': result['sensor_value'],
                    'date_uploaded': result['date_uploaded'].isoformat() if result['date_uploaded'] else None
                }
            }
            
        except Exception as e:
            logging.error(f"Error processing sensor data: {e}")
            return {
                'error': f'Failed to process sensor data: {str(e)}',
                'success': False
            }
