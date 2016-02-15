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


def test_unlink_fail():
    with pytest.raises(KeyError):
        virtuallinks.unlink('/hello/world/error')


def test_link_unlink():
    virtuallinks.link('/hello/world/error', name='key')
    assert virtuallinks.nlinks() == 1

    virtuallinks.unlink(name='key')
    assert virtuallinks.nlinks() == 0


def test_basic_txtfile_link():
    with open('destination.txt', 'w') as f:
        f.write('')

    virtuallinks.monitor('open')
    virtuallinks.link('destination.txt', name='link_to_dest.txt')

    with open('link_to_dest.txt', 'w') as f:
        f.write('hello')

    virtuallinks.unlink(name='link_to_dest.txt')
    assert virtuallinks.nlinks() == 0

    virtuallinks.unmonitor('open')
    assert virtuallinks.nregistered() == 0

    assert not os.path.exists('link_to_dest.txt')

    assert os.path.exists('destination.txt')
    assert os.path.isfile('destination.txt')
    with open('destination.txt') as f:
        assert f.read().strip() == 'hello'


def test_dir_open_txtfile_link():
    os.mkdir('destination')
    path = os.path.join('destination', 'readme.txt')
    with open(path, 'w') as f:
        f.write('it works!')

    virtuallinks.monitor('open')
    virtuallinks.link('destination', name='link_to_dest')

    path = os.path.join('link_to_dest', 'readme.txt')
    with open(path) as f:
        assert f.read().strip() == 'it works!'

    path = os.path.join('link_to_dest', 'new_file.txt')
    with open(path, 'w') as f:
        f.write('helloworld')

    virtuallinks.unmonitor('open')
    assert virtuallinks.nregistered() == 0

    virtuallinks.unlink(name='link_to_dest')
    assert virtuallinks.nlinks() == 0

    path = os.path.join('link_to_dest', 'new_file.txt')
    assert not os.path.exists(path)

    path = os.path.join('destination', 'new_file.txt')
    assert os.path.exists(path)
    assert os.path.isfile(path)
    with open(path) as f:
        assert f.read().strip() == 'helloworld'


def test_dir_move_into_link():
    os.mkdir('destination')
    rootpath = os.path.abspath('.')
    inpath = os.path.abspath('destination')

    virtuallinks.monitor('chdir', os)
    virtuallinks.link('destination', name='link_to_dest')

    os.chdir('link_to_dest')
    assert os.getcwd() == inpath
    os.chdir('..')
    assert os.getcwd() == rootpath

    virtuallinks.unmonitor('chdir', os)
    assert virtuallinks.nregistered() == 0

    virtuallinks.unlink(name='link_to_dest')
    assert virtuallinks.nlinks() == 0

    virtuallinks.unmonitor_all()
    virtuallinks.unlink_all()
