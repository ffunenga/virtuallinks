import core


virtuallinks = core.import_package('virtuallinks')


# set_debug

def test_set_debug(capsys):
    virtuallinks.set_debug(True)
    out, _ = capsys.readouterr()
    assert 'Set debug' in out

    virtuallinks.set_debug(False)
    out, _ = capsys.readouterr()
    assert '' in out


# link, unlink, unlink_all

def test_link_unlink_debug_on(capsys):
    virtuallinks.set_debug(True)

    virtuallinks.link('/destination/path', '/link/name')
    out, _ = capsys.readouterr()
    assert 'New link' in out

    virtuallinks.unlink('/link/name')
    out, _ = capsys.readouterr()
    assert 'Clearing link' in out

    virtuallinks.set_debug(False)


def test_link_unlink_debug_off(capsys):
    virtuallinks.set_debug(False)

    virtuallinks.link('/destination/path', '/link/name')
    out, _ = capsys.readouterr()
    assert '' in out

    virtuallinks.unlink('/link/name')
    out, _ = capsys.readouterr()
    assert '' in out


def test_link_unlink_all_debug_on(capsys):
    virtuallinks.set_debug(True)

    virtuallinks.link('/destination/path', '/link/name')
    out, _ = capsys.readouterr()
    assert 'New link' in out

    virtuallinks.unlink_all()
    out, _ = capsys.readouterr()
    assert 'Clearing links' in out

    virtuallinks.set_debug(False)


def test_link_unlink_all_debug_off(capsys):
    virtuallinks.set_debug(False)

    virtuallinks.link('/destination/path', '/link/name')
    out, _ = capsys.readouterr()
    assert '' in out

    virtuallinks.unlink_all()
    out, _ = capsys.readouterr()
    assert '' in out


# monitor, unmonitor, unmonitor_all

def test_unmonitor_debug_on(capsys):
    virtuallinks.set_debug(True)

    virtuallinks.monitor('open')
    out, _ = capsys.readouterr()
    assert 'monitoring' in out

    virtuallinks.unmonitor('open')
    out, _ = capsys.readouterr()
    assert 'Unmonitoring' in out

    virtuallinks.set_debug(False)


def test_unmonitor_debug_off(capsys):
    virtuallinks.set_debug(False)

    virtuallinks.monitor('open')
    out, _ = capsys.readouterr()
    assert '' in out

    virtuallinks.unmonitor('open')
    out, _ = capsys.readouterr()
    assert '' in out


def test_unmonitor_all_debug_on(capsys):
    virtuallinks.set_debug(True)

    virtuallinks.monitor('open')
    out, _ = capsys.readouterr()
    assert 'monitoring' in out

    virtuallinks.unmonitor_all()
    out, _ = capsys.readouterr()
    assert 'Unmonitoring' in out
    assert 'all' in out

    virtuallinks.set_debug(False)


def test_unmonitor_all_debug_off(capsys):
    virtuallinks.set_debug(False)

    virtuallinks.monitor('open')
    out, _ = capsys.readouterr()
    assert '' in out

    virtuallinks.unmonitor_all()
    out, _ = capsys.readouterr()
    assert '' in out


# enable_inspector, disable_inspector

def test_inspector_debug_on(capsys):
    virtuallinks.set_debug(True)

    virtuallinks.enable_inspector()
    out, err = capsys.readouterr()
    assert 'Enabling inspector' in out

    virtuallinks.disable_inspector()
    out, err = capsys.readouterr()
    assert 'Disabling inspector' in out

    virtuallinks.set_debug(False)


def test_inspector_debug_off(capsys):
    virtuallinks.set_debug(False)

    virtuallinks.enable_inspector()
    out, err = capsys.readouterr()
    assert '' in out

    virtuallinks.disable_inspector()
    out, err = capsys.readouterr()
    assert '' in out

    virtuallinks.unmonitor_all()
    virtuallinks.unlink_all()
