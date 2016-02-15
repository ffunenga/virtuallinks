import os
import core


virtuallinks = core.import_package('virtuallinks')


def test_autoinstall_and_refrain():
    assert virtuallinks.nlinks() == 0

    assert virtuallinks.nregistered() == 0

    virtuallinks.link('destination', name='link_to_dest')

    assert virtuallinks.nregistered() == virtuallinks.ntypical()

    virtuallinks.monitor('open')

    assert virtuallinks.nregistered() == 1

    virtuallinks.unlink_all()
    virtuallinks.unmonitor_all()


def test_auto_avoid_install():
    assert virtuallinks.nlinks() == 0

    assert virtuallinks.nregistered() == 0

    virtuallinks.monitor('open')

    assert virtuallinks.nregistered() == 1

    virtuallinks.link('destination', name='link_to_dest')

    assert virtuallinks.nregistered() == 1

    virtuallinks.unlink('link_to_dest')

    assert virtuallinks.nregistered() == 1

    virtuallinks.unlink_all()
    virtuallinks.unmonitor_all()


def test_monitor_typical_monitor():
    assert virtuallinks.nlinks() == 0

    assert virtuallinks.nregistered() == 0

    virtuallinks.monitor_typical()

    assert virtuallinks.nregistered() == virtuallinks.ntypical()

    virtuallinks.link('destination', name='link_to_dest')

    assert virtuallinks.nregistered() == virtuallinks.ntypical()

    virtuallinks.monitor('chown', os)  # this is just an example

    assert virtuallinks.nregistered() == (virtuallinks.ntypical() + 1)

    virtuallinks.unlink_all()
    virtuallinks.unmonitor_all()


def test_monitor_monitor_typical():
    assert virtuallinks.nlinks() == 0

    assert virtuallinks.nregistered() == 0

    virtuallinks.monitor('chown', os)  # this is just an example

    assert virtuallinks.nregistered() == 1

    virtuallinks.link('destination', name='link_to_dest')

    assert virtuallinks.nregistered() == 1

    virtuallinks.monitor_typical()

    assert virtuallinks.nregistered() == (virtuallinks.ntypical() + 1)

    virtuallinks.unlink_all()
    virtuallinks.unmonitor_all()
