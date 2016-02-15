from __future__ import print_function
import os
import sys
import collections
try:
    import builtins
except:
    import __builtin__ as builtins


DEBUG = False


def set_debug(enable=True):
    """Sets the DEBUG flag inside virtuallinks.

    Arguments:
        enable -- (optional) Boolean value to be setted on the DEBUG variable.
                  Default value is True.
    """
    if enable:
        label = '\033[92m%s\033[0m' % 'Set debug:'
        print(label, enable)

    global DEBUG
    DEBUG = enable


def _str_params(args, kwds):
    args = ', '.join(repr(a) for a in args)
    kwds = ', '.join(
            ('%s=%s' % (repr(k), repr(v))) for k, v in kwds.items())
    separator = ', ' if len(args) and len(kwds) else ''
    return '(%s)' % (args + separator + kwds)


class VirtualLinker:

    def __init__(self):
        self.links = []
        self.monitored = []
        self.__inside = False

    def enter(self):
        router = None if self.__inside else self.route
        self.__inside = True
        return router

    def exit(self):
        self.__inside = False

    def route(self, path):
        try:
            abspath = os.path.abspath(path)
        except:
            return path
        else:
            for link, destination in self.links:
                if abspath.startswith(link):
                    break
            else:
                return path
            return abspath.replace(link, destination)


virtuallinker = VirtualLinker()


class Inspector:

    def __init__(self):
        self.__inside = False

    def enter(self):
        flag = not self.__inside
        self.__inside = True
        return flag

    def exit(self):
        self.__inside = False


inspector = Inspector()


class Decorator(object):

    TYPICAL_INSTALLED = True

    # This next list is where the instantiated Decorators are stored,
    # in order to allow an easy backup of their inner decorated
    # callables, when needed.
    REGISTERED = []

    # The next two namedtuples (Backup and Entry) are herein defined
    # for being used while populating the REGISTERED list above.
    Backup = collections.namedtuple(
            'Backup', ['module', 'callable_name', 'callable'])

    class Entry(collections.namedtuple('Entry', ['decorator', 'backup'])):
        __slots__ = ()
        def __repr__(self):
            _fmt = "Entry(decorator=%s, backup=(...))"
            _label = (self.decorator.inner_callable.__module__ + '.' +
                      self.decorator.inner_callable.__name__)
            return _fmt % _label

    def __init__(self, inner, is_inspected=False, is_monitored=False):
        self.inner_callable = inner
        self.is_inspected = is_inspected
        self.is_monitored = is_monitored

    def set_value(self, is_inspected=None, is_monitored=None):
        if is_inspected != None:
            self.is_inspected = is_inspected
        if is_monitored != None:
            self.is_monitored = is_monitored

    def register(self, module, name):
        assert type(name) == str

        backup = Decorator.Backup(module, name, self.inner_callable)
        entry = Decorator.Entry(self, backup)
        Decorator.REGISTERED.append(entry)

    @staticmethod
    def untouch(decorator, as_inspected, as_monitored):
        if as_inspected:
            decorator.is_inspected = False
        elif as_monitored:
            decorator.is_monitored = False

    @classmethod
    def unregister(cls, module, callable_name, as_inspected=False,
                   as_monitored=False):
        for idx, (decorator, backup) in enumerate(cls.REGISTERED):
            flags = [backup.module == module,
                     backup.callable_name == callable_name,
                     ((as_inspected and decorator.is_inspected) or
                      (as_monitored and decorator.is_monitored))]
            if all(flags):
                cls.untouch(decorator, as_inspected, as_monitored)
                break
        else:
            _err = 'Unregister failed. "%s" is not registered.'
            _label = module.__name__ + '.' + callable_name
            raise KeyError(_err % _label)

        if not (decorator.is_inspected or decorator.is_monitored):
            backup.module.__dict__[backup.callable_name] = backup.callable
            del cls.REGISTERED[idx]

    @classmethod
    def unregister_all(cls, as_inspected=False, as_monitored=False):
        """Arguments:
            type -- Any of Decorator.INSPECTED or Decorator.monitorED
        """
        new_registered= []

        while cls.REGISTERED:
            decorator, backup = entry = cls.REGISTERED.pop()

            cls.untouch(decorator, as_inspected, as_monitored)

            if decorator.is_inspected or decorator.is_monitored:
                new_registered.append(entry)
            else:
                backup.module.__dict__[backup.callable_name] = backup.callable

        cls.REGISTERED += new_registered

    def __call__(self, *args, **kwds):
        global virtuallinker
        global inspector

        assert self.is_inspected or self.is_monitored

        if self.is_inspected:
            flag = inspector.enter()
            if flag:
                fmt = '\033[91m%s %s:\033[0m'
                label = fmt % ('(inspector)', self.inner_callable.__name__)
                print(label, _str_params(args, kwds))

        if self.is_monitored:
            router = virtuallinker.enter()
            if router:
                oldargs, oldkwds = args, kwds
                args = [router(a) for a in oldargs]
                kwds = {}
                for k, v in oldkwds.items():
                    kwds[k] = router(v)
                if DEBUG:
                    fmt = '\033[94m%s:\033[0m'
                    label = fmt % (self.inner_callable.__name__)
                    ini_args = _str_params(oldargs, oldkwds)
                    end_args = _str_params(args, kwds)
                    print(label, ini_args, '->', end_args)

        rst = self.inner_callable(*args, **kwds)

        if self.is_inspected:
            if flag:
                inspector.exit()

        if self.is_monitored:
            if router:
                # Note: The returned values of the inner_callable are only
                # treated if there was not a routing substitution performed
                # upon the repective entry.
                if list(oldargs) == args and oldkwds == kwds:
                    iterables = ['tuple', 'list']
                    if rst.__class__.__name__ in iterables:
                        rst = rst.__class__(router(r) for r in rst)
                    elif rst.__class__.__name__ == 'generator':
                        rst = (router(r) for r in rst)
                    else:
                        rst = router(rst)
                virtuallinker.exit()

        return rst


