import imp
# from .models import Show_v,Parking_site,Device_table
from .models import Show_v, Device_table, Parking_site, Booking, Paid, Payment
from rest_framework import serializers
from django.db.models import Count
v1 = 0

class VehicleRegisterSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Show_v
        fields =['user','platenumber','stateprovision','modal','color']
        
        
    def validate(self,data):
        return data
    
    # def create(self, validate_data):
    #     return Show_v.objects.create_user(**validate_data)
    
class ShowVehicleRegistrationSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField(many=True)
    class Meta:
        model = Show_v
        fields =['id','platenumber','stateprovision','modal','color']
        
class Parking_siteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Parking_site
        fields =['city']
class Parking_site1Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Parking_site
        fields =['parking_name','address']
        
class Parking_site2Serializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Parking_site
        fields =['id','city','user','parking_name','state','address','price','price_1hr']
        
    
class Parking_site3Serializer(serializers.ModelSerializer):
    
    class Meta:
        model = Parking_site
        fields =['id','city','parking_name','state','address','price','price_1hr']
        
    def validate(self,data):
        return data
        
        
class MapSerializer(serializers.ModelSerializer):
    # parking = serializers.StringRelatedField(many=True)
    # available_parking = serializers.SerializerMethodField('get_available_parking')
    # # user_count = serializers.SerializerMethodField()
    
    # def get_available_parking(self,detail_object):
    #     global v1
    #     total = getattr(detail_object,"status")
    #     if total == "True":
    #         v1 = v1+1
            
    #     return v1
    # def get_user_count(self,detail_object):
        
    #     return detail_object.status.count()
    
    class Meta:
        model = Device_table
        fields =['id','lat','lng','device_eui','parking_name','status','num_stats']
        # fields =['id','available_parking','lat','lng','device_eui','parking_name','status','num_stats']

    
class MapSerializer1(serializers.ModelSerializer):

    class Meta:
        model = Parking_site
        fields =['id','state']
    
    
class MapdetailSerializer(serializers.ModelSerializer):
    # parking = serializers.StringRelatedField(many=True)
    class Meta:
        model = Device_table
        fields =['id','lat','lng','device_eui','parking_name','status','floor_no']
      
    
class Device_tableSerializer(serializers.ModelSerializer):
    parking = serializers.StringRelatedField(many=True,read_only=True)
    class Meta:
        model = Device_table
        fields =['id','parking','device_eui','parking_name','floor_no','status','lat','lng']
      
class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model  = Booking
        fields =("device_eui", "parking_name", "platenumber", "checkin_date", "checkout_date","is_checkout", "charge","user")
# class BookingSerializer(serializers.ModelSerializer):
#     device_table = Device_tableSerializer
#     parking_site = MapdetailSerializer
#     show_v  = VehicleRegisterSerializer
#     class Meta:
#         model  = Booking
#         fields =("device_table", "parking_site", "show_v", "checkin_date", "checkout_date","is_checkout", "charge","username1")
class BookingSerializer1(serializers.ModelSerializer):
    # user1 = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # device_table = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    # device_table = Device_tableSerializer
    # parking_site = MapdetailSerializer
    # show_v  = VehicleRegisterSerializer
    class Meta:
        model  = Booking
        fields =('username1',"id","parking_name", "platenumber", "device_eui", "checkin_date", "checkout_date", "charge")

class PaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paid
        fields = "__all__"
        read_only_fields = ["id",  "paid", ]
class PaymentSerializer(serializers.ModelSerializer):
    booking = serializers.PrimaryKeyRelatedField(many=True,read_only=True)
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = ["id",   "booking"]