import { useEthers, useTokenBalance } from "@usedapp/core"
import { Token } from "../Main"
import { formatUnits } from "@ethersproject/units"
import { BalanceMsg } from "../BalanceMsg"

export interface WalletBalanceProps {
    token: Token
}

export const WalletBalance = ({ token }: WalletBalanceProps) => {
    const { image, address, name } = token
    const { account } = useEthers()
    // const WETH2 = '0x87b1f4cf9BD63f7BBD3eE1aD04E8F52540349347'
    const tokenBalance = useTokenBalance(address, account)
    const formattedTokenBalance: number = tokenBalance ? parseFloat(formatUnits(tokenBalance, 18)) : 2
    return (<BalanceMsg
        label={`Your un-staked ${name} balance is:`}
        tokenImgSrc={image}
        amount={formattedTokenBalance} />)
}
