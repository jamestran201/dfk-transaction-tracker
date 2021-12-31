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
 
def add_hero(hero_log,transaction_data,crystalId_log,tx_tokens,_type):

    if _type == 'summonCrystal':

        try:
            _id = transaction_data['HeroSummoningUpgradeable.json']['event']['CrystalSummoned'][1]['crystalId'][0]
            hero_log[f"Crystal_{_id}"] = tx_tokens
        except:
            return hero_log

    if _type == 'bid':
        _id = transaction_data['SaleAuction.json']['event']['AuctionSuccessful'][0]['tokenId'][0]
        hero_log[f"addHero_{_id}"] = tx_tokens

    if _type == 'open':
        _id = transaction_data['HeroSummoningUpgradeable.json']['event']['CrystalOpen'][2]['heroId'][0]
        crystal_id = transaction_data['HeroSummoningUpgradeable.json']['event']['CrystalOpen'][1]['crystalId'][0]
        hero_log[f"addHero_{_id}"] = crystalId_log[f'Crystal_{crystal_id}']
        crystalId_log.pop(f"Crystal_{crystal_id}")

    return hero_log

def levelup_hero(hero_log,transaction_data,tx_tokens):

    _id = transaction_data['MeditationCircle.json']['function']['startMeditation'][0]['_heroId'][0]
    hero_log[f"levelupHero_{_id}"] = tx_tokens

    return hero_log




