// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol"; // for brownie we need to identify this import at config file

contract FundMe{

    address public owner;

    AggregatorV3Interface public priceFeed;

    address[] public funders;

    

    //the constructor is the first thing to be executed
    constructor(address _priceFeed) public{
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }
    
    mapping(address => uint) public map;

    function fund() public payable{
        uint minimumUSD = 50 * 10**18;
        require(getConversionRate(uint(msg.value)) >= minimumUSD, "You need to donate at least $50");
        funders.push(msg.sender);
        map[msg.sender] += msg.value;
    }

    function getPrice() public view returns(uint) {
        //AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
         (
            /*uint80 roundID*/,
            int256 answer,
            /*uint startedAt*/,
            /*uint timeStamp*/,
            /*uint80 answeredInRound*/
        ) = priceFeed.latestRoundData();
        return uint(answer * 10000000000);
    }

    function getEntranceFee() public view returns (uint) { 
        uint minimumUSD = 50 * 10**18;
        uint price = uint(getPrice());
        uint precision = 1 * 10**18;
        return ((minimumUSD * precision) / price) + 1;
    }

    function getConversionRate(uint ethAmount) public view returns(uint){
        uint realPrice = (getPrice() * ethAmount / 1000000000000000000);
        return realPrice;
    }
   
    // the _ means to execute the next function
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function withdraw() public onlyOwner{ //identify the modifier
        payable(msg.sender).transfer(address(this).balance);

        for(uint i = 0; i < funders.length; i++){
            address funder = funders[i];
            map[funder] = 0;
        }

        funders = new address[](0); // clear the array
    }

}