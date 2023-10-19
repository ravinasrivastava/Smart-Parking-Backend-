from functools import partial
import json
from re import I

from django.shortcuts import render
import io
# from rest_framework.parsers import JSONParser
from .models import Show_v,Device_table,Parking_site,Booking,Paid,Payment
from accounts.models import User


from .serializers import VehicleRegisterSerializer,ShowVehicleRegistrationSerializer,MapSerializer,MapSerializer1,Parking_siteSerializer,Parking_site1Serializer
from .serializers import Parking_site2Serializer,Parking_site3Serializer,Device_tableSerializer,BookingSerializer,BookingSerializer1,PaidSerializer,PaymentSerializer
# from rest_framework.renderers import JSONRenderer
# from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request
from django.utils.timezone import now
from datetime import timedelta, datetime
from typing import Union, List
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from rest_framework.views import APIView
from accounts.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

class VehicleRegisterView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request,format=None):
        current_user = request.user
        user_data = current_user.id
        serializer = VehicleRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(user_id=user_data)
            return Response({'msg':'vehicle registration successfully'},
            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        current_user = request.user
        user_data = current_user.id
        x= User.objects.filter(id=user_data)
        
        for i in x:
            print(i.is_admin)
            a=x[0].is_admin
            
            
        if a == '1':
            print('superuser')
            m=Show_v.objects.all()
            serializer=ShowVehicleRegistrationSerializer(m,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif a == '2':
            print('admin')
            m=Show_v.objects.filter(user_id = user_data)
            
            serializer=ShowVehicleRegistrationSerializer(m,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif a == '3':
            print('user')
            m=Show_v.objects.filter(user_id=user_data)
            serializer=ShowVehicleRegistrationSerializer(m,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    def put(self, request, format=None):
        current_user = request.user
        user_data = current_user.id
        data=request.data
        print(data)
        
        data1=data.get('id')
        print(data1,'data1h')
        m=Show_v.objects.get(id=data1)
       
        serializer = ShowVehicleRegistrationSerializer(m, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        current_user = request.user
        user_data = current_user.id
        data=request.data
        print(data)
        
        data1=data.get('id')
        print(data1,'data1h')
        m=Show_v.objects.filter(id=data1)
        m.delete()
        return Response({'msg':'record deleted'})



class VehicleRegister1View(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]
    def delete(self, request,id, format=None):
        m=Show_v.objects.filter(id=id)
        m.delete()
        return Response({'msg':'record deleted'})
        
class VehicleRegister2View(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]

  
    def put(self, request,pk1, format=None): 
        m=Show_v.objects.get(id=pk1)
       
        serializer = ShowVehicleRegistrationSerializer(m, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MapView(APIView):
    
    def get(self, request, format=None):
        
        m=Parking_site.objects.all().values('state').distinct()
        serializer=MapSerializer1(m,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# ////////////////////////////////////////map//////////////////////
class MapdetailView(APIView):
    

    def get( self,request,my,my1=None,my2=None, format=None):
        print(my)
        print(my1)
        print(my2)
        if my1 is None:
           
            m = Parking_site.objects.filter(state=my).values('city').distinct()
            
            if m.exists():
                
                serializer = Parking_siteSerializer(m,many=True)
                return Response(serializer.data)
            else:
                m = Parking_site.objects.filter(city=my)
                
                serializer = Parking_site1Serializer(m,many=True)
                return Response(serializer.data)
        
        elif my2 is None:
            m = Parking_site.objects.filter(city=my1)
           
            if m.exists():
                serializer = Parking_site1Serializer(m,many=True)
                return Response(serializer.data)
            else:
                a = Parking_site.objects.filter(parking_name=my1).values()
  
            b=a[0]
            c= b['price_1hr']
            
            
            m=Device_table.objects.filter(status=1,parking_name=my1)
            print(m,'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
            m1=Device_table.objects.filter(parking_name=my1).values()
            serializer=MapSerializer(m,many=True)
            q=serializer.data
            x=m1
            
            dic1={"PriceOf1hr":c}
            q.append(dic1)
            y=0
            for dic in x:
                for key in dic:
                    if dic[key] is True:
                        y+=1
                        
            dic2={"ParkingSpaceAvailable":y}
            q.append(dic2)
            
            
            return Response(q, status=status.HTTP_200_OK)
            
        else:
            a = Parking_site.objects.filter(parking_name=my2).values()
            
            b=a[0]
            c= b['price_1hr']                                                                                                                                                                                  
            m=Device_table.objects.filter(status=1,parking_name=my1)
            print(m,'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
            print(my1   ,'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')
            m1=Device_table.objects.filter(parking_name=my2).values()
            serializer=MapSerializer(m,many=True)
            q=serializer.data
            x=m1
            print(type(q),'fthrthtrh')

            dic1={"PriceOf1hr":c}
            q.append(dic1)
            print(q[0],"dsgdsgsdgsdg")
            
            y=0
            for dic in x:
                for key in dic:
                    if dic[key] is True:
                        y+=1

            dic2={"ParkingSpaceAvailable":y}
            q.append(dic2)

            # q["PriceOf1hr"]=c
            # q["ParkingSpaceAvailable"]=y
            
            return Response(q, status=status.HTTP_200_OK)
           
           
class Parking_siteView(APIView):
    
    def get(self, request, format=None):
        current_user = request.user
        user_data = current_user.id
        x= User.objects.filter(id=user_data)
        
        for i in x:
            print(i.is_admin)
            a=x[0].is_admin
            
            
        if a == '1':
            print('superuser')
            m=Parking_site.objects.all()
            serializer=Parking_site3Serializer(m,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif a == '2':
            print('admin')
            m=Parking_site.objects.filter(user_id = user_data)
            
            serializer=Parking_site3Serializer(m,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response( {'msg':'User cant see sites'})
    
    
    def post(self, request, format=None):
        if 'signin' in request.session:
            current_user = request.user
            user_data = current_user.id
            a= User.objects.filter(id=user_data)
            print('main object',a)
            for i in a:
                print(i.is_admin)
                x=a[0].is_admin
                print(a[0].is_admin,'-all data')
            
            serializer = Parking_site2Serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if x=='2':               
               
                user = serializer.save(user_id=user_data)
                print(user,"checkuser")
                return Response({ 'msg':'data created Successful'}, status=status.HTTP_201_CREATED)
                print ('data creation')
            return Response( {'msg':'User cant add sites'})
   
            
            
            
    def put(self, request, format=None):
        if 'signin' in request.session:
            current_user = request.user
            user_data = current_user.id
            a= User.objects.filter(id=user_data)
            print('main object',a)
            for i in a:
                print(i.is_admin)
                x=a[0].is_admin
                print(a[0].is_admin,'-all data')
            
            
            if x=='2':
                data=request.data
                print(data)
                
                data1=data.get('id')
                print(data1,'data1h')
                m=Parking_site.objects.get(id=data1)
                print (m,'hsadgkashkjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjs')
            
                serializer = Parking_site3Serializer(m, data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if 'signin' in request.session:
            current_user = request.user
            user_data = current_user.id
            data=request.data
            print(data)
            
            data1=data.get('id')
            print(data1,'data1h')
            m=Parking_site.objects.filter(id=data1)
            m.delete()
            return Response({'msg':'record deleted'})
        
        
            
class Device_tableView(APIView):
    
    def get(self, request, format=None):
        current_user = request.user
        user_data = current_user.id
        x= User.objects.filter(id=user_data)
        
        for i in x:
            print(i.is_admin)
            a=x[0].is_admin
            
            
        if a == '1':
            print('superuser')
            m=Device_table.objects.all()
            serializer=Device_tableSerializer(m,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif a == '2':
            print('admin')
            m1=Parking_site.objects.filter( user_id= user_data)
            for i in m1:
                y=i.parking_name
                print(y)
                m=Device_table.objects.filter(parking_id = m1)
            
                serializer=Device_tableSerializer(m,many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        
       
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def post(self, request, format=None):
        if 'signin' in request.session:
            current_user = request.user
            user_data = current_user.id
            a= User.objects.filter(id=user_data)
            print('main object',a)
            for i in a:
                print(i.is_admin)
                x=a[0].is_admin
                print(a[0].is_admin,'-all data')
            
            serializer = Device_tableSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if x=='2':               
               
                user = serializer.save()
                print(user,"checkuser")
                return Response({ 'msg':'data created Successful'}, status=status.HTTP_201_CREATED)
            print ('data creation')
            
            
            
    def put(self, request, format=None):
        if 'signin' in request.session:
            current_user = request.user
            user_data = current_user.id
            a= User.objects.filter(id=user_data)
            print('main object',a)
            for i in a:
                print(i.is_admin)
                x=a[0].is_admin
                print(a[0].is_admin,'-all data')
            
            
            if x=='2':
                data=request.data
                print(data)
                
                data1=data.get('id')
                print(data1,'data1h')
                m=Device_table.objects.get(id=data1)
                print (m,'hsadgkashkjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjsjs')
            
                serializer = Device_tableSerializer(m, data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if 'signin' in request.session:
            current_user = request.user
            user_data = current_user.id
            data=request.data
            print(data)
            
            data1=data.get('id')
            print(data1,'data1h')
            m=Device_table.objects.filter(id=data1)
            m.delete()
            return Response({'msg':'record deleted'})
            


class BookingRegisterView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request,format=None):
        current_user = request.user
        user_data = current_user.id
        a=request.data
        print(a,"uygyuugggggggggggggggggggggggggggggggggggggggggggggggggggg")
        a1=a['device_eui']
        a2=a['parking_name']
        a4=a['checkin_date']
        a5=a['checkout_date']
        y = Device_table.objects.get(device_eui=a1)
        parking=Parking_site.objects.get(parking_name=a2)
        price_1hr=parking.price_1hr
        price= 2* price_1hr
        # price= (a5-a4 + timedelta(1)).days* price_1hr

        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(user_id=user_data,charge=price)
            
            print(y)
            y.status=False
            y.save()
            return Response({'msg':'Booking successfully'},
            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        current_user = request.user
        user_data = current_user.id
        x= User.objects.filter(id=user_data)
        print(x,'4444444444444444444444444444444444444444444444444')

        for i in x:
            print(i.is_admin)
            a=i.is_admin
            print(a,'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')


        if a == '1':
            print('superuser')
            m=Booking.objects.all()
            serializer=BookingSerializer1(m,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif a == '2':
            print('admin')
            m=Booking.objects.filter(user_id = user_data)

            serializer=BookingSerializer1(m,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif a == '3':
            print('user')
            m=Booking.objects.filter(user_id=user_data)
            print(m,'sdfsdfsdfdsfsdfsdfs')
            serializer=BookingSerializer1(m,many=True)
            print(serializer,"mjmmmmmmmmmmmmmmmmmm")
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
        
class CheckView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def put(self, request,my,format=None):
        print(my)
        x = Payment.objects.filter(booking_id=my).values()
        print(x)
        y = Booking.objects.get(id=my)
        print(y)
        d_eui=y.device_eui
        di=Device_table.objects.get(device_eui=d_eui)
        di=di.id
        print(di,'di ')
        z=Device_table.objects.get(id=di)
        print(z)
 
        if x[0]['pay']:
            y.is_checkout=True
            z.status=True
            y.save()
            z.save()

            return Response({'msg':'checkout succesfully'})
        return Response( {'msg':'Payment is not done'},status=status.HTTP_400_BAD_REQUEST)
        
        
