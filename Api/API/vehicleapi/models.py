from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from datetime import timedelta, datetime

def validate_platenumber(platenumber: str):
    """
    Validate the car's plate.
    """
    regexp = r"^[A-Z0-9]{4}-\d{4}$"
    if not re.search(regexp, platenumber):
        raise ValidationError(
            f"{platenumber} isn't a valid plate format. "
            "The correct format is RJ14-1111 (uppercase letters)"
        )
        
        
class Show_v(models.Model):
    user            = models.ForeignKey('accounts.User',on_delete=models.CASCADE,related_name='user',)
    platenumber     = models.CharField(max_length=9, validators=[validate_platenumber],unique=True)
    stateprovision  = models.CharField(max_length=30)
    modal           = models.CharField(max_length=30)
    color           = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.platenumber
    
    
class Parking_site(models.Model):
    user          = models.ForeignKey('accounts.User',on_delete=models.CASCADE)
    parking_name  = models.CharField(max_length=100)
    state         = models.CharField(max_length=30)
    city          = models.CharField(max_length=30)
    address       = models.CharField(max_length=100)
    price         = models.IntegerField(default='30')
    price_1hr     = models.IntegerField(default='30')
    no_of_parking = models.IntegerField(default='0')
    
    
    def __str__(self):
      return self.parking_name
    
class Device_table(models.Model):
    parking            = models.ForeignKey('vehicleapi.Parking_site',on_delete=models.CASCADE,related_name='parking')
    device_eui         = models.CharField(max_length=100)
    parking_name       = models.CharField(max_length=100)
    floor_no           = models.CharField(max_length=100)
    status             = models.BooleanField(default=True)
    lat                = models.CharField(max_length=30)
    lng                = models.CharField(max_length=30)
 
    def __str__(self) -> str:
        return self.device_eui
    
    
    @property
    def num_stats(self):
        self.status.filter(status=True).count()


class Booking(models.Model):
    user          = models.ForeignKey('accounts.User',on_delete=models.CASCADE,related_name='user1')
    device_eui    = models.CharField(max_length=100)
    parking_name  = models.CharField(max_length=100)
    platenumber   = models.CharField(max_length=100)
    checkin_date  = models.DateTimeField(default=datetime.now)
    checkout_date = models.DateTimeField(default=datetime.now)
    is_checkout   = models.BooleanField(default=False)
    charge        = models.CharField(max_length=100,default= "1")
    # amount        = models.IntegerField(default=0)

    def __int__(self) -> int:
        return self.id

    def username1(self) -> str:
        return self.user.username
    def parking_site_name(self) -> str:
        return self.parking_name
    def show_v_name(self) -> str:
        return self.platenumber
    def device_table_name(self) -> str:
        return self.device_eui

    # def charge(self) -> float:
    #     return self.is_checkout* \
    #     (self.checkout_date - self.checkin_date + timedelta(1)).days* \
    #     self.parking_site.price_1hr

        
class Paid(models.Model):
    paid          = models.BooleanField(default=False)
    user          = models.ForeignKey('accounts.User',on_delete=models.CASCADE,related_name='user2')
    booking       = models.ForeignKey(Booking, on_delete=models.CASCADE)



class Payment(models.Model):
    pay          = models.BooleanField(default=False)
    user         = models.ForeignKey('accounts.User',on_delete=models.CASCADE,related_name='user3')
    booking      = models.ForeignKey(Booking, on_delete=models.CASCADE)


