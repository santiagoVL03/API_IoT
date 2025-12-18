from app.db.conection import db_connection
from app.utils.detection_util import DetectionUtil
from app.utils.email_util import EmailUtil
import logging
import os

class IothumedadController:
    def __init__(self):
        self.db = db_connection
        self.detection_util = DetectionUtil(confidence_threshold=0.5)
        self.email_util = EmailUtil()  # Will load config from email_config.json or env vars
        # Get camera URL from environment variable or use default
        # Common endpoints for IP Webcam app: /video, /videofeed, or just the IP
        self.camera_url = os.getenv('CAMERA_URL', 'http://10.7.135.29:8080')
    
    def index(self):
        return {'message':'Hello, World!'}
    
    def insert_humedad_data(self, sensor_value_humedad, sensor_value_temperatura):
        """Process and save humidity sensor data to PostgreSQL database"""
        try:
            # Validate input parameters
            if sensor_value_humedad is None or sensor_value_temperatura is None:
                return {
                    'error': 'Missing required parameters: sensor_value_humedad and sensor_value_temperatura are required',
                    'success': False
                }
            
            # Convert to float
            try:
                humedad = float(sensor_value_humedad)
                temperatura = float(sensor_value_temperatura)
            except ValueError:
                return {
                    'error': 'Invalid parameter values: sensor_value_humedad and sensor_value_temperatura must be numeric',
                    'success': False
                }
            
            # Insert data into database
            result = self.db.insert_humedad_data(humedad, temperatura)
            alert_information = self.alert_possible_critical_status(
                sensor_value_humedad=humedad, 
                sensor_value_temperatura=temperatura,
                CRITICAL_HUMIDITY_LOW=10.0,
                CRITICAL_HUMIDITY_HIGH=80.0,
                CRITICAL_TEMPERATURE_LOW=15.0,
                CRITICAL_TEMPERATURE_HIGH=35.0
            )

            if alert_information['has_critical_status']:
                logging.warning(f"Critical status detected: {alert_information['alerts']}")
            if alert_information['has_fire_risk']:
                logging.warning(f"Fire risk detected: {alert_information['alerts']}")
                self.request_video_fire_detection()

            return {
                'message': 'Humidity sensor data processed and saved successfully!',
                'success': True,
                'data': {
                    'id_sensor': result['id_sensor'],
                    'sensor_value_humedad': humedad,
                    'sensor_value_temperatura': temperatura,
                    'date_uploaded': result['date_uploaded'].isoformat() if result['date_uploaded'] else None
                },
                'alerts': alert_information['alerts']
            }
            
        except Exception as e:
            logging.error(f"Error processing humidity sensor data: {e}")
            return {
                'error': f'Failed to process humidity sensor data: {str(e)}',
                'success': False
            }
            
    def alert_possible_critical_status (
        self, 
        sensor_value_humedad, 
        sensor_value_temperatura, 
        CRITICAL_HUMIDITY_LOW,
        CRITICAL_HUMIDITY_HIGH,
        CRITICAL_TEMPERATURE_LOW,
        CRITICAL_TEMPERATURE_HIGH
    ):
        """Check for critical humidity or temperature levels and alert if necessary"""
        try:
            alerts = []
            # Check humidity levels
            if sensor_value_humedad < CRITICAL_HUMIDITY_LOW:
                alerts.append(f'Alert: Humidity level too low ({sensor_value_humedad}%)')
            elif sensor_value_humedad > CRITICAL_HUMIDITY_HIGH:
                alerts.append(f'Alert: Humidity level too high ({sensor_value_humedad}%)')
            
            # Check temperature levels
            if sensor_value_temperatura < CRITICAL_TEMPERATURE_LOW:
                alerts.append(f'Alert: Temperature too low ({sensor_value_temperatura}°C)')
            elif sensor_value_temperatura > CRITICAL_TEMPERATURE_HIGH:
                alerts.append(f'Alert: Temperature too high ({sensor_value_temperatura}°C)')

            if sensor_value_humedad < CRITICAL_HUMIDITY_LOW and sensor_value_temperatura > CRITICAL_TEMPERATURE_LOW:
                alerts.clear()
                alerts.append('Critical Alert: Low Humidity and High Temperature detected simultaneously! Risk of fire hazard.')
                
            return {
                'alerts': alerts,
                'has_critical_status': len(alerts) > 0,
                'has_fire_risk': any('fire hazard' in alert.lower() for alert in alerts)
            }
            
        except Exception as e:
            logging.error(f"Error checking critical status: {e}")
            return {
                'alerts': [],
                'has_critical_status': False,
                'has_fire_risk': False
            }
            
    def request_video_fire_detection(self):
        """Request video fire detection from camera and save alert to database."""
        try:
            logging.info("="*70)
            logging.info("FIRE RISK DETECTED - Initiating camera fire detection")
            logging.info(f"Camera URL: {self.camera_url}")
            logging.info("="*70)
            
            # Capture video from camera and detect fire
            detection_results = self.detection_util.detect_fire_from_camera_url(
                camera_url=self.camera_url,
                duration_seconds=15
            )
            
            if not detection_results.get('success'):
                error_msg = detection_results.get('error', 'Unknown error')
                logging.error(f"Failed to detect fire from camera: {error_msg}")
                
                # Save error alert to database
                try:
                    self.db.insert_fire_alert(
                        ip_camera=self.camera_url,
                        alert_status=f'ERROR: {error_msg}'
                    )
                except Exception as db_error:
                    logging.error(f"Failed to save error alert to database: {db_error}")
                
                return {
                    'success': False,
                    'error': error_msg
                }
            
            # Determine alert status based on detection results
            fire_detected = detection_results.get('fire_detected', False)
            confidence = detection_results.get('confidence', 0.0)
            fire_percentage = detection_results.get('fire_percentage', 0.0)
            
            if fire_detected:
                alert_status = f'FIRE_DETECTED (Confidence: {confidence:.2%}, Frames: {fire_percentage:.1f}%)'
                logging.warning("="*70)
                logging.warning("FIRE DETECTED IN CAMERA FEED!")
                logging.warning(f"   Confidence: {confidence:.2%}")
                logging.warning(f"   Fire in {fire_percentage:.1f}% of frames")
                logging.warning(f"   Total frames: {detection_results.get('total_frames', 0)}")
                logging.warning(f"   Frames with fire: {detection_results.get('frames_with_fire', 0)}")
                logging.warning("="*70)
            else:
                alert_status = 'NO_FIRE_DETECTED'
                logging.info("="*70)
                logging.info("✓ No fire detected in camera feed")
                logging.info(f"   Frames analyzed: {detection_results.get('total_frames', 0)}")
                logging.info("="*70)
            
            # Save alert to database
            try:
                alert_result = self.db.insert_fire_alert(
                    ip_camera=self.camera_url,
                    alert_status=alert_status
                )
                
                logging.info(f"Fire alert saved to database (ID: {alert_result['id_alert']})")
                
                # Send email notification
                if fire_detected:
                    try:
                        logging.info("Sending email notification...")
                        email_result = self.email_util.send_fire_alert_email(
                            fire_detected=fire_detected,
                            detection_results=detection_results,
                            camera_url=self.camera_url,
                            alert_id=alert_result['id_alert']
                        )
                        
                        if email_result['success']:
                            logging.info(f"Email sent successfully to {email_result['total_sent']} recipient(s)")
                            logging.info(f"Email details: {email_result['results']}")
                        else:
                            logging.error(f"Failed to send email: {email_result}")
                            
                    except Exception as email_error:
                        logging.error(f"Failed to send email notification: {email_error}")
                # Continue anyway - email failure shouldn't block the process
                return {
                    'success': True,
                    'fire_detected': fire_detected,
                    'alert_id': alert_result['id_alert'],
                    'detection_results': detection_results,
                    'email_sent': email_result.get('success', False) if 'email_result' in locals() else False
                }
                
            except Exception as db_error:
                logging.error(f"Failed to save alert to database: {db_error}")
                return {
                    'success': False,
                    'error': f'Detection completed but failed to save to database: {str(db_error)}',
                    'detection_results': detection_results
                }
            
        except Exception as e:
            logging.error(f"Error in fire detection process: {e}")
            import traceback
            traceback.print_exc()
            
            # Try to save error to database
            try:
                self.db.insert_fire_alert(
                    ip_camera=self.camera_url,
                    alert_status=f'SYSTEM_ERROR: {str(e)}'
                )
            except:
                pass
            
            return {
                'success': False,
                'error': str(e)
            }

    def get_last_humedad_data(self):
        """Retrieve the last humidity sensor data from the database."""
        try:
            query = """
                SELECT id_sensor, sensor_value_humedad, sensor_value_temperatura, date_uploaded
                FROM sensor_humedad
                ORDER BY id_sensor DESC
                LIMIT 1
            """
            result = self.db.execute_query(query)
            row = result.fetchone()
            if row:
                return {
                    'message': 'Last humidity sensor data retrieved successfully',
                    'success': True,
                    'data': {
                        'id_sensor': row[0],
                        'sensor_value_humedad': row[1],
                        'sensor_value_temperatura': row[2],
                        'date_uploaded': row[3].isoformat() if row[3] else None
                    }
                }
            else:
                return {
                    'message': 'No humidity sensor data found',
                    'success': False
                }
        except Exception as e:
            logging.error(f"Error retrieving last humidity sensor data: {e}")
            return {
                'error': f'Failed to retrieve last humidity sensor data: {str(e)}',
                'success': False
            }
            
    def get_last_humedad_warning_data(self):
        """Retrieve the last humidity sensor data that triggered a warning."""
        try:
            query = """
                SELECT id_alert, ip_camera, date_uploaded, alert_status
                FROM fire_sensor_alerts fsa
                ORDER BY id_alert DESC
                LIMIT 1
            """
            result = self.db.execute_query(query)
            row = result.fetchone()
            if row:
                return {
                    'message': 'Last humidity warning sensor data retrieved successfully',
                    'success': True,
                    'data': {
                        'id_alert': row[0],
                        'ip_camera': row[1],
                        'date_uploaded': row[2].isoformat() if row[2] else None,
                        'alert_status': row[3]
                    }
                }
            else:
                return {
                    'message': 'No humidity warning sensor data found',
                    'success': False
                }
        except Exception as e:
            logging.error(f"Error retrieving last humidity warning sensor data: {e}")
            return {
                'error': f'Failed to retrieve last humidity warning sensor data: {str(e)}',
                'success': False
            }