.. image:: https://badges.gitter.im/ffunenga/virtuallinks.svg
    :target: https://gitter.im/ffunenga/virtuallinks?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge

.. image:: https://travis-ci.org/ffunenga/virtuallinks.svg?branch=master
    :target: https://travis-ci.org/ffunenga/virtuallinks

Virtuallinks
============

    Why can't file system links occur without being registered on the file
    system?

.. code-block:: python

    import virtuallinks
    virtuallinks.link('on/a/dir/far/far/away', name='far_away_dir')
    with open('far_away_dir/file.txt', 'w') as f:
        f.write('hello world!')

*virtuallinks* simulates at least one link, without changing the file system.

Install it with:

.. code-block:: bash

    $ pip install virtuallinks

If you have any questions, then lets
`chat <https://gitter.im/ffunenga/virtuallinks>`_.

Pure Python code, 2 and 3 compatible.


Links
-----

The links implemented by *virtuallinks* can be managed by the following
methods:

* ``virtuallinks.link(destination, name=None)``
    Create a virtuallink to a destination.

    Arguments:
        - **destination** -- The final path, file or folder, to which the read/write
                       operations are performed.
        - **name** -- (optional) The identifier that will be used to route
                     operations to the destination.
                     Default value is the the current working directory
                     joined with the basename of the destination.

* ``virtuallinks.unlink(name)``
    Unlink a registered virtuallink.

    Arguments:
        - **name** -- The intended virtuallink's name that is to be
                     removed.
                     Default behavior is to remove all registered virtuallinks.

* ``virtuallinks.unlink_all()``
    Unlink all registered virtuallinks.

Monitoring callables
--------------------

*virtuallinks* works by decorating callables in the Python environment and
replacing (when appropriate) any recognized link on their inputs/outputs.
The list of typical callables that are decorated by default can be consulted
in ``virtuallinks.virtuallinks.TYPICAL``.

The callables which are decorated by *virtuallinks* can be managed by the
following methods:

* ``virtuallinks.monitor(callable_name, module=None)``
    Monitor a callable for virtuallinks routing.

    Arguments:
        - **callable_name** -- A str with the name of the callable
        - **module** -- (optional) The module in which the callable resides.
                  Default value is the builtins (or __builtin__) module.

* ``virtuallinks.monitor_typical()``
    Monitors typical main library callables for virtualinks routing.

* ``virtuallinks.unmonitor(callable_name, module=None)``
    Unmonitor a callable from previous virtuallinks routing.

    Arguments:
        - **callable_name** -- A str with the name of the callable
        - **module** -- (optional) The module in which the callable resides.
                  Default value is the builtins (or __builtin__) module.

* ``virtuallinks.unmonitor_typical()``
    Unmonitors typical callables from previous virtualinks routing.

* ``virtuallinks.unmonitor_all()``
    Unmonitor all method being monitored for virtuallink's routing.

Inspecting
----------

In order to facilitate finding out which callables are being used by a
certain block of code, *virtuallinks* provides an inspector which makes it
easy to decorate in bulk all the callables inside a module, or/and decorate
all callables in a list.

This inspector can be managed with the following methods:

* ``virtuallinks.enable_inspector(modules=None, methods=None)``
    Enable inspector to print initial entries on the modules or methods.

    Arguments:
        - **modules** -- (optional) List of modules to inspect.
                   Default value is [os, os.path]
        - **methods** -- (optional) List of (module, callable_name) tuples.
                   Default value is [(builtins, 'open')]

* ``virtuallinks.disable_inspector()``
    Disable inspector from monitoring initial entries.
