/* eslint-disable spaced-comment */
/// <reference types="react-scripts" />
import { useEthers } from "@usedapp/core"
import helperConfig from "../helper-config.json"
import networkMapping from "../chain-info/deployments/map.json"
import { constants } from "ethers"
import brownieConfig from "../brownie-config.json"
import dapp from "../dapp.png"
import eth from "../eth.png"
import dai from "../dai.png"
import { YourWallet } from "./yourWallet"
import { makeStyles } from "@material-ui/core"
import { text } from "node:stream/consumers"

//  we creating a new type called token:
export type Token = {
    image: string
    address: string
    name: string
}

const useStlyles = makeStyles((theme) => ({
    title: {
        color: theme.palette.common.white,
        textAlign: "center",
        padding: theme.spacing(4)


    }
})

)

export const Main = () => {
    // Show token values from wallet
    // Get address of tokens
    // Get balance of the wallet
    //  We need to grab info from brownie:
    //  - brownie-config
    //  - build folder >>dapp token/mocks addresses
    const classes = useStlyles()
    const { chainId, error } = useEthers()
    // but we have network name, not the id
    //  we make a file with mapping name >> id: import helper-config
    // So if chian Id (?) exsists we take it
    const networkName = chainId ? helperConfig[chainId] : "dev"
    console.log(chainId)
    console.log(networkName)
    //  Addresses from map.json
    const dappTokenAddress = chainId ? networkMapping[String(chainId)]["DappToken"][0] : constants.AddressZero
    console.log(dappTokenAddress)
    // Address from brownie_config.json
    const wethTokenAddress = chainId ? brownieConfig["networks"][networkName]["weth_token"] : constants.AddressZero
    console.log(wethTokenAddress)
    const fauTokenAddress = chainId ? brownieConfig["networks"][networkName]["fau_token"] : constants.AddressZero

    const supportedTokens: Array<Token> = [
        {
            image: dapp,
            address: dappTokenAddress,
            name: "DAPP"
        },
        {
            image: eth,
            address: wethTokenAddress,
            name: "WETH"
        },
        {
            image: dai,
            address: fauTokenAddress,
            name: "DAI"
        }
    ]
    return (<>
        <h2 className={classes.title}>Dapp Token App</h2 >
        <YourWallet supportedTokens={supportedTokens} />
    </>
    )
}