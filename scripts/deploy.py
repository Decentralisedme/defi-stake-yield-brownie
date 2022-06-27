import shutil
from scripts.helpful_scripts import get_account, get_contract
from brownie import DappToken, TokenFarm, network, config
from web3 import Web3
import yaml
import json
import os

KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_token_farm_and_DappToken(front_end_update=False):
    account = get_account()
    dapp_token = DappToken.deploy({"from": account})
    token_farm = TokenFarm.deploy(
        dapp_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    #  we need to send all the Dapp tokens to the TokenFarm contract
    tx = dapp_token.transfer(
        token_farm.address, dapp_token.totalSupply() - KEPT_BALANCE, {"from": account}
    )
    tx.wait(2)
    # to stake we need to: Approve the spending and then the Price Feed
    # we allow-for now- 3 tokens
    # dapp_token, weth_token, fau_token (DAI - from erc20faucet.com)
    # We also want to deploy mocks to test localy
    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")
    dict_of_allowed_tokens = {
        dapp_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }
    add_allowed_token(token_farm, dict_of_allowed_tokens, account)
    if front_end_update:
        update_front_end()
    return token_farm, dapp_token


def add_allowed_token(token_farm, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = token_farm.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = token_farm.setPriceFeedContract(
            token.address, dict_of_allowed_tokens[token], {"from": account}
        )
        set_tx.wait(2)
    return token_farm


def update_front_end():
    #  we need this cose we do not have set contract- they change anytime we redeploy
    #  in real workd they are aset we can just put them in the Front End repository
    #  Build Folder
    copy_folders_to_fron_end("./build", "./front_end/src/chain-info")
    # Brownie-config: this needs to be send injson format>> we need to convert the files
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        with open("./front_end/src/brownie-config.json", "w") as brownie_config_json:
            #  dump the dictionary in this jsomn file
            json.dump(config_dict, brownie_config_json)
    print("Front End updated!!!")


#  the following funtion is moving flolders >> (source folder, destination folder)
def copy_folders_to_fron_end(src, dest):
    # we need to check if dest ecsxist, and if yes>> remove it
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)

    pass


def main():
    deploy_token_farm_and_DappToken(front_end_update=True)
