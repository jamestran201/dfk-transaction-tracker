CONTRACT_NAME_TO_GAME_NAME_MAPPING = {
    "UniswapV2Router02": "Marketplace",
}
class TransactionPresenter:
    def __init__(self, transaction):
        self.transaction = transaction

    def date(self):
        # The timestamp field follows the format YYYY/MM/DD, HH:mm:ss
        # This function returns only the date from the timestamp
        return self.transaction["timestamp"].split(",")[0]

    def transaction_type(self):
        if self.transaction["from_mapped"] == "USER":
            contract_name = self.transaction["to_mapped"]
        else:
            contract_name = self.transaction["from_mapped"]

        # Remove the Serendale_ prefix from the contract name, if any
        contract_name = contract_name.lstrip("Serendale_")

        return CONTRACT_NAME_TO_GAME_NAME_MAPPING.get(contract_name, contract_name)

    def action(self):
        return self.transaction["function"]
