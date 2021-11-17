from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from core.models import Genero
from core.serializers import GeneroSerializer


class GenerosList(APIView):
    def get(self, request):
        generos = Genero.objects.all()
        serializer = GeneroSerializer(generos, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GeneroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

class GeneroDetail(APIView):
    def get(self, request, id):
        genero = get_object_or_404(Genero.objects.all(), id=id)
        serializer = GeneroSerializer(genero)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id):
        genero = get_object_or_404(Genero.objects.all(), id=id)
        serializer = GeneroSerializer(genero, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        genero = get_object_or_404(Genero.objects.all(), id=id)
        genero.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    