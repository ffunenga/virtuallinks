from __future__ import print_function
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


def test_inspector_pass_repeated_modules():
    assert virtuallinks.nregistered() == 0

    virtuallinks.enable_inspector()
    n = virtuallinks.nregistered()
    assert n > 0

    virtuallinks.enable_inspector()
    assert n == virtuallinks.nregistered()

    virtuallinks.disable_inspector()
    assert virtuallinks.nregistered() == 0


def test_inspector_pass_repeated_methods():
    virtuallinks.enable_inspector()
    n = virtuallinks.nregistered()

    virtuallinks.enable_inspector(modules=[])
    assert n == virtuallinks.nregistered()

    virtuallinks.disable_inspector()
    assert virtuallinks.nregistered() == 0


def test_inspector_run_abspath(capsys):
    virtuallinks.enable_inspector()

    os.path.abspath(__file__)
    out, err = capsys.readouterr()
    assert '(inspector)' in out
    assert 'abspath' in out

    virtuallinks.disable_inspector()
    out, err = capsys.readouterr()
    assert out == ''
    assert err == ''


def test_inspector_run_abspath_after(capsys):
    virtuallinks.enable_inspector()
    virtuallinks.disable_inspector()

    os.path.abspath(__file__)
    out, err = capsys.readouterr()
    assert out == ''


def test_inspector_run_open(capsys):
    virtuallinks.enable_inspector()

    with open('file.txt', 'w') as f:
        f.write('')
    out, err = capsys.readouterr()
    assert '(inspector)' in out
    assert 'open' in out
    assert "('file.txt', 'w')" in out

    virtuallinks.disable_inspector()

    virtuallinks.unmonitor_all()
    virtuallinks.unlink_all()
