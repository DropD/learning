import pytest

from .train import DQoach


@pytest.fixture
def dq_coach(tmpdir):
    yield DQoach(gamma=0.1, cache_file=tmpdir / 'pytorch-gym-test.yaml')


def test_save_load(dq_coach):
    dq_coach._save_state()  # pylint:disable=protected-access
    new_coach = DQoach(cache_file=dq_coach.cache_file)
    new_coach._load_state()  # pylint:disable=protected-access
    assert new_coach.hyper_params.gamma == dq_coach.hyper_params.gamma
