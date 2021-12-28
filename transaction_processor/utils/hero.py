import requests
import json

SALETAX = 3.75 / 100

def api_call(query,url='http://graph3.defikingdoms.com/subgraphs/name/defikingdoms/apiv5'):

    return requests.post(url,json={'query':query})

def check_hero_sold(auction_id,to_mapped):
    """
    Check if hero is sold in an auction transaction
    returns True when a hero is sold
    """
    if to_mapped == 'Serendale_summoning':
        query_ = f"assistingAuction(id:{auction_id})"
        auction_type = 'assistingAuction'
    elif to_mapped == 'Serendale_AuctionHouse':
        query_ = f"saleAuction(id:{auction_id})"
        auction_type = 'saleAuction'
    else:
        NotImplemented
    query = f"""query{{
      {query_} {{
          winner {{id}}
          }}
    }}"""
    r = api_call(query)
    json_data = json.loads(r.text)
    try:
        sold_hero_flag = (json_data['data'][auction_type]['winner'] is not None)
    # There are cases where the graphql query returns null
    # In these cases, it is assumed that the sale was not successful.
    except:
        sold_hero_flag = False
    
    return sold_hero_flag
 
def add_hero(hero_log,transaction_data,tx_hash,_type):

    if _type == 'summonCrystal':

        # [TxHASH: 0xecb4af1d9f0671d70a6fc50a215b6f9a82e64c9e3eaa13dfb27c0680ead31c5a] TXN receipt has no events (not sure why this is)
        # However, I don't think a crystal was summoned in this transaction.
        try:
            _id = transaction_data['HeroSummoningUpgradeable.json']['event']['CrystalSummoned'][1]['crystalId'][0]
            hero_log[f"Crystal_{_id}"] = tx_hash
        except:
            return hero_log

    if _type == 'bid':
        _id = transaction_data['SaleAuction.json']['event']['AuctionSuccessful'][0]['tokenId'][0]
        hero_log[f"addHero_{_id}"] = tx_hash

    if _type == 'open':
        _id = transaction_data['HeroSummoningUpgradeable.json']['event']['CrystalOpen'][2]['heroId'][0]
        hero_log[f"addHero_{_id}"] = tx_hash

    return hero_log
