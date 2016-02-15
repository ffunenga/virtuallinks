import pytest
import os
import shutil

import core


virtuallinks = core.import_package('virtuallinks')


def setup_function(function):
    shutil.rmtree('temporary', ignore_errors=True)
    os.mkdir('temporary')
    os.chdir('temporary')


def teardown_function(function):
    os.chdir('..')
    shutil.rmtree('temporary', ignore_errors=True)


def test_unmonitor_fail():
    with pytest.raises(KeyError):
        virtuallinks.unmonitor('open')


def test_monitor_double_unmonitor():
    assert virtuallinks.nregistered() == 0
    virtuallinks.monitor('open')
    virtuallinks.monitor('open')
    virtuallinks.unmonitor('open')
    assert virtuallinks.nregistered() == 0


def test_monitor_unmonitor_double():
    assert virtuallinks.nregistered() == 0
    virtuallinks.monitor('open')
    assert virtuallinks.nregistered() == 1
    virtuallinks.unmonitor('open')
    assert virtuallinks.nregistered() == 0
    virtuallinks.monitor('open')
    assert virtuallinks.nregistered() == 1
    virtuallinks.unmonitor('open')
    assert virtuallinks.nregistered() == 0


def test_monitor_after_inspector(capsys):
    virtuallinks.enable_inspector()
    virtuallinks.monitor('open')
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''
    virtuallinks.unmonitor('open')
    virtuallinks.disable_inspector()


def _test_monitor_inspector_interleaved_0(capsys):
    virtuallinks.monitor('open')
    virtuallinks.enable_inspector()
    virtuallinks.unmonitor('open')
    virtuallinks.disable_inspector()
    with open('file.txt', 'w') as f:
        f.write('')
    assert os.path.exists('file.txt')
    assert os.path.isfile('file.txt')


def test_monitor_inspector_interleaved_1(capsys):
    virtuallinks.monitor('open')
    virtuallinks.enable_inspector()
    virtuallinks.unmonitor('open')
    with open('file.txt', 'w') as f:
        f.write('')
    virtuallinks.disable_inspector()
    assert os.path.exists('file.txt')
    assert os.path.isfile('file.txt')


def test_monitor_inspector_interleaved_2(capsys):
    virtuallinks.monitor('open')
    virtuallinks.enable_inspector()
    with open('file.txt', 'w') as f:
        f.write('')
    virtuallinks.unmonitor('open')
    virtuallinks.disable_inspector()
    assert os.path.exists('file.txt')
    assert os.path.isfile('file.txt')


def test_monitor_inspector_interleaved_3(capsys):
    virtuallinks.monitor('open')
    with open('file.txt', 'w') as f:
        f.write('')
    virtuallinks.enable_inspector()
    virtuallinks.unmonitor('open')
    virtuallinks.disable_inspector()
    assert os.path.exists('file.txt')
    assert os.path.isfile('file.txt')

    virtuallinks.unmonitor_all()
    virtuallinks.unlink_all()
