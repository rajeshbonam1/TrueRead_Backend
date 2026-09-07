from django.contrib import admin
from .models import MeterReaderRegistration,Consumers,UserManagement

# Register your models here.
class MeterReaderRegistrationAdmin(admin.ModelAdmin):
    list_display = ['id','mrId','mrName','section','mrPhone','mrPhoto','androidToken']

admin.site.register(MeterReaderRegistration,MeterReaderRegistrationAdmin)
admin.site.register(Consumers)
admin.site.register(UserManagement)