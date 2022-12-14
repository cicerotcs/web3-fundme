from brownie import FundMe

from scripts.helper import getAccount

def fund():
    fund_me = FundMe[-1]
    account = getAccount()
    entrance_fee = fund_me.getEntranceFee()
    fund_me.fund({"from": account, "value": entrance_fee})

def withdraw():
    fund_me = FundMe[-1]
    account = getAccount()
    fund_me.withdraw({"from": account})

def main():
    fund()
    withdraw()
    