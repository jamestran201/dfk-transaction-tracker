import requests
import json
import warnings

warnings.filterwarnings("ignore")

def api_call(query,url='https://graph4.defikingdoms.com/subgraphs/name/defikingdoms/dex'):
    
    return requests.post(url,json={'query':query})

class QueryTokens:
    def __init__(self,token_path,endpoint='https://graph2.defikingdoms.com/subgraphs/name/defikingdoms/dex'):
        self.token_path = token_path

    def _get_query(self,query_type,skip,first):
        if query_type == 'build_all':
            query_ = f"tokens(skip:{skip},first:{first})"
        else:
            NotImplemented

        query = f"""query{{
          {query_} {{
              id
              symbol
              name
              }}
        }}"""

        return query

    def _write_py(self,json_data,rule,counter):
        with open(self.token_path, rule) as f:
            if counter == 1:
                f.write("TOKEN_ADDRESS = {\n")
            for token in json_data['data']['tokens']:
                f.write(f"        \"{token['name']} ({token['symbol']})\": \"{token['id']}\",\n")
    
    def get_tokens(self):
        """
        Get associated info of all historical/current sales
        """
        # Get all sale info
        loop_flag= True
        counter = 0
        while loop_flag:
            skip = counter*1000
            first = 1000
            counter += 1
            # query sales for one loop
            query = self._get_query(query_type='build_all',skip=skip,first=first)
            r = api_call(query)
            json_data = json.loads(r.text)
            if counter == 1:
                self._write_py(json_data,'w',counter)
            else:
                self._write_py(json_data,'a',counter)
            if len(json_data['data']['tokens'])==0:
                with open(self.token_path, 'a') as f:
                    f.write("         }")
                break
