import shiftplanner.planner as p


def test_days_in_a_feburary():
    assert len(p.days_in_month(2021, 2)) == 28

def test_days_in_a_march():
    assert len(p.days_in_month(2021, 3)) == 31