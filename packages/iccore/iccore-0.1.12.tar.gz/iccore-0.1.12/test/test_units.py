from iccore import units


def test_units():

    q = units.Quantity(name="vecolity", unit=units.Unit(name="metres_per_second"))

    assert q.unit.name == "metres_per_second"

    unit_collection = units.load_default_units()
    assert unit_collection
