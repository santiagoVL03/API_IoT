import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import logging

class DatabaseConnection:
    def __init__(self):
        self.username = os.getenv("DB_USER", "arduino_user")
        self.password = os.getenv("DB_PASS", "arduino_pass")
        self.host = os.getenv("DB_HOST", "localhost")
        self.port = int(os.getenv("DB_PORT", 5432))
        self.database = os.getenv("DB_NAME", "sensores")
        self.engine = None
        self.Session = None
        self._create_connection()
    
    def _create_connection(self):
        """Create database connection using SQLAlchemy"""
        try:
            connection_string = f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
            self.engine = create_engine(connection_string, echo=False)
            
            # Test the connection
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            
            # Create session factory
            self.Session = sessionmaker(bind=self.engine)
            logging.info("Database connection established successfully")
            
        except OperationalError as e:
            logging.error(f"Failed to connect to database: {e}")
            raise e
        except Exception as e:
            logging.error(f"Unexpected error connecting to database: {e}")
            raise e
    
    def get_session(self):
        """Get a new database session"""
        if self.Session:
            return self.Session()
        else:
            raise Exception("Database connection not established")
    
    def execute_query(self, query, params=None):
        """Execute a raw SQL query"""
        try:
            with self.engine.connect() as connection:
                if params:
                    result = connection.execute(text(query), params)
                else:
                    result = connection.execute(text(query))
                connection.commit()
                return result
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            raise e
    
    def insert_sensor_data(self, type_sensor, sensor_value):
        """Insert sensor data into the sensor_data_raw table"""
        try:
            query = """
                INSERT INTO sensor_data_raw (type_sensor, sensor_value) 
                VALUES (:type_sensor, :sensor_value)
                RETURNING id_sensor, date_uploaded
            """
            
            params = {
                'type_sensor': type_sensor,
                'sensor_value': sensor_value
            }
            
            result = self.execute_query(query, params)
            row = result.fetchone()
            
            if row:
                return {
                    'id_sensor': row[0],
                    'type_sensor': type_sensor,
                    'sensor_value': sensor_value,
                    'date_uploaded': row[1]
                }
            else:
                raise Exception("Failed to insert sensor data - no row returned")
            
        except Exception as e:
            logging.error(f"Error inserting sensor data: {e}")
            raise e

    def insert_giroscopio_data(self, sensor_value_ax=None, sensor_value_ay=None, sensor_value_az=None,
                               sensor_value_gx=None, sensor_value_gy=None, sensor_value_gz=None):
        """Insert gyroscope sensor data into the sensor_giroscopio table.

        All parameters are optional; pass None to store NULLs.
        Returns a dict with id_sensor and date_uploaded.
        """
        try:
            query = """
                INSERT INTO sensor_giroscopio (
                    sensor_value_ax, sensor_value_ay, sensor_value_az,
                    sensor_value_gx, sensor_value_gy, sensor_value_gz
                ) VALUES (
                    :sensor_value_ax, :sensor_value_ay, :sensor_value_az,
                    :sensor_value_gx, :sensor_value_gy, :sensor_value_gz
                )
                RETURNING id_sensor, date_uploaded
            """

            params = {
                'sensor_value_ax': sensor_value_ax,
                'sensor_value_ay': sensor_value_ay,
                'sensor_value_az': sensor_value_az,
                'sensor_value_gx': sensor_value_gx,
                'sensor_value_gy': sensor_value_gy,
                'sensor_value_gz': sensor_value_gz,
            }

            result = self.execute_query(query, params)
            row = result.fetchone()

            if row:
                return {
                    'id_sensor': row[0],
                    'date_uploaded': row[1]
                }
            else:
                raise Exception("Failed to insert gyroscope data - no row returned")
        except Exception as e:
            logging.error(f"Error inserting gyroscope data: {e}")
            raise e
    
    def close_connection(self):
        """Close database connection"""
        if self.engine:
            self.engine.dispose()
            logging.info("Database connection closed")

# Create a global database instance
db_connection = DatabaseConnection()