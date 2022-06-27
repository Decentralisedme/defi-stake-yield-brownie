import React from 'react'
import { ChainId, DAppProvider, Config, Kovan } from "@usedapp/core"
import { Header } from "./components/Header"
import { Container } from "@material-ui/core"
import { Main } from "./components/Main"
import { getDefaultProvider } from 'ethers'

// const config: Config = {
//     networks: [Kovan]
// }

const config: Config = {
    readOnlyChainId: Kovan.chainId,
    readOnlyUrls: {
        [Kovan.chainId]: getDefaultProvider('kovan')

    },
    notifications: {
        expirationPeriod: 1000,
        checkInterval: 1000,
    }
}

function App() {
    return (
        <DAppProvider config={config}>
            <Header />
            <Container maxWidth="md">
                <div> Test Network only: Kovan </div>
                <div> Repository: https://github.com/Decentralisedme/defi-stake-yield-brownie  </div>
                <div> Thanks To Patrick Collins @ Alpha Chain </div>
                <div className="App">
                    <Main />
                </div>
            </Container>
        </DAppProvider >
    )
}

export default App;