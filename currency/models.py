from django.db import models
from django.contrib.auth.models import User

class CurrencyTransferHistory(models.Model):

    from_user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,related_name='from_user')
    from_user_currency = models.CharField(max_length=21)
    from_user_quantity = models.DecimalField(max_digits=19,decimal_places=2)
    to_user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True,related_name='to_user')
    to_user_currency = models.CharField(max_length=21)
    to_user_currency_price = models.DecimalField(max_digits=19,decimal_places=2)
    to_user_quantity = models.DecimalField(max_digits=19,decimal_places=2)
    event_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'ce_currency_transfer_history'

    

