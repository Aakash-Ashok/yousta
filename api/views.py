from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from rest_framework.decorators import action
from rest_framework import authentication
from rest_framework import permissions

from yousta.models import Cloths,ClothVarients,Carts,Orders,Reviews

from api.serializers import UserSerializer,ClothsSerializer,CartSerializer,OrderSerializer,ReviewSerializer




class UserCreationView(APIView):
    def post(self,request,*args, **kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        
        else:
            return Response(data=serializer.errors)
        

class ClothView(ModelViewSet):
   # authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    serializer_class=ClothsSerializer
    model=Cloths
    queryset=Cloths.objects.all()
    #custom method 
    @action(methods=["post"],detail=True)
    def cart_add(self,request,*args, **kwargs):
        vid=kwargs.get("pk")
        varient_obj=ClothVarients.objects.get(id=vid)
        user=request.user
        serializer=CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(clothvarient=varient_obj,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    @action(methods=["post"],detail=True)
    def place_order(self,request,*args, **kwargs):
        oid=kwargs.get("pk")
        varient_obj=ClothVarients.objects.get(id=oid)
        user=request.user
        serializer=OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(clothvarient=varient_obj,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
#url:http://127.0.0.1:8000/api/cloths/{cloth_id}/add_review/

    @action(methods=["post"],detail=True)
    def add_review(self,request,*args, **kwargs):
        c_id=kwargs.get("pk")
        cloth_obj=Cloths.objects.get(id=c_id)
        user=request.user
        serializer=ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cloth=cloth_obj,user=user)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        

class CartsView(ViewSet):
  #  authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def list(self,request,*args, **kwargs):
        user=request.user
        qs=Carts.objects.filter(user=user)
        serializer=CartSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        Carts.objects.filter(id=id).delete()
        return Response(data={"message":"deleted"})
    

class OrderView(ViewSet):
    #authentication_classes=[authentication.BasicAuthentication]
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=OrderSerializer
    
    def list(self,request,*args,**kwargs):
        qs=Orders.objects.filter(user=request.user)
        serializer=OrderSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def destroy(self,request,*args, **kwargs):
        id=kwargs.get("pk")
        instance=Orders.objects.get(id=id)
        if instance.user==request.user:
            instance.delete()
            return Response(data={"message":"order removed successfully"})
        else:
            return Response(data={"message":"permission denied for current user"})


        
