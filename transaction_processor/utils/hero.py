import requests
import json

HEROTAX = 3.75 / 100

def api_call(query,url='http://graph3.defikingdoms.com/subgraphs/name/defikingdoms/apiv5'):

    return requests.post(url,json={'query':query})

def check_hero_sold(auction_id):
    """
    Check if hero is sold in an auction transaction
    returns True when a hero is sold
    """
    query_ = f"saleAuction(id:{auction_id})"
    query = f"""query{{
      {query_} {{
          winner {{id}}
          }}
    }}"""
    r = api_call(query)
    json_data = json.loads(r.text)
    sold_hero_flag = (json_data['data']['saleAuction']['winner'] is not None)
    
    return sold_hero_flag
 
def add_hero(hero_log,transaction_data,tx_hash,_type):

    if _type == 'summonCrystal':
        _id = transaction_data['HeroSummoningUpgradeable.json']['event']['CrystalSummoned'][1]['crystalId'][0]
        hero_log[f"Crystal_{_id}"] = tx_hash

    if _type == 'bid':
        _id = transaction_data['SaleAuction.json']['event']['AuctionSuccessful'][0]['tokenId'][0]
        hero_log[f"addHero_{_id}"] = tx_hash

    if _type == 'open':
        _id = transaction_data['HeroSummoningUpgradeable.json']['event']['CrystalOpen'][2]['heroId'][0]
        hero_log[f"addHero_{_id}"] = tx_hash

    return hero_log
