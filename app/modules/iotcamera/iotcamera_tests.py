import unittest
import json

from app.modules.iotcamera.controller import IotcameraController


def test_index():
    iotcamera_controller = IotcameraController()
    result = iotcamera_controller.index()
    assert result == {'message': 'Hello, World!'}
