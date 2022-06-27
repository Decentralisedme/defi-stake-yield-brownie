// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

// 1. StakeTokens
// 2. unStakeTokens >> rewards to user of the platform
// 3. issueTokens
// 4. addAllowedTokens
// 5. getEthValue

contract TokenFarm is Ownable {
    //  ---- MAPPINGS / LIST
    //  mapping Token 1st-address  -> staker 2nd-address -> uint256-amount
    mapping(address => mapping(address => uint256)) public stakingBalance;
    //  Mapp token to user, so we know how many different tokens this address is staking
    mapping(address => uint256) public uniqueTokensStaked;
    // List stakers
    address[] public stakers;
    // List allowed token
    address[] public allowedTokens;
    //  Token Address >> Price Feed
    mapping(address => address) public tokenPriceFeedMapping;

    //  ----GLOBAL VARIABLES
    IERC20 public dappToken;

    constructor(address _dappTokenAddress) public {
        dappToken = IERC20(_dappTokenAddress);
    }

    function setPriceFeedContract(address _token, address _priceFeed)
        public
        onlyOwner
    {
        tokenPriceFeedMapping[_token] = _priceFeed;
    }

    // 3. issueTokens
    function issueToken() public onlyOwner {
        //  we need list of staker - above
        for (
            uint256 stakersIndex = 0;
            stakersIndex < stakers.length;
            stakersIndex++
        ) {
            //  then we can issue some token
            address recipient = stakers[stakersIndex];
            uint256 userTotalValue = getUserTotalValue(recipient);
            dappToken.transfer(recipient, userTotalValue);
            //  we are going thought the recepient and send them a token rewards >> DappT
            //  based on total vaule locked
            //  Cose we must have DappT >> we put in cunstructur DappT address
            //  we can send the rewards
            //  ===== dappToken.transfer(recepien)
        }
    }

    // Function A
    function getUserTotalValue(address _user) public view returns (uint256) {
        uint256 totalValue = 0;
        require(uniqueTokensStaked[_user] > 0, "NO tokens staked !!!");
        for (
            uint256 allowedTokenIndex = 0;
            allowedTokenIndex < allowedTokens.length;
            allowedTokenIndex++
        ) {
            totalValue =
                totalValue +
                getUserSingleTokenValue(
                    _user,
                    allowedTokens[allowedTokenIndex]
                );
        }
        return totalValue;
    }

    // Function A.1: to get a singole token value for a user- used in getUserTotalValue
    function getUserSingleTokenValue(address _user, address _token)
        public
        view
        returns (uint256)
    {
        // 1 ETH -> $2,000
        // Value -> 2000
        // 100 DAI -> 100
        // Value -> 100
        if (uniqueTokensStaked[_user] <= 0) {
            return 0;
        }
        //  WE want: Token Price * StakingBalance[_token][user]
        //  new function
        (uint256 price, uint256 decimals) = getTokenValue(_token);
        return (((stakingBalance[_token][_user] * price) / 10**decimals));
    }

    // Function A.1.1
    function getTokenValue(address _token)
        public
        view
        returns (uint256, uint256)
    {
        //  ChainLink: priceFeedAddress: map each token to priceFeed address - above
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        //  we can use it with AggregatorV3Interface
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            priceFeedAddress
        );
        (, int256 price, , , ) = priceFeed.latestRoundData();
        // we needto know decimals
        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);
    }

    // 1. stake amount and token address
    function stakeTokens(uint256 _amount, address _token) public {
        // which token is stakable
        // how much can you stake
        require(_amount > 0, "Amount must be greater then 0");
        // Create a token is allowed funct
        require(tokenIsAllowed(_token), "Token is currently not allowed!!");
        //  Now call transfer function from ERC20
        //  ERC20 has 2 tyeo of transfer: transfer and transferFrom
        //  We need abi to use the function of the token>> import IERC20
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        updateUniqueTokensStaked(msg.sender, _token);
        stakingBalance[_token][msg.sender] =
            stakingBalance[_token][msg.sender] +
            _amount;
        // Update list of stakers if new
        if (uniqueTokensStaked[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    // 2. unStakeTokens
    function unstakeTokens(address _token) public {
        uint256 balance = stakingBalance[_token][msg.sender];
        require(balance > 0, "Staking balance cannnot be zero");
        IERC20(_token).transfer(msg.sender, balance);
        stakingBalance[_token][msg.sender] = 0;
        // Vulnerable to Reentracy Attack???
        uniqueTokensStaked[msg.sender] = uniqueTokensStaked[msg.sender] - 1;
        //  We should update the Staker list- skipped for now- but things will stiil work coseissue token check balance
    }

    function updateUniqueTokensStaked(address _user, address _token) internal {
        if (stakingBalance[_token][_user] <= 0) {
            //  uniqueTokStkd is a mapping - above
            uniqueTokensStaked[_user] = uniqueTokensStaked[_user] + 1;
        }
    }

    // 4. addAllowTokens but only from the owner
    function addAllowedTokens(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    function tokenIsAllowed(address _token) public returns (bool) {
        //  we need a list of allowedTokens - above
        for (
            uint256 allowedTokensIndex = 0;
            allowedTokensIndex < allowedTokens.length;
            allowedTokensIndex++
        ) {
            if (allowedTokens[allowedTokensIndex] == _token) {
                return true;
            }
        }
        return false;
    }
}
