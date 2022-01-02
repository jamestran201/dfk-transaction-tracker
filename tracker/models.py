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

    created_at = models.DateTimeField(null=True,default=None)
    updated_at= models.DateTimeField(auto_now=True)
    wallet_address = models.CharField(max_length=1024,primary_key=True)
    balance = JSONField(default=jsonfield_default_value())
    crystal_log = JSONField(default={})

    def __str__(self):
        return self.wallet_address

class Transaction(models.Model):

    class Meta:
        db_table = 'transactions'
    
    class Status(models.TextChoices):
        SUCCESS = "SUCCESS"
        FAILED = "FAILED"

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_hash = models.CharField(max_length=1024,primary_key=True)
    transaction_timestamp = models.DateTimeField()
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.SUCCESS)
    address_from = models.CharField(max_length=1024)
    address_to = models.CharField(max_length=1024)
    function = models.CharField(max_length=128)
    transaction_fee = models.FloatField()
    token_transaction = JSONField(null=True)
    hero_transaction = JSONField(null=True)
    lp_transaction = JSONField(null=True)
    
    def update_balance(self):
        if self.token_transaction is not None:
            for k,v in self.token_transaction.items():
                if k not in self.wallet.balance['tokens']:
                    self.wallet.balance['tokens'][k] = v
                else:
                    self.wallet.balance['tokens'][k] += v

        if self.wallet.balance['heroes'] is not None:
            for hero, hero_values in self.hero_transaction.items():
                hero = hero.split('_')[1] # Get hero id
                # Input hero dict key in balance if it does not exist
                if hero not in self.wallet.balance['heroes']:
                    self.wallet.balance['heroes'][hero] = {}
                # Determine the value of the hero based on materials used to create him/her
                for k, v in hero_values.items():
                    if k not in self.wallet.balance['heroes'][hero]:
                        self.wallet.balance['heroes'][hero][k] = v
                    else:
                        self.wallet.balance['heroes'][hero][k] += v
        
        if self.wallet.balance['liquidity_pools'] is not None:
            for lp, lp_values in self.lp_transaction.items():
                # Input lp dict key in balance if it does not exist
                if lp not in self.wallet.balance['liquidity_pools']:
                    self.wallet.balance['liquidity_pools'][lp] = lp_values
                else:
                    self.wallet.balance['liquidity_pools'][lp] += lp_values

        self.wallet.save()

    def __str__(self):
        return self.transaction_hash
