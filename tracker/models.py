from django.db import models
from jsonfield import JSONField

class TransactionSynchronization(models.Model):

    class Meta:
        db_table = "transaction_synchronization"

    class Status(models.TextChoices):
        PENDING = "PENDING"
        IN_PROGRESS = "IN_PROGRESS"
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"

    id = models.BigAutoField(primary_key=True)
    wallet_address = models.CharField(max_length=1024)
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def jsonfield_default_value():

    return {
            'tokens':{},
            'heroes':{},
            'liquidity_pools':{}
            }

class Wallet(models.Model):

    class Meta:
        db_table = 'wallets'

    created_at = models.DateTimeField()
    wallet_address = models.CharField(max_length=1024,primary_key=True)
    balance = JSONField(default=jsonfield_default_value())

    def __str__(self):
        return self.wallet_address

class Transaction(models.Model):

    class Meta:
        db_table = 'transactions'

    wallet_address = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_hash = models.CharField(max_length=1024,primary_key=True)
    transaction_timestamp = models.DateTimeField()
    address_from = models.CharField(max_length=1024)
    address_to = models.CharField(max_length=1024)
    function = models.CharField(max_length=128)
    transaction_fee = models.FloatField()
    token_transaction = JSONField(null=True)
    hero_transaction = JSONField(null=True)
    lp_transaction = JSONField(null=True)
    
    def update(self):
        if token_transaction is not None:
            for k,v in token_transaction.items():
                if k not in wallet_address.balance['tokens']:
                    self.wallet_address.balance['tokens'][k] = v
                else:
                    self.wallet_address.balance['tokens'][k] += v

        if self.wallet_address.balance['heroes'] is not None:
            for hero, hero_values in hero_transaction.items():
                # Input hero dict key in balance if it does not exist
                if hero not in self.wallet_address.balance['heroes']:
                    self.wallet_address.balance['heroes'][hero] = {}
                # Determine the value of the hero based on materials used to create him/her
                for k, v in hero_values.items():
                    if k not in self.wallet_address.balance['heroes'][hero]:
                        self.wallet_address.balance['heroes'][hero] = v
                    else:
                        self.wallet_address.balance['heroes'][hero] += v
        
        if self.wallet_address.balance['liquidity_pools'] is not None:
            for lp, lp_values in lp_transaction.items():
                # Input lp dict key in balance if it does not exist
                if lp not in self.wallet_address.balance['liquidity_pools']:
                    self.wallet_address.balance['liquidity_pools'][lp] = lp_values
                else:
                    self.wallet_address.balance['liquidity_pools'][lp] += lp_values

    def __str__(self):
        return self.transaction_hash
