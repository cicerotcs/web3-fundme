from brownie import network, accounts
import pytest

from scripts.helper import LOCAL_BLOCKCHAIN_ENVIRONMENTS, getAccount

from scripts.deploy import main

def test_fund():
    account = getAccount()
    fund_me = main()
    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.map(account.address) == entrance_fee
    tx2 = fund_me.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me.map(account.address) == 0

# def test_only_owner_can_withdraw():
#     if(network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS):
#         pytest.skip("Only local testing...")
#     another_account = accounts.add()
#     fund_me = main()
#     fund_me.withdraw({"from": another_account})
