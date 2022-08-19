# from dataclasses import field, fields
# from pyexpat import model
from rest_framework import serializers
from students.models import Student


# 创建序列化器类，以便在views.py中被调用
class StudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student  # model指明序列化器处理的数据字段从模型类Student中参考生成
        fields = '__all__'  # fields指明该序列化器包含模型类中的哪些字段，__all__表示所有字段
        # 补充：
        # 如果fields = ['name','sex']，则视图views中序列化后就只能显示name和sex字段