def decorate(module, callable_name, inner, **kwds):
    if type(inner) == Decorator:
        inner.set_value(is_inspected=kwds.get('is_inspected'))
        inner.set_value(is_monitored=kwds.get('is_monitored'))
        decorated = inner
    else:
        decorated = Decorator(inner, **kwds)
        module.__dict__[callable_name] = decorated
        decorated.register(module, callable_name)
    return decorated


def list_registered():
    """List registered callables (either inspected or monitored).
    """
    if Decorator.REGISTERED:
        print('Registered callables:')
    for d in Decorator.REGISTERED:
        try:
            print('   ', d)
        except:
            print('FAIL')
    if Decorator.REGISTERED:
        print('[%d callables are registered]' % len(Decorator.REGISTERED))


def nregistered():
    """Count number of registered callables.
    """
    return len(Decorator.REGISTERED)


# ----------------------------------------------------------------------------

def enable_inspector(modules=None, methods=None):
    """Enable inspector to print initial entries on the modules or methods.

    Arguments:
        modules -- (optional) List of modules to inspect.
                   Default value is [os, os.path]
        methods -- (optional) List of (module, callable_name) tuples.
                   Default value is [(builtins, 'open')]
    """
    if DEBUG:
        label = '\033[92m%s\033[0m' % ('Enabling inspector:')
        print(label, 'now')

    modules = modules if modules is not None else [os, os.path]
    for module in modules:
        for callable_name, inner in module.__dict__.items():
            if any([not callable_name.islower(),
                    callable_name.startswith('_'),
                    not hasattr(inner, '__call__')]):
                continue
            decorate(module, callable_name, inner, is_inspected=True)

    methods = methods if methods is not None else [(builtins, 'open')]
    for module, callable_name in methods:
        inner = module.__dict__[callable_name]
        decorate(module, callable_name, inner, is_inspected=True)


def disable_inspector():
    """Disable inspector from monitoring initial entries.
    """
    if DEBUG:
        label = '\033[92m%s\033[0m' % ('Disabling inspector:')
        print(label, 'now')

    Decorator.unregister_all(as_inspected=True)


# ----------------------------------------------------------------------------

# CAUTION: Be carefull here. Adding new callables bellow will always be
#          easy. The real problems only appear after. If any of the following
#          entries *turns out* to be ambiguous (in any way) and a decision
#          is made to delete said entry (which will most likely happen), then
#          there's a tormenting probability that prior code depending on
#          virtuallinks might brake due to that change.
#
# The ONE NIGHT SLEEP rule:
#          If the following entries need to change, then:
#              1) sleep on it (at least one night), and
#              2) commit the change if you still feel it is the correct way to
#                 proceed.
TYPICAL = [
    ('open', builtins),
    ('chdir', os),
    ('mkdir', os),
    ('rmdir', os),
]


