import sys
sys.path.insert(0, '..')

from utils.query import QueryTokens

path = '../contracts/contract_address/Tokens.py'
print(f"Generating token addresses: {path}")
x = QueryTokens(path)
x.get_tokens()
