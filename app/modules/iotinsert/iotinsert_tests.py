import unittest
import json

from app.modules.iotinsert.controller import IotinsertController


def test_index():
    iotinsert_controller = IotinsertController()
    result = iotinsert_controller.index()
    assert result == {'message': 'Hello, World!'}
