import create_cw_event as cw
from config import config
import pytest

config.username = 'ethatest@gmail.com'
@pytest.mark.int
def test_create_event():
    response = cw.build_cloudwatch_event('test')
    assert response is not None

@pytest.mark.int
def test_create_event_target():
    response = cw.build_cloudwatch_event_target('test')
    assert response is not None


@pytest.mark.int
def test_enable_event():
    response = cw.enable_cloudwatch_event('test')
    assert response is not None

@pytest.mark.int
def test_disable_event():
    response = cw.disable_cloudwatch_event('test')
    assert response is not None

@pytest.mark.int
def test_remove_target():
    response = cw.delete_event_rule_targets('test')
    assert response is not None

@pytest.mark.int
def test_delete_event():
    response = cw.delete_event_rule('test')
    assert response is not None

