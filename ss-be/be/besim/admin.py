from django.contrib import admin

from beapi.models import Scenario
from beapi.models import Client
from beapi.models import ConsumerCard
from beapi.models import ConsumerAccount
from beapi.models import Consumer
from beapi.models import ReviewTemplate
from beapi.models import Merchant
from beapi.models import MerchantOffer
from beapi.constantModels import TxnCategory
from beapi.constantModels import Location

# Register your models here.

admin.site.register(Scenario)
admin.site.register(Client)
admin.site.register(ConsumerCard)
admin.site.register(ConsumerAccount)
admin.site.register(Consumer)
admin.site.register(ReviewTemplate)
admin.site.register(Merchant)
admin.site.register(MerchantOffer)
admin.site.register(Location)
admin.site.register(TxnCategory)