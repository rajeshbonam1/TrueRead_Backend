from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from  ..models import Consumers,MeterReaderRegistration,Office,notificatio_recepients,NotificationMani
from ..serializers import MeterReaderRegistrationSerializer,ConsumerDataSerializer,ConsumerWiseDetailsSerializer,MridSerializer,NotificationManiSerializer,NotificationRecepientsSerializer,ConsumerSerializer
 
from django.db.models import Q
from rest_framework import status
import datetime
from rest_framework.decorators import parser_classes

from rest_framework.parsers import MultiPartParser, FormParser
from django.db import connection
import json
import jwt
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

from django.http import JsonResponse
from django.db.models import Count,Case, When, IntegerField
# from decouple import config
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
# from rest_framework import pagination
import base64
from datetime import datetime,timedelta,date
from copy import deepcopy
import math
import requests

# Create your views here.

SECRETKEY="6AZJYQ2T317WGPXC0UHVLDOR49FIBS8N5ME"

@api_view(['POST'])
def sendnotificationforexcelsheet(request):
    locationwise = request.data.get('locationwise',None)
    locationname = request.data.get('locationname',None)
    new4=[]
    newdata4=[]
    def listfun4(dict):
        if dict['mr_id'] not in new4:
            new4.append(dict.copy())
        return new4
    cursor=connection.cursor()
    newdict4={}
    if(locationwise is not None):
        # ===========================================
        # get all location data for excel
        query4=(f''' 
        SELECT  r."mrId",discom,zone,circle,division,subdivision,sectioncode
            FROM meterreaderregistration r
            WHERE {locationwise} = '{locationname}' order by r."mrId"
        ''')
    
        cursor.execute(query4)
        result4=cursor.fetchall()
        for row4 in result4:
            if row4[0] not in newdata4:
                newdict4['mr_id']=row4[0]
                newdict4['ofc_discom']=row4[1]
                newdict4['ofc_zone']=row4[2]
                newdict4['ofc_circle']=row4[3]
                newdict4['ofc_division']=row4[4]
                # newdict4['ofc_sub_div_code']=row4[5]
                newdict4['ofc_subdivision']=row4[5]
                newdict4['ofc_section']=row4[6]

                newdata4=listfun4(newdict4)
        return Response({"msg":"done","data":newdata4})

@api_view(["POST"])
def importExcelfunc(request):
    locationwise = request.data.get('locationwise',None)
    locationname = request.data.get('locationname',None)
    data= Consumers.objects.filter(ofc_discom="NBPDCL")
    serializer = ExcelSerializer(data,many=True)
    return Response(serializer.data)


