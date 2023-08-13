from django.db import models


class Recipient(models.Model):
    tg_id = models.IntegerField(primary_key=True)
    is_group = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50, 
                                  null=True, 
                                  default=None, 
                                  blank = True)
    last_name = models.CharField(max_length=50, 
                                 null=True, 
                                 default=None, 
                                 blank = True)
    username = models.CharField(max_length=50, 
                                null=True, 
                                default=None, 
                                blank = True)
    title = models.CharField(max_length=200, 
                             null=True, 
                             default=None, 
                             blank = True)

    def __str__(self):
        if self.is_group:
            return title
        else:    
            return str(self.first_name) + str(self.last_name)


class Subscription(models.Model):
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE, default=None, null=True)
    page = models.ForeignKey('socnet.Page', on_delete=models.CASCADE, default=None, null=True)
    #platform = models.ForeignKey('socnet.Platform', on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return str(self.recipient.tg_id)


        