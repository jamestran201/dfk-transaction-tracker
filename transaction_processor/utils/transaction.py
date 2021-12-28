from transaction_processor.utils import transaction_core, utils, hero

from rich.console import Console
console = Console()

import warnings
warnings.simplefilter("ignore")

class Transaction:
    def __init__(self,main_address,transaction_df,transaction_receipt,transaction_data,verbose=False):
        self.main_address = main_address
        self.transaction_df = transaction_df
        self.transaction_receipt = transaction_receipt
        self.transaction_data = transaction_data
        self.verbose = verbose
        self.info = {}
        self.hero_log = {}
        self.liquiditypool = {}
    
    def _convert_token_addresses_to_names(self):
        new_tx_tokens = {}
        for key, values in self.info['TxTokens'].items():
            token_name = utils.process_address(key, self.main_address)
            if token_name:
                new_tx_tokens[token_name] = values
            else:
                new_tx_tokens[key] = values

        self.info['TxTokens'] = new_tx_tokens

    def get_receipt(self):
        """
        Print transaction information
        """
        receipt = ""
        receipt += f"\n[[cyan]{self.info['timestamp']}[/] || [Tx Hash] [magenta]{self.info['TxHash']}[/] || [Status] {self.info['status']}\n"
        receipt += f"(Raw addresses) [yellow bold]{self.info['from']}[/] > [yellow bold]{self.info['to']}[/]\n"
        receipt += f"(Remapped addresses) [yellow bold]{self.info['from_mapped']}[/] > [yellow bold]{self.info['to_mapped']}[/]\n"
        receipt += f"(Function) {self.info['function']}\n"
        receipt += f"(Transaction fee) {self.info['TxFee']} ONE\n"
        receipt += f"(Value) {self.info['value']} ONE\n"
        receipt += f"[bold underline]Token transfers[/]\n"
        if len(self.info['TxTokens']) == 0:
            receipt += f"-\n"
        else:
            for key,values in self.info['TxTokens'].items():
                receipt += f"{key}: {values}\n"
        receipt += f"[bold underline]Hero transfers[/]\n"
        if len(self.hero_log) == 0:
            receipt += f"-\n"
        else:
            for key,values in self.hero_log.items():
                receipt += f"{key}: {values}\n"
        receipt += f"[bold underline]Liquidity pool[/]\n"
        if len(self.liquiditypool) == 0:
            receipt += f"-\n"
        else:
            for key,values in self.liquiditypool.items():
                receipt += f"{key}: {values}\n"

        console.print(receipt,highlight=False)


    def get_info(self):
        # Transaction type
        try:
            self.info['function'] = [j for j in [i for i in self.transaction_data.values()][0]['function'].keys()][0]
        except:
            self.info['function'] = str(self.transaction_data)
            if self.info['function'] == '{}':
                self.info['function'] = 'empty'
        # Skip unmatch function type // Filter function type
        self.info['status'] = dict(self.transaction_receipt)['status']
        # Basic transaction info
        self.info['TxHash'] = self.transaction_df['TxHash']
        self.info['timestamp'] = self.transaction_df['timestamp']
        self.info['to'] = self.transaction_df['to']
        self.info['from'] = self.transaction_df['from']
        self.info['to_mapped'] = self.transaction_df['to_mapped']
        self.info['from_mapped'] = self.transaction_df['from_mapped']
        # Transaction of currencies / tokens
        self.info['value'] = self.transaction_df['value']
        self.info['TxFee'] = dict(self.transaction_receipt)['gasUsed'] * self.transaction_df['gasPrice']
        self.info['TxTokens'] = transaction_core.get_Transfers(
                self.transaction_receipt,
                self.main_address,
                verbose=True
                )
        # Transaction status - transactione error occured when status:0
        self.info['status'] = dict(self.transaction_receipt)['status']
        if self.info['status'] == 0:
            # Print receipt
            if self.verbose:
                self.get_receipt()

            self._convert_token_addresses_to_names()
            return 0

        ### UniswapV2Router02 

        if self.info['function'] == 'swapExactTokensForETH':
            self.info['TxTokens'] = transaction_core.swapExactTokensForETH(
                    self.info['TxTokens'],
                    self.transaction_receipt,
                    )
        elif self.info['function'] == 'swapExactTokensForTokens':
            pass
        elif self.info['function'] == 'swapTokensForExactTokens':
            pass
        elif self.info['function'] == 'swapETHForExactTokens':
            self.info['TxTokens'] = transaction_core.swapETHForExactTokens(
                    self.info['TxTokens'],
                    self.info['value'],
                    )
        elif self.info['function'] == 'swapExactETHForTokens':
            self.info['TxTokens'] = transaction_core.swapETHForExactTokens(
                    self.info['TxTokens'],
                    self.info['value'],
                    )
        # Swap ONE+JEWEL for LP Pair
        elif self.info['function'] == 'addLiquidityETH':
            self.info['TxTokens'] = transaction_core.swapETHForExactTokens(
                    self.info['TxTokens'],
                    self.info['value'],
                    )
        # Swap TokenX+JEWEL for LP Pair
        elif self.info['function'] == 'addLiquidity':
            pass
        # Swap LP Pair for TokenX+JEWEL
        elif self.info['function'] == 'removeLiquidity':
            pass

        ### Serendale_summoning

        # has bonusItem input not included in current method
        elif self.info['function'] == 'summonCrystal':
            self.hero_log = hero.add_hero(
                    self.hero_log,
                    self.transaction_data,
                    self.info['TxHash'],
                    self.info['function']
                    )
        # open crystal to summon hero 
        # need to find example with re-charging crystal w/JEWEL to summon hero
        elif self.info['function'] == 'open':
            self.hero_log = hero.add_hero(
                    self.hero_log,
                    self.transaction_data,
                    self.info['TxHash'],
                    self.info['function']
                    )

        ### Serendale_MeditationCircle

        # TODO: ADD THIS TO VALUE OF THE HERO
        # costs Rune & Jewel to level-up
        # has attunementCrystal input not included in current method
        elif self.info['function'] == 'startMeditation':
            pass
        # Level-up stats (only TX fee)
        elif self.info['function'] == 'completeMeditation':
            pass

        ### Serendale_AuctionHouse / Serendale_summoning
        
        # Listing hero for auction (only TX fee)
        # Also, uses graphQL to query if the hero has sold
        # Hero is sold at .9675 of purchased price (dfk recieves 3.75% of hero sales)
        elif self.info['function'] == 'createAuction':
            self.info['TxTokens'], self.hero_log = transaction_core.createAuction(
                    self.info['TxTokens'],
                    self.hero_log,
                    self.transaction_data,
                    self.info['to_mapped']
                    )
        # Cancel hero for auction (only TX fee)
        elif self.info['function'] == 'cancelAuction':
            pass

        ### Serendale_AuctionHouse

        # bid for hero
        elif self.info['function'] == 'bid':
            self.hero_log = hero.add_hero(
                    self.hero_log,
                    self.transaction_data,
                    self.info['TxHash'],
                    self.info['function']
                    )

        ### Serendale_QuestCore

        # Chance to recieve quest rewards
        elif self.info['function'] == 'completeQuest':
            pass
        # Start quest (only TX fee)
        elif self.info['function'] == 'startQuest':
            pass
        # Cancel quest (Gardening quest may return Jewels?)
        elif self.info['function'] == 'cancelQuest':
            pass

        ### Serendale_MasterGardener

        # Deposit LP-pairs (also recieve existing pooled governance tokens)
        elif self.info['function'] == 'deposit':
            self.liquiditypool = transaction_core.deposit(
                    self.liquiditypool,
                    self.info['TxTokens']
                    )
        # Withdraw LP-pairs (also recieve existing pooled governance tokens)
        elif self.info['function'] == 'withdraw':
            self.liquiditypool = transaction_core.withdraw(
                    self.liquiditypool,
                    self.info['TxTokens']
                    )
        # Sum all governance tokens across all LP-pools
        elif self.info['function'] == 'claimRewards':
            pass
        # Sum governance token from a LP-pool
        elif self.info['function'] == 'claimReward':
            pass

        ### Serendale_xJEWEL
        
        # Swap xJEWEL for JEWEL
        elif self.info['function'] == 'enter':
            pass
        # Swap JEWEL for xJEWEL
        elif self.info['function'] == 'leave':
            pass

        ### Serendale_JewelToken
        elif self.info['function'] == 'transfer':
            pass

        ### Other

        # Approval (only TX fee)
        elif self.info['function'] == 'approve':
            pass
        # ApprovalForAll (only TX fee)
        elif self.info['function'] == 'setApprovalForAll':
            pass
        # TODO
        elif self.info['function'] == 'empty':
            pass

        else:
            NotImplemented

        self._convert_token_addresses_to_names()

        # Print receipt
        if self.verbose:
            self.get_receipt()
