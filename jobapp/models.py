from django.db import models


# Create your models here.
class User(models.Model):  # 用户表
    openid = models.CharField(max_length=220, db_index=True, primary_key=True)  # 用户的标识符
    phonenumber = models.CharField(max_length=11,null=True)  # 用户绑定的手机号


class User_signed(models.Model):  # 用户报名表
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # 用户id
    job_info = models.ForeignKey('Job_info', on_delete=models.CASCADE)  # 兼职id


class Job_info(models.Model):  # 工作详情表
    name = models.CharField(max_length=30)  # 兼职名称
    job_kind = models.CharField(max_length=30)  # 工作类型
    salary = models.CharField(max_length=30)  # 工资
    date = models.CharField(max_length=30)  # 日期
    jobtime = models.CharField(max_length=35)  # 工作时长
    locate = models.CharField(max_length=35)  # 地址
    information = models.CharField(max_length=100)
    time = models.CharField(max_length=30)  # 发布时间
    signed = models.IntegerField(default=0)  # 报名人数
    need = models.IntegerField(default=1)  # 需要人数
    index = models.IntegerField(default=0)  # 工资的计量单位
    publisher = models.ForeignKey('User', to_field='openid', on_delete=models.CASCADE)  # 发布者


class User_collect(models.Model):  # 用户收藏表
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # 用户id
    job_info = models.ForeignKey('Job_info', on_delete=models.CASCADE)  # 兼职id