@api_view(['GET'])
def notificationDataGrid(request):
    person_objects = NotificationMani.objects.all().order_by('-Message_delivery_date_time')
    serializer = NotificationManiSerializer(person_objects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def notificationDataGridChild(request):
    id = request.query_params.get('id')
    person_objects = notificatio_recepients.objects.filter(notification_id=id)
    serializer = NotificationRecepientsSerializer(person_objects, many=True)
    return Response(serializer.data)
# @api_view(['GET'])
# def notificationDataGrid(request):
#     paginator = PageNumberPagination()
#     paginator.page_size = 10
#     person_objects = NotificationMani.objects.all()
#     result_page = paginator.paginate_queryset(person_objects, request)
#     serializer = NotificationManiSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)

# @api_view(['GET'])
# def notificationDataGridChild(request):
#     id = request.query_params.get('id')
#     print("567890")
#     paginator = PageNumberPagination()
#     paginator.page_size = 10
#     person_objects = notificatio_recepients.objects.filter(notification_id=id)
#     result_page = paginator.paginate_queryset(person_objects, request)
#     serializer = NotificationRecepientsSerializer(result_page, many=True)
#     return paginator.get_paginated_response(serializer.data)


import ast
@api_view(['POST'])
def saveExcelData(request):
    message_type = request.data.get('message_type')
    notification_criteria = request.data.get('notification_criteria')
    locationwise = request.data.get('locationwise')
    locationname = str(request.data.get('locationname'))
    request.data['location_id'] =  locationwise + "/"+ locationname
    isScheduled = request.data.get('isScheduled')
    scheduled_time = request.data.get('scheduled_time')
    message_image_url = request.data.get('message_image_url')
    if scheduled_time is None:
        now = datetime.now()
        scheduled_time = now.strftime("%Y-%m-%d %H:%M:%S")
    exceldata = request.data.get('exceldata')
    mrr = json.loads(exceldata)
    mr=mrr[:-1]
    serializer = NotificationManiSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        new=[]
        new1=[]
        def listfun(dict):
            new.append(dict.copy())
            return new
        def listfun1(dict):
            new1.append(dict.copy())
            return new1
        ID=NotificationMani.objects.latest('id')
        cursor=connection.cursor()
        newdict={}
        
        newdict1={}
        for i in mr:
            message_title=i['message_title']
            message_content=i['message_content']
            query2=(f''' 
            SELECT  r."mrId",r."mrName",r.section,r."mrPhone",r."mrPhoto",r."androidToken"
            FROM meterreaderregistration r
            WHERE r."mrId" = '{i['mr_id']}' 
            ''')
            cursor.execute(query2)
            result2=cursor.fetchall()
            for row1 in result2:
                # print(row1[0])
                newdict1['notification_id']=ID.id
                newdict1['mr_id']=row1[0]
                newdict1['mr_name']=row1[1] 
                newdict1['mr_location_section_id']=row1[2]
                newdict1['mr_mobile_number']=row1[3]
                newdict1['mr_token_id']=row1[5] 
                newdict1['message_image_url']=message_image_url
                # newdict1['message_image_url']=i["message_image_url"]
                newdict1['message_title']=i['message_title']
                newdict1['message_content']= i['message_content']

                url = 'https://fcm.googleapis.com/fcm/send'
                headers={
                            'Authorization': 'key=AAAAaPQjwDI:APA91bH61p6WCfdjdbBF4SPdRwc2SQlbCAC7-yfm2mqKfdmbdG1VqyjrB6SI0pWoVIbtSpeBwO6YGa3WovmbxfXmFpCp114Z7tJKibo-2zwNmF4fXEkp1lC1hb4SxYFmn4cuKd4RpMvp',
                            'Content-Type': 'application/json'}
                data = {
                        "to": row1[5],
                        "priority": "high",
                        "data": {
                            "title":i['message_title'],
                            "message":  i['message_content'],
                            "isScheduled" : isScheduled,
                            "scheduledTime" : scheduled_time,
                            "image":message_image_url
                        }

                } # post data
                # print("data-----",data)
                response = requests.post(url, headers=headers, json=data)
                changeData=response.json()
            
                if changeData['success'] == 1 and changeData['failure'] == 0:
                        newdict1['message_delivery_status'] = "Deliverd"
                if changeData['success'] == 0 and changeData['failure'] == 1:
                    newdict1['message_delivery_status'] = "Failed"

                newdata1=listfun1(newdict1)
            
            serializer = NotificationRecepientsSerializer(data=newdict1)
            if serializer.is_valid():
                serializer.save()
            newdata=listfun(newdict)
        return JsonResponse({"msg":"sent successfully"})
    else:
        return Response({"wrong":"Data is Not Save"})  

@api_view(['POST'])
def savenotification(request):
    message_type = request.data.get('message_type')
    notification_criteria = request.data.get('notification_criteria')
    locationwise = request.data.get('locationwise')
    locationname = str(request.data.get('locationname'))
    message_title = request.data.get('message_title')
    message_content = request.data.get('message_content')
    message_image_url = request.data.get('message_image_url')
    isScheduled = request.data.get('isScheduled')
    scheduled_time = request.data.get('scheduled_time')
    request.data['location_id'] =  locationwise + "/"+ locationname
    if scheduled_time is None:
        now = datetime.now()
        scheduled_time = now.strftime("%Y-%m-%d %H:%M:%S")
    # print("manish scheduled time===>", message_type,notification_criteria,locationwise,locationname,message_title,message_content,message_image_url,isScheduled,scheduled_time)
    # print(locationname,locationwise,"6789----------------isScheduled")
    if locationwise and locationname and message_title and message_content:
        print(date,"----------------date")
        serializer = NotificationManiSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new=[]
            new1=[]
            def listfun(dict):
                new.append(dict.copy())
                return new
            def listfun1(dict):
                new1.append(dict.copy())
                return new1
           
            ID=NotificationMani.objects.latest('id')
            cursor=connection.cursor()
            
            newdict1={}
            
            query2=(f''' 
            SELECT  r."mrId",r."mrName",r.section,r."mrPhone",r."mrPhoto",r."androidToken"
            FROM meterreaderregistration r
            WHERE {locationwise} = '{locationname}' 
            ''')
            cursor.execute(query2)
            result2=cursor.fetchall()
            print(result2)
            for row1 in result2:
                newdict1['notification_id']=ID.id
                newdict1['mr_id']=row1[0]
                newdict1['mr_name']=row1[1] 
                newdict1['mr_location_section_id']=row1[2]
                newdict1['mr_mobile_number']=row1[3]
                newdict1['mr_token_id']=row1[5] 
                newdict1['message_image_url']=message_image_url
                newdict1['message_title']=message_title
                newdict1['message_content']=message_content
                
                url = 'https://fcm.googleapis.com/fcm/send'
                headers={
                            'Authorization': 'key=AAAAaPQjwDI:APA91bH61p6WCfdjdbBF4SPdRwc2SQlbCAC7-yfm2mqKfdmbdG1VqyjrB6SI0pWoVIbtSpeBwO6YGa3WovmbxfXmFpCp114Z7tJKibo-2zwNmF4fXEkp1lC1hb4SxYFmn4cuKd4RpMvp',
                            'Content-Type': 'application/json'}
                data = {
                        "to":row1[5],
                        "priority": "high",
                        "data": {
                            "title":message_title,
                            "message": message_content,
                            "isScheduled" : isScheduled,
                            "scheduledTime" : scheduled_time,
                            "image": message_image_url
                        }
                } 
                # print("data-----",data)
                response = requests.post(url, headers=headers, json=data)
                changeData=response.json()
                
                if changeData['success'] == 1 and changeData['failure'] == 0:
                        newdict1['message_delivery_status'] = "Deliverd"
                if changeData['success'] == 0 and changeData['failure'] == 1:
                    newdict1['message_delivery_status'] = "Failed"

                newdata1=listfun1(newdict1)
                # print("changeData",changeData)
                serializer = NotificationRecepientsSerializer(data=newdict1)
                if serializer.is_valid():
                    serializer.save()
            return Response({"msg":"sent successfully"})
        else:
            return Response("data not save")
    else:
        return Response({"wrong":"Some Field is missing"})


def dictfetchall(cursor):

    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
    
@api_view(['GET'])
def getofficedatacheck(request):
    cursor=connection.cursor()
    query2=(f''' 
            SELECT  *
            FROM meterreaderregistration r
            ''')
    cursor.execute(query2)
    result2=dictfetchall(cursor)
    return Response(result2)  


    


