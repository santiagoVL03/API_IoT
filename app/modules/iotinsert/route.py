from flask import Blueprint, make_response, jsonify, request
from .controller import IotinsertController

iotinsert_bp = Blueprint('iotinsert', __name__)
iotinsert_controller = IotinsertController()

@iotinsert_bp.route('/', methods=['GET'])
def index():
  """ Example endpoint with sensor input.
  ---
  tags:
    - Example API
  parameters:
    - name: type_sensor
      in: query
      type: string
      required: true
      description: The type of the sensor
    - name: sensor_value
      in: query
      type: string
      required: true
      description: The value of the sensor
  responses:
    200:
      description: A response with the processed sensor data
      schema:
        type: object
        properties:
          data:
            type: object
            properties:
              message:
                type: string
                example: "Processed sensor data successfully!"
              success:
                type: boolean
                example: true
              data:
                type: object
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
  type_sensor = request.args.get('type_sensor')
  sensor_value = request.args.get('sensor_value')
  result = iotinsert_controller.process_sensor_data(type_sensor, sensor_value)
  
  # Return appropriate HTTP status code based on success
  status_code = 200 if result.get('success', True) else 400
  return make_response(jsonify(data=result), status_code)