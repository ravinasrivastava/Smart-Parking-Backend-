from django.contrib import admin
from .models import Device_table,Parking_site,Show_v, Booking ,Payment
# Register your models here.
# admin.site.register(Booking)
# admin.site.register(Payment)

@admin.register(Payment)
class Device_tableAdmin(admin.ModelAdmin):
    list_display=['id','pay','user','booking_id']
    
@admin.register(Booking)
class Device_tableAdmin(admin.ModelAdmin):
    list_display=['id','device_eui','parking_name','platenumber','checkin_date','checkout_date','is_checkout']
    

@admin.register(Show_v)
class Device_tableAdmin(admin.ModelAdmin):
    list_display=['id','user','platenumber','stateprovision','modal','color',]
    

@admin.register(Device_table)
class Device_tableAdmin(admin.ModelAdmin):
    list_display=['parking','device_eui','floor_no','parking_name','floor_no','status','lat','lng']
    
    
    
    
@admin.register(Parking_site)
class Parking_siteAdmin(admin.ModelAdmin):
    list_display=['id','parking_name','state','city','address','price','price_1hr','no_of_parking','user']
    