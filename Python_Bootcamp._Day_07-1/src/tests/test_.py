import sys

sys.path.append('../internal')

from vkt import VKTest
from input import InputData
from validation import validate_data
from unittest.mock import patch, MagicMock

import pytest
import json

@pytest.fixture
def vk_test():
    return VKTest("questions.json")

def test_get_questions(vk_test):
    vk_test.get_questions()
    assert vk_test.questions is not None
    assert len(vk_test.questions) > 0

def test_respiration_valid_input(vk_test, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '15')
    vk_test.input_data.update()
    assert vk_test.input_data.respiration == 15

def test_respiration_invalid_low_input(vk_test, monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: '11')
    vk_test.input_data.update()
    assert vk_test.input_data.blushing_level == 11

def test_respiration_invalid_high_input(vk_test, monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: '17')
    vk_test.input_data.update()
    assert vk_test.input_data.heart_rate == 17

def test_input_data_incorrect_respiration():
    input_data = InputData()
    input_data.respiration = 20
    assert input_data.check() == False

def test_input_data_incorrect_heart_rate():
    input_data = InputData()
    input_data.respiration = 13
    input_data.heart_rate = 50
    assert input_data.check() == False

def test_input_data_incorrect_blushing_level():
    input_data = InputData()
    input_data.respiration = 13
    input_data.heart_rate = 63
    input_data.blushing_level = 7
    assert input_data.check() == False

def test_input_data_incorrect_pupillary_dilation():
    input_data = InputData()
    input_data.respiration = 13
    input_data.heart_rate = 1
    input_data.blushing_level = 2
    input_data.pupillary_dilation = 7
    assert input_data.check() == False

def test_input_data_correct():
    input_data = InputData()
    input_data.respiration = 14
    input_data.heart_rate = 70
    input_data.blushing_level = 2
    input_data.pupillary_dilation = 4
    assert input_data.check() == True

def test_input_data_with_invalid_input_1(monkeypatch):
    input_data = InputData()
    with pytest.raises(ValueError):
        monkeypatch.setattr('builtins.input', lambda _: '11.5')
        input_data.update()


def test_input_data_with_invalid_input_2(monkeypatch):
    input_data = InputData()
    with pytest.raises(ValueError):
        monkeypatch.setattr('builtins.input', lambda _: 'abc')
        input_data.update()

def test_get_questions_found():
    vktest = VKTest("questions.json")
    vktest.get_questions()
    assert len(vktest.questions) == 2
