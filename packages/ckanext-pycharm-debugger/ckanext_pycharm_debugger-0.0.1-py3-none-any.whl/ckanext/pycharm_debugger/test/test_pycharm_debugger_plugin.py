import sys
import types
import logging
from unittest import mock

from ckanext.pycharm_debugger.plugin import PycharmDebugger


def test_update_config_debug_enabled_import_failure(monkeypatch, caplog):
    caplog.set_level(logging.INFO)

    config = {
        'debug.remote': 'True',
        'debug.remote.host.ip': '127.0.0.1',
        'debug.remote.host.port': '1234',
        'debug.remote.stdout_to_server': 'True',
        'debug.remote.stderr_to_server': 'True',
        'debug.remote.suspend': 'False',
    }

    sys_path_original = list(sys.path)
    monkeypatch.setattr(sys, 'path', list(sys_path_original))

    # Mock pydevd_pycharm to simulate import failure
    mock_pydevd = types.SimpleNamespace(settrace=mock.Mock(side_effect=ConnectionRefusedError("Connection refused")))
    monkeypatch.setitem(sys.modules, 'pydevd_pycharm', mock_pydevd)

    plugin = PycharmDebugger()
    plugin.update_config(config)

    assert "pydevd_pycharm is missing" in caplog.text or \
           "Failed to connect to debug server" in caplog.text

    sys.path = sys_path_original


def test_update_config_debug_enabled_mimic_missing(monkeypatch, caplog):
    caplog.set_level(logging.INFO)

    config = {
        'debug.remote': 'True',
        'debug.remote.egg_dir': '/dummy/dir',
        'debug.remote.egg_file': 'dummy.egg',
        'debug.remote.host.ip': '127.0.0.1',
        'debug.remote.host.port': '1234',
        'debug.remote.stdout_to_server': 'True',
        'debug.remote.stderr_to_server': 'True',
        'debug.remote.suspend': 'True',
    }

    sys_path_original = list(sys.path)
    monkeypatch.setattr(sys, 'path', list(sys_path_original))

    monkeypatch.delitem(sys.modules, 'pydevd_pycharm', raising=False)

    plugin = PycharmDebugger()
    plugin.update_config(config)

    assert "pydevd_pycharm is missing" in caplog.text or \
           "Failed to connect to debug server" in caplog.text

    sys.path = sys_path_original


def test_update_config_see_manual_egg_injected_into_sys(monkeypatch, caplog):
    caplog.set_level(logging.INFO)

    config = {
        'debug.remote': 'False',
        'debug.remote.egg_dir': '/dummy/dir',
        'debug.remote.egg_file': 'dummy.egg',
        'debug.remote.host.ip': '127.0.0.1',
        'debug.remote.host.port': '1234',
        'debug.remote.stdout_to_server': 'True',
        'debug.remote.stderr_to_server': 'True',
        'debug.remote.suspend': 'True',
    }

    sys_path_original = list(sys.path)
    monkeypatch.setattr(sys, 'path', list(sys_path_original))

    plugin = PycharmDebugger()
    plugin.update_config(config)

    assert "Initiating supplied egg path: /dummy/dir  file: dummy.egg" in caplog.text
    assert '/dummy/dir/dummy.egg' in sys.path

    sys.path = sys_path_original


def test_update_config_debug_disabled(monkeypatch, caplog):
    caplog.set_level(logging.INFO)

    config = {
        'debug.remote': 'False',
    }

    sys_path_original = list(sys.path)
    monkeypatch.setattr(sys, 'path', list(sys_path_original))

    plugin = PycharmDebugger()
    plugin.update_config(config)

    assert "PyCharm Debugger not enabled" in caplog.text

    sys.path = sys_path_original


def test_update_config_debug_import_failure(monkeypatch, caplog):
    caplog.set_level(logging.INFO)

    config = {
        'debug.remote': 'True',
    }

    sys_path_original = list(sys.path)
    monkeypatch.setattr(sys, 'path', list(sys_path_original))

    # Mock pydevd_pycharm to raise ImportError when accessed
    monkeypatch.setattr('builtins.__import__', mock.Mock(side_effect=ImportError("pydevd_pycharm not found")))

    plugin = PycharmDebugger()
    plugin.update_config(config)

    assert "debug.enabled set to True, but pydevd_pycharm is missing." in caplog.text

    sys.path = sys_path_original


def test_update_config_debug_enabled_nameerror_or_importerror(monkeypatch, caplog):
    caplog.set_level(logging.WARNING)

    config = {
        'debug.remote': 'True',
        'debug.remote.host.ip': '127.0.0.1',
        'debug.remote.host.port': '1234',
        'debug.remote.stdout_to_server': 'True',
        'debug.remote.stderr_to_server': 'True',
        'debug.remote.suspend': 'True',
    }

    sys_path_original = list(sys.path)
    monkeypatch.setattr(sys, 'path', list(sys_path_original))

    # Simulate ImportError by removing the module from sys.modules
    monkeypatch.delitem(sys.modules, 'pydevd_pycharm', raising=False)

    # Mock pydevd_pycharm to raise ImportError when accessed
    monkeypatch.setattr('builtins.__import__', mock.Mock(side_effect=ConnectionRefusedError("Can't Connect")))

    plugin = PycharmDebugger()
    plugin.update_config(config)

    assert "Failed to connect to debug server; is it started?" in caplog.text

    sys.path = sys_path_original
