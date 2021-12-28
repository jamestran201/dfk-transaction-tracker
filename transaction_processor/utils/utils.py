import os

from web3 import Web3

from transaction_processor.utils.abi_parser import ABIParser
from transaction_processor.contracts.contract_address import SerendaleContractAddress
from transaction_processor.contracts.contract_address import Tokens


def receipt_data():
    data = {}
    data['function'] = {}
    data['event'] = {}
    return data

def get_transaction_receipt(transaction_hash,main_net='https://rpc.s0.t.hmny.io'):
    w3 = Web3(Web3.HTTPProvider(main_net))
    return w3.eth.get_transaction_receipt(transaction_hash)

def get_transaction_receipt_data(txn_receipt,txn_input,contract_address,main_address,abidir='contracts/abi',main_net='https://rpc.s0.t.hmny.io'):
    # Loop through all abis to find function info
    w3 = Web3(Web3.HTTPProvider(main_net))
    abi_parsers = _create_abi_parsers(abidir)
    data = {}
    for abi_parser in abi_parsers:
        abi_data = receipt_data() # Set-up empty data
        abi_json = abi_parser.load_json() # load json into parser
        contract = w3.eth.contract(contract_address,abi=abi_json) # generate web3 contract to parse txn
        try:
            abi_data['function'] = _decode_transaction_function(contract, txn_input, abi_parser)
            abi_data['event'] = _decode_transaction_receipts(contract, abi_parser, txn_receipt)
        except:
            continue

        data[abi_parser.abi_name()] = abi_data

    return data

def _create_abi_parsers(abi_dir):
    all_abis = [os.path.join(abi_dir,i) for i in os.listdir(abi_dir)]
    return [ABIParser(abi) for abi in all_abis]

def _decode_transaction_function(contract, txn_input, abi_parser):
    """
    Decode txn function & function input
    """
    result = {}

    decoded_txn_input = contract.decode_function_input(txn_input)
    func = str(decoded_txn_input[0]).split('Function ')[1].split('(')[0]
    result[func] = []

    inputs = decoded_txn_input[1]
    input_types = abi_parser.get_function_input_types(func)
    output_types = abi_parser.get_function_output_types(func)
    # Save function info
    for key,values in inputs.items():
        result[func].append(
            {
                key: (values, input_types[key])
            }
        )

    return result

def _decode_transaction_receipts(contract, abi_parser, txn_receipt):
    """
    Extract txn receipt
    """
    results = {}
    abi_events = abi_parser.get_event_names()
    for event in abi_events:
        results[event] = []
        try:
            processed_receipts = getattr(contract.events,event)().processReceipt(txn_receipt)
            if isinstance(processed_receipts, tuple) and len(processed_receipts) > 0:
                for receipt in processed_receipts:
                    receipt_inputs = dict(dict(receipt)['args'])
                    input_types = abi_parser.get_event_input_types(event)
                    # Save event info
                    for key,values in receipt_inputs.items():
                        results[event].append(
                            {
                                key: (values, input_types[key])
                            }
                        )
        except:
            continue

    return results


def process_address(address, main_address):
    assert main_address is not None and isinstance(address,str)

    address = address.lower()

    CONTRACT_ADDRESSES = SerendaleContractAddress.CONTRACT_ADDRESS
    CONTRACT_ADDRESSES[main_address] = "USER"
    name = CONTRACT_ADDRESSES.get(address, None)
    if name:
        return name

    name = Tokens.TOKEN_ADDRESS.get(address, None)
    return name

# Removal later
def _process_address(address, main_address):
    address = address.lower()

    CONTRACT_ADDRESSES = SerendaleContractAddress.CONTRACT_ADDRESS
    CONTRACT_ADDRESSES[main_address] = "USER"
    name = CONTRACT_ADDRESSES.get(address, None)
    if name:
        return name

    name = Tokens.TOKEN_ADDRESS.get(address, None)
    return name

def _process_input(_input,_input_type,main_address,list_flag=False):
    #{'uint8', 'bool', 'address[]', 'uint16', 'uint256[]', 'uint256', 'address', 'uint128', 'uint64'}
    # Check if input_type is a list
    if _input_type[-2:] == '[]':
        list_flag = True

    if 'address' in _input_type:
        if not list_flag:
            return _process_address(_input,main_address)
        else:
            return [_process_address(i,main_address) for i in _input]
    elif 'int' in _input_type:
        if not list_flag:
            return int(_input)
        else:
            return [int(i) for i in _input]
    elif 'bool' in _input_type:
        if not list_flag:
            return bool(_input)
        else:
            return [bool(i) for i in _input]
    else:
        from rich.console import Console
        red_console = Console(style="bold red")
        red_console.print("INPUT_TYPE [{_input_type}] NOT IMPLEMENTED.")
        return None

def process_transaction_data(transaction_data,main_address=None,verbose=True,logpath=None):
    if verbose:
        if not bool(transaction_data):
            print(f"------[PROCESSED] TRANSACTION RECEIPT------\nEMPTY")
        else:
            print(f"------[PROCESSED] TRANSACTION RECEIPT------")

    if logpath is None:
        pass
    else:
        with open(logpath,'a') as f:
            if not bool(transaction_data):
                f.write(f"------[PROCESSED] TRANSACTION RECEIPT------\nEMPTY\n")
            else:
                f.write(f"------[PROCESSED] TRANSACTION RECEIPT------\n")

    for abi in transaction_data.keys():
        for _type in transaction_data[abi].keys():
            for _type_key in transaction_data[abi][_type].keys():
                n_receipts = len(transaction_data[abi][_type][_type_key])
                for i in range(n_receipts):
                    for name,values in transaction_data[abi][_type][_type_key][i].items():
                        _input = values[0]
                        _input_type = values[1]
                        _processed_input = _process_input(_input,_input_type,main_address)
                        # Output to terminal
                        if verbose:
                            loop_elements = [abi,_type,_type_key,i,name,_processed_input,_input_type]
                            log = ' | '.join([str(i) for i in loop_elements])
                            print(f"{log}")
                        # Write to logpath
                        if logpath is None:
                            pass
                        else:
                            loop_elements = [abi,_type,_type_key,i,name,_processed_input,_input_type]
                            log = ' | '.join([str(i) for i in loop_elements])
                            with open(logpath,'a') as f:
                                f.write(f"{log}\n")
