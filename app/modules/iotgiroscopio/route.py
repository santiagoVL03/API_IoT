from flask import Blueprint, make_response, jsonify, request
from .controller import IotgiroscopioController


iotgiroscopio_bp = Blueprint('iotgiroscopio', __name__)
iotgiroscopio_controller = IotgiroscopioController()
@iotgiroscopio_bp.route('/', methods=['GET'])
def index():
    """Insert gyroscope sensor data.
    ---
    tags:
      - Gyroscope API
    parameters:
      - name: ax
        in: query
        type: number
        required: false
        description: Acceleration X
      - name: ay
        in: query
        type: number
        required: false
        description: Acceleration Y
      - name: az
        in: query
        type: number
        required: false
        description: Acceleration Z
      - name: gx
        in: query
        type: number
        required: false
        description: Gyroscope X
      - name: gy
        in: query
        type: number
        required: false
        description: Gyroscope Y
      - name: gz
        in: query
        type: number
        required: false
        description: Gyroscope Z
    responses:
      200:
        description: Insert result
    """
    # Read query params; treat missing or literal 'NULL'/'null' as None
    def parse_float(val):
        if val is None:
            return None
        if isinstance(val, str) and val.strip().lower() in ('null', 'none', ''):
            return None
        try:
            return float(val)
        except Exception:
            return None

    ax = parse_float(request.args.get('ax'))
    ay = parse_float(request.args.get('ay'))
    az = parse_float(request.args.get('az'))
    gx = parse_float(request.args.get('gx'))
    gy = parse_float(request.args.get('gy'))
    gz = parse_float(request.args.get('gz'))

    result = iotgiroscopio_controller.insert_giroscopio(ax, ay, az, gx, gy, gz)
    status_code = 200 if result.get('success', True) else 400
    return make_response(jsonify(data=result), status_code)
      
@iotgiroscopio_bp.route('/iotshow', methods=['GET'])
def show_index():
    """Show index message."""
    result = iotgiroscopio_controller.show_last_data()
    return make_response(jsonify(data=result), 200)
