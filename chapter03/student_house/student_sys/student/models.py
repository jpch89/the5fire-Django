from django.db import models


class Student(models.Model):
    SEX_ITEMS = [
        (1, '男'),
        (2, '女'),
        (3, '未知'),
    ]

    STATUS_ITEMS = [
        (0, '申请'),
        (1, '通过'),
        (2, '拒绝'),
    ]

    # verbose_name 用于显示易阅读的字段名
    # 位于字段的第一个参数（除了外键，多对多，一对一以外）
    name = models.CharField(max_length=128, verbose_name='姓名')
    sex = models.IntegerField(choices=SEX_ITEMS, verbose_name='性别')
    profession = models.CharField(max_length=128, verbose_name='职业')
    email = models.EmailField(verbose_name='Email')
    qq = models.CharField(max_length=128, verbose_name='QQ')
    phone = models.CharField(max_length=128, verbose_name='电话')
    status = models.IntegerField(choices=STATUS_ITEMS, default=0, verbose_name='审核状态')
    created_time = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='创建时间')

    def __str__(self):
        return '<Student: {}>'.format(self.name)

    class Meta:
        verbose_name = verbose_name_plural = '学员信息'

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @property
    def sex_show(self):
        return dict(self.SEX_ITEMS)[self.sex]
