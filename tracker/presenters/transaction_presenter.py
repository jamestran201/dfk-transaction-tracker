CONTRACT_NAME_TO_GAME_NAME_MAPPING = {
    "UniswapV2Router02": "Marketplace",
}

HARMONY_BLOCK_EXPLORER = "https://explorer.harmony.one/tx/"

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

    def tx_hash(self):
        return self.transaction["TxHash"]

    def block_explorer_link(self):
        return f"{HARMONY_BLOCK_EXPLORER}{self.transaction['TxHash']}"

    def has_token_transfers(self):
        return len(self.transaction["TxTokens"]) > 0

    def sent_tokens(self):
        results = []
        for token, amount in self.transaction["TxTokens"].items():
            if amount > 0:
                continue

            amount *= -1
            amount = self._convert_amount_relative_to_one_tokens(token, amount)
            results.append(dict(token=token, amount=amount))

        return results

    def received_tokens(self):
        results = []
        for token, amount in self.transaction["TxTokens"].items():
            if amount < 0:
                continue

            amount = self._convert_amount_relative_to_one_tokens(token, amount)
            results.append(dict(token=token, amount=amount))

        return results

    def _convert_amount_relative_to_one_tokens(self, token, amount):
        # TODO: Add logic to differentiate token vs item transfers
        # Checking that amount is greater than 1000 is quick hack
        # because the token transfers can contain in-game items as well.
        # The amount for these in-game items does not need to be normalized.
        if token != "ONE" and amount > 1000:
            return amount / 10e17
        else:
            return amount
