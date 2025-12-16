import unittest
import json

from app.modules.iothumedad.controller import IothumedadController


def test_index():
    iothumedad_controller = IothumedadController()
    result = iothumedad_controller.index()
    assert result == {'message': 'Hello, World!'}
