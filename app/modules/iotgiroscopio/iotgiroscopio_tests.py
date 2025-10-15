import unittest
import json

from app.modules.iotgiroscopio.controller import IotgiroscopioController


def test_index():
    iotgiroscopio_controller = IotgiroscopioController()
    result = iotgiroscopio_controller.index()
    assert result == {'message': 'Hello, World!'}
