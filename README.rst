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

If you have any questions, then lets
`chat <https://gitter.im/ffunenga/virtuallinks>`_.

Pure Python code, 2 and 3 compatible.
