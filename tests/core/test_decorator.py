import sys
import pytest

import core


virtuallinks = core.import_package('virtuallinks')


def foo():
    """Simple function to be used for core purposes."""
    return 10


def test_api_init():
    decorator = virtuallinks.Decorator(foo, is_inspected=True)
    assert decorator.is_inspected is True and decorator.is_monitored is False

    decorator = virtuallinks.Decorator(foo, is_monitored=True)
    assert decorator.is_inspected is False and decorator.is_monitored is True

    decorator = virtuallinks.Decorator(
            foo, is_inspected=True, is_monitored=True)
    assert decorator.is_inspected is True and decorator.is_monitored is True


def verify_transition(len_ini, len_end, inner, *args, **kwds):
    assert len(virtuallinks.Decorator.REGISTERED) == len_ini
    if len_ini != len_end:
        ini = virtuallinks.Decorator.REGISTERED[:]

    inner(*args, **kwds)

    if len_ini != len_end:
        assert ini != virtuallinks.Decorator.REGISTERED
    assert len(virtuallinks.Decorator.REGISTERED) == len_end


def test_api_register_unregister():
    decorator = virtuallinks.Decorator(foo, is_inspected=True)

    with pytest.raises(TypeError):
        decorator.register(sys.modules[__name__])

    with pytest.raises(AssertionError):
        decorator.register(sys.modules[__name__], foo)

    verify_transition(0, 1, decorator.register, sys.modules[__name__], 'foo')

    with pytest.raises(KeyError):
        decorator.unregister(sys, 'faa', as_monitored=True)

    with pytest.raises(KeyError):
        decorator.unregister(sys, 'faa', as_inspected=True)

    with pytest.raises(KeyError):
        decorator.unregister(sys, 'faa')

    with pytest.raises(KeyError):
        decorator.unregister(sys.modules[__name__], 'faa', as_monitored=True)

    with pytest.raises(KeyError):
        decorator.unregister(sys.modules[__name__], 'faa', as_inspected=True)

    with pytest.raises(KeyError):
        decorator.unregister(sys.modules[__name__], 'faa')

    with pytest.raises(KeyError):
        decorator.unregister(sys.modules[__name__], 'foo', as_monitored=True)

    with pytest.raises(KeyError):
        decorator.unregister(sys.modules[__name__], 'foo')

    verify_transition(1, 0, decorator.unregister,
                      sys.modules[__name__], 'foo', as_inspected=True)


def test_api_register_unregister_monitored_inspected():
    decorator = virtuallinks.Decorator(
            foo, is_inspected=True, is_monitored=True)

    verify_transition(0, 1, decorator.register,
                      sys.modules[__name__], 'foo')

    verify_transition(1, 1, decorator.unregister,
                      sys.modules[__name__], 'foo', as_inspected=True)

    verify_transition(1, 0, decorator.unregister,
                      sys.modules[__name__], 'foo', as_monitored=True)


def test_api_register_unregister_all_inspected():
    for idx in range(10):
        decorator = virtuallinks.Decorator(foo, is_inspected=True)
        verify_transition(0 + idx, 1 + idx, decorator.register,
                          sys.modules[__name__], 'foo%d' % idx)

    verify_transition(10, 0, decorator.unregister_all, as_inspected=True)


def test_api_register_unregister_all_monitored():
    for idx in range(10):
        decorator = virtuallinks.Decorator(foo, is_monitored=True)
        verify_transition(0 + idx, 1 + idx, decorator.register,
                          sys.modules[__name__], 'foo%d' % idx)

    verify_transition(10, 0, decorator.unregister_all, as_monitored=True)


def test_api_register_unregister_all_inspected_monitored():
    for idx in range(10):
        decorator = virtuallinks.Decorator(
                foo, is_inspected=True, is_monitored=True)
        verify_transition(0 + idx, 1 + idx, decorator.register,
                          sys.modules[__name__], 'foo%d' % idx)

    verify_transition(10, 10, decorator.unregister_all, as_monitored=True)
    verify_transition(10, 0, decorator.unregister_all, as_inspected=True)

    virtuallinks.unmonitor_all()
    virtuallinks.unlink_all()
