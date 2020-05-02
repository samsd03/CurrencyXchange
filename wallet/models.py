from django.db import models
from django.contrib.auth.models import User

class UserWallet(models.Model):

    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    currency_code = models.CharField(max_length=11)
    currency_quantity = models.IntegerField()
    
    class Meta:
        db_table = 'ce_user_wallet'
    