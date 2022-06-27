import pytest
import web3


import pytest
from web3 import Web3


@pytest.fixture
def amount_staked():
    return Web3.toWei(1, "ether")

