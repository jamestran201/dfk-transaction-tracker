# abi utils
import json

class ABIParser:
    def __init__(self,abi_json, verbose=False):
        self.json = abi_json
        self.verbose = False

    def _filter_type(self,_type):
        data = self.load_json()
        return [i for i in data if i['type'] == _type]

    def _convert_to_dict(self,_type,mainkey='name'):
        data = self._filter_type(_type)
        _dict = {}
        for i in data:
            _dict[i[mainkey]] = {}
            for key,value in i.items():
                if key == mainkey:
                    pass
                else:
                    _dict[i[mainkey]][key] = value
        return _dict

    def load_json(self):
        with open(self.json) as f:
            data = json.load(f)
        return data

    def get_functions(self,_type='function'):
        return self._convert_to_dict(_type)

    def get_function_input_types(self,function):
        data = self.get_functions()[function]['inputs']
        _dict = {}
        for i in data:
            _dict[i['name']] = i['type']
        return _dict
    
    def get_function_output_types(self,function):
        data = self.get_functions()[function]['outputs']
        _dict = {}
        for i in data:
            _dict[i['name']] = i['type']
        return _dict

    def get_events(self,_type='event'):
        return self._convert_to_dict(_type)

    def get_event_names(self):
        return list(self.get_events().keys())

    def get_event_input_types(self,event):
        data = self.get_events()[event]['inputs']
        _dict = {}
        for i in data:
            _dict[i['name']] = i['type']
        return _dict

    def abi_name(self):
        return self.json.split("/")[-1]
