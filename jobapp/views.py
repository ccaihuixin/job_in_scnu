import json

from django.db.models import Q
from django.db.models import F
from django.shortcuts import render
from rest_framework import serializers
from jobapp import models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import BaseFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
import base64
import json
from Crypto.Cipher import AES


class WXBizDataCrypt:  # 微信小程序解密类
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


# Create your views here.
class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"


class Job_addModelSerializer(serializers.ModelSerializer):
    class Meta:
        publisher = serializers.CharField(source='User.openid')  # 关联外键
        model = models.Job_info
        fields = (
            "id", "name", "job_kind", "salary", "date", "jobtime", "locate", "information", "time", "signed", "need",
            "publisher", "index")
        # depth = 1


class Job_infoModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.Job_info
        fields = "__all__"


class Job_infoView(APIView):
    def get(self, request, *args, **kwargs):
        kind = request.query_params.get("kind")
        print(kind)
        if kind != "all":
            job_kinds = eval(request.query_params.get('jobkind_list'))  # 获取到工作类型,job_kind为str类型
            print(job_kinds)
            con = Q()
            for i in job_kinds:
                print(i)
                q = Q()
                q.children.append(('job_kind', i))
                con.add(q, 'OR')

            queryset = models.Job_info.objects.filter(con)
            ser = Job_infoModelSerilizer(instance=queryset, many=True)
            print(ser.data)
            return Response(ser.data, status=200)
        else:  # 没有选择类别默认加载全部数据
            queryset = models.Job_info.objects.all()
            ser = Job_infoModelSerilizer(instance=queryset, many=True)
            return Response(ser.data, status=200)

    def delete(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if models.Job_info.objects.filter(id=data["jobid"]).exists():
            models.Job_info.objects.filter(id=data["jobid"]).delete()
        queryset = models.Job_info.objects.all()
        ser = Job_infoModelSerilizer(instance=queryset, many=True)
        return Response(ser.data, status=200)

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        result = models.Job_info.objects.filter(id=data["id"]).update(**data)
        if result:
            return Response("更新成功")
        else:
            return Response("更新失败")


class Job_detailModelSerilizer(serializers.ModelSerializer):
    class Meta:
        model = models.Job_info
        fields = "__all__"


class Job_detailView(APIView):  # 兼职详细信息
    def get(self, request, *args, **kwargs):
        id = request.query_params.get("id")
        queryset = models.Job_info.objects.filter(id=id)[0]
        print(queryset)
        ser = Job_detailModelSerilizer(instance=queryset)
        return Response(ser.data, status=200)


class Job_addView(CreateAPIView):  # 添加新的兼职
    serializer_class = Job_addModelSerializer

    def perform_create(self, serializer):
        new_object = serializer.save()
        return new_object


class UserView(APIView):  # 用户信息
    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        openid = data["openid"]
        appid = data["appid"]
        sessionKey = data["sessionKey"]
        encryptedData = data["encryptedData"]
        iv = data['iv']
        pc = WXBizDataCrypt(appid, sessionKey)
        phonenumber = pc.decrypt(encryptedData, iv)["phoneNumber"]
        print(phonenumber)
        if not models.User.objects.filter(openid=openid).exists():
            result = models.User.objects.create(openid=openid, phonenumber=phonenumber)
            ser = UserModelSerializer(instance=result)
            return Response(ser.data)
        else:
            return Response("用户信息存在")


class My_publishView(APIView):  # 我的发布
    def get(self, request, *args, **kwargs):
        publisher = request.query_params.get('publisher')  # 获取用户的openid
        print(publisher)
        queryset = models.Job_info.objects.filter(publisher=publisher)
        ser = Job_addModelSerializer(instance=queryset, many=True)  # 数据校验
        return Response(ser.data, status=200)


class User_collectModelSerializer(serializers.ModelSerializer):
    class Meta:
        user = serializers.CharField(source='User.openid')
        job_info = serializers.IntegerField(source='Job_info.id')
        model = models.User_collect
        fields = ('user', 'job_info')


class My_collectView(APIView):  # 我的收藏
    def get(self, request, *args, **kwargs):
        jobid = request.query_params.get("jobID")  # 获取当前兼职信息id
        openid = request.query_params.get("openID")  # 获取当前用户的id
        con = Q()
        con.connector = 'AND'
        con.children.append(('job_info', jobid))
        con.children.append(('user', openid))
        if models.User_collect.objects.filter(con).exists():  # 判断用户收藏数据表中是否存在该数据
            return Response(True, status=200)
        else:
            return Response(False, status=200)

    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        collect = data['collect']  # 用户是否已收藏
        if not collect:  # 用户当前每收藏 点击收藏
            result = models.User_collect.objects.create(user_id=data["openid"], job_info_id=data["id"])
            ser = User_collectModelSerializer(instance=result)
            return Response(True, status=200)
        else:
            con = Q()
            con.connector = 'AND'
            con.children.append(('job_info', data["id"]))
            con.children.append(('user', data["openid"]))
            models.User_collect.objects.filter(con).delete()
            return Response(False, status=200)


class User_collectListModelSerializer(serializers.ModelSerializer):
    job_info = Job_addModelSerializer()

    class Meta:
        model = models.User_collect
        fields = '__all__'


class My_collectListView(APIView):
    def get(self, request, *args, **kwargs):
        openid = request.query_params.get("openid")
        queryset = models.User_collect.objects.filter(user_id=openid)
        ser = User_collectListModelSerializer(instance=queryset, many=True)  # 数据校验
        return Response(ser.data, status=200)


class My_signedModelSerializer(serializers.ModelSerializer):
    job_info = Job_addModelSerializer()

    class Meta:
        model = models.User_signed
        fields = '__all__'


class SignView(APIView):
    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        openid = data['openid']
        jobid = data['jobid']
        con = Q()
        con.connector = 'AND'
        con.children.append(('job_info', data["jobid"]))
        con.children.append(('user', data["openid"]))
        if not models.User_signed.objects.filter(con).exists():
            result = models.User_signed.objects.create(user_id=openid, job_info_id=jobid)
            models.Job_info.objects.filter(id=jobid).update(signed=F("signed") + 1)
        else:
            models.User_signed.objects.filter(user_id=openid, job_info_id=jobid).delete()
            models.Job_info.objects.filter(id=jobid).update(signed=F("signed") - 1)
        queryset = models.Job_info.objects.filter(id=jobid)
        ser = Job_infoModelSerilizer(instance=queryset, many=True)
        return Response(ser.data, status=200)

    def get(self, request, *args, **kwargs):
        openid = request.query_params.get("openid")
        queryset = models.User_signed.objects.filter(user=openid)
        ser = My_signedModelSerializer(instance=queryset, many=True)
        return Response(ser.data, status=200)


class SearchView(APIView):
    def get(self, request, *args, **kwargs):
        value = request.query_params.get("value")
        queryset = models.Job_info.objects.filter(name__contains=value)
        ser = Job_infoModelSerilizer(instance=queryset, many=True)
        return Response(ser.data, status=200)
