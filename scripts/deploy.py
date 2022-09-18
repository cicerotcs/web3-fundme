
from brownie import FundMe, MockV3Aggregator, network, config 
from scripts.helper import getAccount, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS

#from web3 import Web3

def main():
    #Arrange
    account = getAccount()
    #act
    # if we are on a persistent network like rinkeby, use the associated address, otherwise, deploy mocks
    if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"] #rinkeby MM
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address # the last address
        
    fundme = FundMe.deploy(price_feed_address, {"from": account}, publish_source=config["networks"][network.show_active()].get("verify")) # <- the address will be accessed from the constructor
    print(f"Contract deployed to  {fundme.address}")
    return fundme


