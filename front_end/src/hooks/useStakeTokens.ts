import { useEffect, useState } from "react"
import { useEthers, useContractFunction } from "@usedapp/core"
import { constants, utils } from "ethers"
import { Contract } from "@ethersproject/contracts"
import TokenFarm from "../chain-info/contracts/TokenFarm.json"
import ERC20 from "../chain-info/contracts/MockERC20.json"
import networkMapping from "../chain-info/deployments/map.json"

export const useStakeTokens = (tokenAddress: string) => {
    //  Address
    // abi > from token Farm
    // chianId
    const { chainId } = useEthers()
    const { abi } = TokenFarm
    //From Main >> const dappTokenAddress = chainId ? networkMapping[String(chainId)]["DappToken"][0] : constants.AddressZero
    const tokenFarmAddress = chainId ? networkMapping[String(chainId)]["TokenFarm"][0] : constants.AddressZero
    const tokenFarmInterface = new utils.Interface(abi)
    const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface)

    const erc20ABI = ERC20.abi
    const erc20Interface = new utils.Interface(erc20ABI)
    const erc20Contract = new Contract(tokenAddress, erc20Interface)


    //  1. APPROVE
    const { send: approveErc20Send, state: approveAndStakeErc20State } = useContractFunction(erc20Contract, "approve", { transactionName: "Approve ERC20 transfer", })
    // 1.a Approve:
    //  this funct will 1 approve the ERC20 -2change amount we are going to stake(setAmntToStake), 3 once txn succeed will perform stake send 
    const approveAndStake = (amount: string) => {
        setAmountToStake(amount)
        return approveErc20Send(tokenFarmAddress, amount)
    }


    // 2. STAKE
    const { send: stakeSend, state: stakeState } = useContractFunction(tokenFarmContract, "stakeTokens", { transactionName: "Stake Tokens", })
    // 2.a how much we want to stake
    const [amountToStake, setAmountToStake] = useState("0")


    // useEffect
    useEffect(() => {
        if (approveAndStakeErc20State.status === "Success") {
            // Stake function >> we need
            // 1 stake function >> stakeSend
            // 2 approve rthe amount to stake and approve the stake >> approve and stake
            stakeSend(amountToStake, tokenAddress)
        }
    }, [approveAndStakeErc20State, amountToStake, tokenAddress])

    //  Stake state
    const [state, setState] = useState(approveAndStakeErc20State)
    useEffect(() => {
        if (approveAndStakeErc20State.status === "Success") {
            setState(stakeState)
        } else {
            setState(approveAndStakeErc20State)
        }
    }, [approveAndStakeErc20State, stakeState])




    return { approveAndStake, state }
}