import jazz


virtuallinks = jazz.import_package('virtuallinks')


def test_generator():
    virtuallinks.monitor('generate_numbers', jazz)
    numbers = jazz.generate_numbers()
    assert numbers.__class__.__name__ == 'generator'
    assert list(numbers) == list(range(10))

    virtuallinks.unmonitor_all()
    virtuallinks.unlink_all()
