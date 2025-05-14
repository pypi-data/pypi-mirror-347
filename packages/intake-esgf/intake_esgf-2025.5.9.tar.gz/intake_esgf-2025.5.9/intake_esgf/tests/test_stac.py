"""
from intake_esgf.core import STACESGFIndex


def test_search():
    index = STACESGFIndex()
    df = index.search(
        experiment_id="historical",
        source_id=["CESM2", "CanESM5"],
        frequency="mon",
    )
    assert len(df) == 28
"""
