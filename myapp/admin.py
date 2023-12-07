from django.contrib import admin
from .models import ChainUser,Product,Payment,Receipt

# Register your models here.
admin.site.register(ChainUser)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(Receipt)

