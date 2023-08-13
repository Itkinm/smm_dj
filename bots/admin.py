from django.contrib import admin
from bots.models import Recipient, Subscription

# Register your models here.
@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
	pass

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
	pass
