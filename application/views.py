from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User as AuthUser

from application.models import *
import application.serializer as app_ser
import json

from rest_framework import status,viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes


# Create your views here.
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    ser = app_ser.RegisterSerializer(data=request.data)
    mobNum = request.POST.get("mobileno")
    reply = {}
    
    if not ser.is_valid():
        for err in ser.errors:
           
            reply['message'] = ser.errors[err][0]
            reply['status'] = "ERROR"
            reply['error_code'] = "INVALID_"+err.upper()
            dict_obj = json.dumps(reply)
            return HttpResponse(dict_obj, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = AuthUser.objects.filter(username=mobNum).first()
        if user:
            user.first_name=ser.validated_data.get('first_name')
            user.last_name=ser.validated_data.get('last_name')
            user.email=ser.validated_data.get('email')
            user.set_password(request.POST.get('password'))
            user.save()
            
        else:
            user = ser.save()
            user.set_password(request.POST.get('password'))
            user.save()

        pass
    except Exception as e:
        print(str(e))
        reply['status'] = "ERROR"
        reply['message'] = "Server: User not created. Please contact support or retry."
        reply['error_code'] = "DB_CREATE_FAILED"
        dict_obj = json.dumps(reply)
        return HttpResponse(json.dumps(reply), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    reply['status'] = "SUCCESS"
    reply['message'] = "Signup was sucessful"
    dict_obj = json.dumps(reply)
    return HttpResponse(dict_obj, status=status.HTTP_201_CREATED)


class SnippetViewset(viewsets.ModelViewSet):

    model = Snippet
    queryset = Snippet.objects.all()
   
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return app_ser.SnippetReadSerializer

        return app_ser.SnippetSerializer

    def create(self, request):
        try:
            title = request.data['title']
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception = True)
            self.perform_create(serializer)
            
            tag_serializer = app_ser.TagSerializer
            tags = tag_serializer(data={'title': title, 'snippet':serializer.data['id']})
            if tags.is_valid():
                tags.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print("ERROR" + str(e))
            return Response("Error Occurred", status=status.HTTP_400_BAD_REQUEST)


    

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.title = request.data.get("title")
        instance.description = request.data.get("description")
        instance.title = request.data.get("title")
        instance.save()

        serializer = self.get_serializer(instance)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    
    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TagViewset(viewsets.ModelViewSet):
    
    model = Tag
    queryset = Tag.objects.all()
    serializer_class = app_ser.TagSerializer