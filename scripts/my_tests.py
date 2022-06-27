from brownie import network
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from scripts.deploy import deploy_token_farm_and_DappToken
import pytest


def test_set_price_feed_contract():
    # Arrange test
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for LOCAL testing")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_DappToken()
    #  Act
    price_feed_address = get_contract("eth_usd_price_feed")
    #  - note: setPrFedCnt 2nd parameter is declared as address (address _priceFeed) >> wen get contract no need to say address here - brownie knows
    token_farm.setPriceFeedContract(
        dapp_token.address, price_feed_address, {"from": account}
    )
    #  Assert
    print(f"1- Dapp Token Address: {dapp_token.address}")
    print(f"2- Price Feed Address eth: {price_feed_address.address}")
    print(f"3- Price Feed Mapping: {token_farm.tokenPriceFeedMapping}")


def main():
    test_set_price_feed_contract()
