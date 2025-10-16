import psycopg2

def create_giroscopio_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sensor_giroscopio (
        id_sensor SERIAL PRIMARY KEY,
        sensor_value_ax FLOAT NULL,
        sensor_value_ay FLOAT NULL,
        sensor_value_az FLOAT NULL,
        sensor_value_gx FLOAT NULL,
        sensor_value_gy FLOAT NULL,
        sensor_value_gz FLOAT NULL,
        date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with connection.cursor() as cursor:
        cursor.execute(create_table_query)
    connection.commit()

def create_sensor_data_raw_table(connection):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS sensor_data_raw (
        id_sensor SERIAL PRIMARY KEY,
        type_sensor VARCHAR(50) NOT NULL,
        sensor_value FLOAT NOT NULL,
        date_uploaded TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    with connection.cursor() as cursor:
        cursor.execute(create_table_query)
    connection.commit()

def initialize_database():
    connection = None
    try:
        connection = psycopg2.connect(
            dbname="sensores",
            user="arduino_user",
            password="arduino_pass",
            host="localhost",
            port="5432"
        )
        create_giroscopio_table(connection)
        create_sensor_data_raw_table(connection)
        print("Tablas creadas correctamente.")
    except psycopg2.Error as e:
        print(f"Error en la base de datos: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        if connection:
            connection.close()

def main():
    initialize_database()
    
if __name__ == "__main__":
    main()