def ntypical():
    """Returns the number of typical main library callables defined.
    """
    return len(TYPICAL)


def unmonitor(callable_name, module=None):
    """Unmonitor a callable from previous virtuallinks routing.

    Arguments:
        callable_name -- A str with the name of the callable
        module -- (optional) The module in which the callable resides.
                  Default value is the builtins (or __builtin__) module.
    """
    assert type(callable_name) == str

    module = module if module is not None else builtins

    if DEBUG:
        label = '\033[92m%s\033[0m' % ('Unmonitoring:')
        print(label, module, callable_name)

    Decorator.unregister(module, callable_name, as_monitored=True)


def unmonitor_typical():
    """Unmonitors typical callables from previous virtualinks routing.
    """
    for module, callable_name in TYPICAL:
        unmonitor(callable_name, module)


def unmonitor_all():
    """Unmonitor all method being monitored for virtuallink's routing.
    """
    if DEBUG:
        label = '\033[92m%s\033[0m' % ('Unmonitoring:')
        print(label, 'all')

    Decorator.unregister_all(as_monitored=True)


def monitor(callable_name, module=None):
    """Monitor a callable for virtuallinks routing.

    Arguments:
        callable_name -- A str with the name of the callable
        module -- (optional) The module in which the callable resides.
                  Default value is the builtins (or __builtin__) module.
    """
    assert type(callable_name) == str

    module = module if module is not None else builtins

    if DEBUG:
        label = '\033[92m%s\033[0m' % ('monitoring:')
        print(label, module, callable_name)

    if Decorator.TYPICAL_INSTALLED:
        Decorator.unregister_all(as_monitored=True)
        Decorator.TYPICAL_INSTALLED = False

    inner = module.__dict__[callable_name]
    decorate(module, callable_name, inner, is_monitored=True)


def __monitor_typical():
    for callable_name, module in TYPICAL:
        inner = module.__dict__[callable_name]
        decorate(module, callable_name, inner, is_monitored=True)


def monitor_typical():
    """Monitors typical main library callables for virtualinks routing.
    """
    if Decorator.TYPICAL_INSTALLED:
        Decorator.unregister_all(as_monitored=True)
        Decorator.TYPICAL_INSTALLED = False
    __monitor_typical()


# ----------------------------------------------------------------------------

def link(destination, name=None):
    """Create a virtuallink to a destination.

    Arguments:
        destination -- The final path, file or folder, to which the read/write
                       operations are performed.
        name -- (optional) The identifier that will be used to route
                     operations to the destination.
                     Default value is the the current working directory
                     joined with the basename of the destination.
    """
    assert type(destination) == str
    assert name is None or type(name) == str

    if DEBUG:
        label = '\033[92m%s\033[0m' % ('New link:')
        print(label, destination, '->', name)

    abs_destination = os.path.abspath(destination)
    if name is None:
        _cwd = os.getcwd()
        _basename = os.path.basename(abs_destination)
        abs_name = os.path.join(_cwd, _basename)
    else:
        abs_name = os.path.abspath(name)

    if nregistered() == 0 and Decorator.TYPICAL_INSTALLED:
        __monitor_typical()

    virtuallinker.links = [(k, v) for k, v in virtuallinker.links
                           if k != abs_name]
    entry = (abs_name, abs_destination)
    virtuallinker.links.append(entry)


def unlink(name):
    """Unlink a registered virtuallink.

    Arguments:
        name -- The intended virtuallink's name that is to be
                     removed.
                     Default behavior is to remove all registered virtuallinks.
    """
    assert type(name) == str

    if DEBUG:
        print('\033[92m%s\033[0m' % ('Clearing link:'), name)

    abs_name = os.path.abspath(name)
    for idx, (key, _) in enumerate(virtuallinker.links):
        if key == abs_name:
            break
    else:
        _err = 'Unlink failed. Virtuallink "%s" is unknown.'
        raise KeyError(_err % name)

    del virtuallinker.links[idx]


def unlink_all():
    """Unlink all registered virtuallinks.
    """
    if DEBUG:
        print('\033[92m%s\033[0m' % ('Clearing links:'), 'all')

    del virtuallinker.links[:]


def nlinks():
    return len(virtuallinker.links)
