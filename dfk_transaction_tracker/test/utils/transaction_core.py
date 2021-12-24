from web3 import Web3
from utils import utils

from rich.console import Console
console = Console()

w3 =  Web3(Web3.HTTPProvider('https://rpc.s0.t.hmny.io'))

event_hex = {
        'Transfer': '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
        'Withdrawal': '0x7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65'
        }

ETH = "ONE"

def get_Transfers(transaction_receipt,main_address,verbose=False):
    net_transactions = {}
    for log in transaction_receipt['logs']:
        address = log['address']
        data = log['data']
        func_hex = log['topics'][0].hex()
        if func_hex == event_hex['Transfer']:
            # Determine +/- of the transaction
            _from = '0x'+log['topics'][1].hex()[-40:]
            _to = '0x'+log['topics'][2].hex()[-40:]
            if _from.lower() == main_address.lower():
                sign = -1
            elif _to.lower() == main_address.lower():
                sign = 1
            else:
                continue
            # Get transfer amount
            try:
                amount = int(data,16)
            except:
                console.print(f"[bold red] WARNING[/]: (Transfer amount) {data}")
                continue
            if address not in net_transactions:
                net_transactions[address] = sign * amount
            else:
                net_transactions[address] += sign * amount

            #if verbose:
            #    print(f"{from_mapped} > {to_mapped} || {sign*amount} ({address_mapped})")
    
    return net_transactions

def swapExactTokensForETH(net_transactions,transaction_receipt):
    log = transaction_receipt['logs'][-1]
    func_hex = log['topics'][0].hex()
    data = log['data']
    assert func_hex == event_hex['Withdrawal']
    # Get transfer amount
    try:
        amount = int(data,16)
    except:
        console.print(f"[bold red] WARNING[/]: (Transfer amount) {data}")
    if ETH not in net_transactions:
        net_transactions[ETH] = amount
    else:
        net_transactions[ETH] += amount

    return net_transactions
    
def swapETHForExactTokens(net_transactions,amount):
    if ETH not in net_transactions:
        net_transactions[ETH] = -1 * amount
    else:
        net_transactions[ETH] -= amount

    return net_transactions

"""
Move to utils/hero.py
"""
def _add_hero(hero_log,transaction_data,tx_hash,_type):

    if _type == 'summonCrystal':
        _id = transaction_data['HeroSummoningUpgradeable.json']['event']['CrystalSummoned'][1]['crystalId'][0]
        hero_log[f"Crystal_{_id}"] = tx_hash

    if _type == 'bid':
        _id = transaction_data['SaleAuction.json']['event']['AuctionSuccessful'][0]['tokenId'][0]
        hero_log[f"Hero_{_id}"] = tx_hash

    return hero_log

def add_hero(hero_log,transaction_data,tx_hash,_type):
    return _add_hero(hero_log,transaction_data,tx_hash,_type)

#abi = ABIParser('contracts/abi/IUniswapV2Pair.json').load_json()
#jewel_lp = '0xA1221A5BBEa699f507CC00bDedeA05b5d2e32Eba'
#contract = w3.eth.contract(jewel_lp, abi=abi)
#token0 = contract.functions.token0().call()
#token1 = contract.functions.token1().call()
