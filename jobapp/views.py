import json

from conda.common.serialize import json_load
from django.shortcuts import render
from rest_framework import serializers
from jobapp import models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView


# Create your views here.
class Job_infoModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.job_info
        fields = "__all__"


class Job_infoView(APIView):
    def get(self, request, *args, **kwargs):
        job_kind = request.query_params.get('job_kind')
        queryset = models.job_info.objects.filter(job_kind=job_kind)
        ser = Job_infoModelSerilizer(instance=queryset, many=True)
        return Response(ser.data, status=200)


class Job_detailModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.job_info
        fields = "__all__"


class Job_detailView(APIView):
    def get(self, request, *args, **kwargs):
        id = request.query_params.get("id")
        queryset = models.job_info.objects.filter(id=id)[0]
        print(queryset)
        ser = Job_detailModelSerilizer(instance=queryset)
        return Response(ser.data, status=200)


# class Job_addView(CreateAPIView):
#     def post(self, request, *args, **kwargs):
#         data = dict(request.data)
#
#         result = models.job_info.objects.create(**data)
#         print(result)
#         return Response(result)

class Job_addModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.job_info
        fields = "__all__"


class Job_addView(CreateAPIView):
    serializer_class = Job_addModelSerializer

    def perform_create(self, serializer):
        new_object = serializer.save()
        return new_object
