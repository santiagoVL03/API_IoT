from flask import Blueprint, make_response, jsonify, request
from .controller import IothumedadController


iothumedad_bp = Blueprint('iothumedad', __name__)
iothumedad_controller = IothumedadController()

@iothumedad_bp.route('/', methods=['GET'])
def index():
    """ Example endpoint with simple greeting.
    ---
    tags:
      - Example API
    responses:
      200:
        description: A simple greeting
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                message:
                  type: string
                  example: "Hello World!"
    """
    result=iothumedad_controller.index()
    return make_response(jsonify(data=result))

@iothumedad_bp.route('/insert', methods=['GET'])
def insert():
    """ Insert humidity sensor data endpoint.
    ---
    tags:
      - Humidity Sensor API
    parameters:
      - name: sensor_value_humedad
        in: query
        type: number
        required: true
        description: The humidity value from the sensor
      - name: sensor_value_temperatura
        in: query
        type: number
        required: true
        description: The temperature value from the sensor
    responses:
      200:
        description: Successfully inserted humidity sensor data
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                message:
                  type: string
                  example: "Humidity sensor data processed and saved successfully!"
                success:
                  type: boolean
                  example: true
                data:
                  type: object
                  properties:
                    id_sensor:
                      type: integer
                      example: 1
                    sensor_value_humedad:
                      type: number
                      example: 65.5
                    sensor_value_temperatura:
                      type: number
                      example: 22.3
                    date_uploaded:
                      type: string
                      example: "2025-12-05T10:30:00"
      400:
        description: Bad request - missing or invalid parameters
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                error:
                  type: string
                success:
                  type: boolean
                  example: false
    """
    sensor_value_humedad = request.args.get('sensor_value_humedad')
    sensor_value_temperatura = request.args.get('sensor_value_temperatura')
    result = iothumedad_controller.insert_humedad_data(sensor_value_humedad, sensor_value_temperatura)
    
    # Return appropriate HTTP status code based on success
    status_code = 200 if result.get('success', True) else 400
    return make_response(jsonify(data=result), status_code)

      