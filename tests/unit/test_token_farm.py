from brownie import network, exceptions
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    INITIAL_VALUE,
    get_account,
    get_contract,
)
from scripts.deploy import deploy_token_farm_and_DappToken
import pytest

# 1. Test the set price Feed contract
def test_set_price_feed_contract():
    # Arrange test
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for LOCAL testing")
    account = get_account()
    non_owner = get_account(index=1)
    token_farm, dapp_token = deploy_token_farm_and_DappToken()
    #  Act
    price_feed_address = get_contract("dai_usd_price_feed")
    #  - note: setPrFedCnt 2nd parameter is declared as address (address _priceFeed) >> wen get contract no need to say address here - brownie knows
    token_farm.setPriceFeedContract(
        dapp_token.address, price_feed_address, {"from": account}
    )
    #  Assert
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == price_feed_address
    # Assert non owner CANNOT call the function
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(
            dapp_token.address, price_feed_address, {"from": account}
        )


# We will use amount often: we define it in conf ..
# 2. Test Staking Tokens
def test_stake_tokens(amount_staked):
    # Arrange test
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for LOCAL testing")
    account = get_account()
    token_farm, dapp_token = deploy_token_farm_and_DappToken()
    # Act: send token to token Farm
    #  1. Approve
    dapp_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, dapp_token.address, {"from": account})
    # Assert
    # We use the mapping staking balance which mapps 3 elemnts: token addss + account addss + amount
    assert (
        token_farm.stakingBalance(dapp_token.address, account.address) == amount_staked
    )
    """
    In addition from the function we have
    // Update list of stakers if new
        if (uniqueTokensStaked[msg.sender] == 1) {
            stakers.push(msg.sender);"""
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address
    #  We return so we can use it in other functions
    return token_farm, dapp_token


# 3. Test Issue Token - but we need to have token staked before we can issue them
def test_issue_tokens(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for LOCAL testing")
    account = get_account()
    #  here we can use the RETURN from test_stake_tokens
    token_farm, dapp_token = test_stake_tokens(amount_staked)
    starting_balance = dapp_token.balanceOf(account.address)
    # Act
    token_farm.issueToken({"from": account})
    # Assert
    assert dapp_token.balanceOf(account.address) == starting_balance + INITIAL_VALUE
