from django.urls import path
from vehicleapi.views import VehicleRegisterView,MapdetailView,MapView,Parking_siteView,Device_tableView,VehicleRegister1View,VehicleRegister2View,BookingRegisterView
from vehicleapi.views import CheckView

urlpatterns = [
    path('register_v/', VehicleRegisterView.as_view(), name='register_v'),
    path('booking/', BookingRegisterView.as_view(), name='booking'),
    path('check/<str:my>/', CheckView.as_view(), name='check'),
    path('register_v/<str:id>/', VehicleRegister1View.as_view(), name='register_v1'),
    path('register_v/<str:pk1>', VehicleRegister2View.as_view(), name='register_v2'),
    path('parking_site/', Parking_siteView.as_view(), name='parking_site'),
    path('device_table/', Device_tableView.as_view(), name='device_table'),
    path('map/', MapView.as_view(), name='map'),
    path('map/<str:my>/', MapdetailView.as_view(), name='detail'),
    path('map/<str:my>/<str:my1>/', MapdetailView.as_view(), name='detail1'),
    path('map/<str:my>/<str:my1>/<str:my2>/', MapdetailView.as_view(), name='detail2'),
   
    
]