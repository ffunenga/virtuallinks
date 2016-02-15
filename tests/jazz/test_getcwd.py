import jazz
import os


virtuallinks = jazz.import_package('virtuallinks')


def test_getcwd():
    virtuallinks.monitor('getcwd', os)

    virtuallinks.link('/home', name='.')

    path = os.getcwd()
    assert path == '/home'

    virtuallinks.unlink_all()
    virtuallinks.link('/future', name='.')

    path = os.getcwd()
    assert path == '/future'

    virtuallinks.unmonitor_all()
    virtuallinks.unlink_all()
