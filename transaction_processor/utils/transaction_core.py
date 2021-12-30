from web3 import Web3

from transaction_processor.utils import utils, hero
from transaction_processor.utils.abi_parser import ABIParser
from transaction_processor.contracts.contract_address import SerendaleContractAddress

from rich.console import Console
console = Console()

w3 =  Web3(Web3.HTTPProvider('https://rpc.s0.t.hmny.io'))

event_hex = {
        'Transfer': '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef',
        'Withdrawal': '0x7fcf532c15f0a6db0bd6d0e038bea71d30d808c7d98cb3bf7268a95bf5081b65'
        }

JewelToken_address = [k for k, v in SerendaleContractAddress.CONTRACT_ADDRESS.items() if v == 'Serendale_JewelToken'][0]

ETH = "ONE"

def get_LiquidityPair(lp_addr):
    if lp_addr.lower() == '0xEb579ddcD49A7beb3f205c9fF6006Bb6390F138f'.lower():
        token0 = 'Serendale_JewelToken' # JewelToken
        token1 = 'ONE'
        return (token0,token1)
    else:
        try:
            abi = ABIParser('transaction_processor/contracts/abi/IUniswapV2Pair.json').load_json()
            contract = w3.eth.contract(lp_addr,abi=abi)
            token0 = contract.functions.token0().call()
            token1 = contract.functions.token1().call()
            return (utils.process_address(token0,''),
                    utils.process_address(token1,''))
        except:
            return None

def get_Transfers(transaction_receipt,main_address,verbose=False):
    net_transactions = {}
    for log in transaction_receipt['logs']:
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

            address = log['address']
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

def deposit(liquidity_pool,net_transactions):
    for key, value in net_transactions.items():
        # Get liquidity pairs (deposited txns)
        if value < 0:
            tokens = get_LiquidityPair(key)
            liquidity_pool[f"{tokens[0]}-{tokens[1]}"] = abs(value)

    return liquidity_pool

def withdraw(liquidity_pool,net_transactions):
    for key, value in net_transactions.items():
        tokens = get_LiquidityPair(key)
        if tokens is not None:
            liquidity_pool[f"{tokens[0]}-{tokens[1]}"] = -1 * value

    return liquidity_pool

def createAuction(net_transactions,hero_log,transaction_data,to_mapped):
    """
    query graphQL to see if hero is sold,
    if hero is sold, the USER recieves JEWEL
    and loses their hero
    """
    _id = transaction_data['SaleAuction.json']['event']['AuctionCreated'][1]['tokenId'][0] # Hero id
    auction_id = transaction_data['SaleAuction.json']['event']['AuctionCreated'][2]['auctionId'][0] # Auction Id
    price = transaction_data['SaleAuction.json']['event']['AuctionCreated'][3]['startingPrice'][0] # Price of hero
    # `to_mapped` determines if the hero is rented or sold
    if hero.check_hero_sold(auction_id, to_mapped):
        profit = price * (1-hero.SALETAX)
        net_transactions[ JewelToken_address ] = profit
        if to_mapped == 'Serendale_summoning':
            hero_log[f"rentHero_{_id}"] = profit
        elif to_mapped == 'Serendale_AuctionHouse':
            hero_log[f"subtractHero_{_id}"] = profit
        else:
            NotImplemented
    else:
        pass

    return net_transactions, hero_log
