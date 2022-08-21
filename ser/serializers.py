# from operator import truediv
# from typing_extensions import Required
# from unicodedata import name
# from unittest.util import _MAX_LENGTH
# from wsgiref.validate import validator
from email.policy import default
from unicodedata import name
from rest_framework import serializers

from students.models import Student

# 所有自定义序列化器类必须直接或者间接继承于serializers.Serializer


class StudentSerializer(serializers.Serializer):
    # 声明序列化器
    # part1. 字段声明【要转换的字段，如果在part2中使用Meta声明模型和字段后，可以不用写】
    id = serializers.IntegerField()
    name = serializers.CharField()
    sex = serializers.BooleanField()
    age = serializers.IntegerField()
    class_num = serializers.CharField()
    description = serializers.CharField()

    # part2. 可选【如果序列化器是继承ModelSerializer，则需要声明模型model和字段feilds
    # ModelSerializer是Serializer的子类】

    # part3. 可选【用于反序列化阶段对客户端提交的数据进行验证】

    # part4. 可选【用于把通过验证的数据进行数据库操作，保存到数据库。】

    # ！！！注意：serializer不是只能为数据库模型类定义，也可以为非数据库模型类的数据定义。serializer是独立于数据库之外的存在。
""" 
在drf中，对于客户端提交的数据，往往需要验证数据的有效性，这部分代码是写在序列化器中的。
在序列化器中，已经提供了三种方式或者说三个地方针对客户端提交的数据进行验证：
1. 某个字段的通用内置选项，即字段声明的小括号中，以选项的方式来验证
2. 自定义方法，在序列化器中作为对象返回来提供验证
2.1 单个字段【以形如"validate_<字段名>"】来验证，传入data参数，验证完成后返回data
2.2 多个字段直接【以validate】方法来验证，传入attrs参数，验证完成后返回attrs
3 自定义函数，在序列化器外部，提前声明一个验证代码，然后在字段声明的小圆括号中，以"validators=[验证函数1,验证函数2,...]"来验证
自定义函数中传入data参数，验证完成后返回data
"""

choices = [(1, '上班'), (2, '午休'), (3, '下班')]
title_level = [(0, '顶级人员'), (1, '高级人员'), (2, '中级人员'), (3, '初级人员')]


def check_user(data):
    """ 
    这个验证函数最重要的就是：
    1 根据传入的数据做判断
    2 用serializers.ValidationError()给出报错
    3 返回验证完成的数据
    """
    if data == 'badboy':
        raise serializers.ValidationError('用户名不能为badboy!!')
    return data


class Student3Serializer(serializers.Serializer):
    # 声明序列化器
    # part1. 字段声明【要转换的字段，如果在part2中使用Meta声明模型和字段后，可以不用写】
    # 声明什么，就序列化什么，换句话说，没有声明的字段即便模型中有也不会被序列化；
    # 如果字段已声明，即便模型中没有也会被序列化；数据提交验证通过后也不会进入到数据库中。
    # 以下三个字段是模型对象中有的字段
    name = serializers.CharField(max_length=10, min_length=4, validators=[
                                 check_user])  # 两个选项式验证，一个自定义函数验证,1个单字段自定义方法验证
    sex = serializers.BooleanField(required=True)  # 一个必填的选项式验证
    # 两个选项式验证,1个单字段自定义方法验证，1个多字段验证
    age = serializers.IntegerField(max_value=150, min_value=0)
    # 以下2个字段是模型对象中没有的字段
    workingtime = serializers.ChoiceField(choices=choices)  # 1个选项式验证，一个多字段验证
    hobby = serializers.CharField(required=True)  # 一个必填的选项式验证，一个多字段自定义方法验证
    title = serializers.ChoiceField(choices=title_level)  # 1个选项式验证一个多字段自定义方法验证

    # part2. 可选【如果序列化器是继承ModelSerializer，则需要声明模型model和字段feilds
    # ModelSerializer是Serializer的子类】

    # part3. 可选【用于反序列化阶段对客户端提交的数据进行验证】
    """ 验证单个字段值得合法性 """

    def validate_name(self, data):
        if data == 'root':
            raise serializers.ValidationError('禁止向root用户提交数据')
        return data

    def validate_age(self, data):
        if data <= 18 and data >= 16:
            raise serializers.ValidationError('年龄不能在16~18岁')
        return data
    """ 验证多个字段的合法性 """

    def validate(self, attrs):
        name = attrs.get('name')
        age = attrs.get('age')
        workingtime = attrs.get('workingtime')
        hobby = attrs.get('hobby')
        title = attrs.get('title')
        if name == 'admin' and workingtime == 1:
            raise serializers.ValidationError('管理员上班时间禁止摸鱼！！')
        if age > 30 and '单身' in hobby:
            raise serializers.ValidationError('大龄青年不允许单身')
        if title <= 1 and '休息' in hobby:
            raise serializers.ValidationError('高级以上人员没有时间休息')
        return attrs
    # part4. 可选【用于把通过验证的数据进行数据库操作，保存到数据库。】


class Student4Serializer(serializers.Serializer):
    # 声明序列化器
    # part1. 字段声明【要转换的字段，如果在part2中使用Meta声明模型和字段后，可以不用写】
    # 声明什么，就序列化什么，换句话说，没有声明的字段即便模型中有也不会被序列化；
    # 如果字段已声明，即便模型中没有也会被序列化；数据提交验证通过后也不会进入到数据库中。
    # 以下三个字段是模型对象中有的字段
    name = serializers.CharField(max_length=10, min_length=4, validators=[
                                 check_user])  # 两个选项式验证，一个自定义函数验证,1个单字段自定义方法验证
    sex = serializers.BooleanField(required=True)  # 一个必填的选项式验证
    # 两个选项式验证,1个单字段自定义方法验证，1个多字段验证
    age = serializers.IntegerField(max_value=150, min_value=0)

    # 以下2个字段是模型对象中没有的字段
    workingtime = serializers.ChoiceField(
        choices=choices, default=1)  # 1个选项式验证，一个多字段验证
    hobby = serializers.CharField(default='muzhi')  # 一个必填的选项式验证，一个多字段自定义方法验证
    title = serializers.ChoiceField(
        choices=title_level, default=1)  # 1个选项式验证一个多字段自定义方法验证

    # part2. 可选【如果序列化器是继承ModelSerializer，则需要声明模型model和字段feilds
    # ModelSerializer是Serializer的子类】

    # part3. 可选【用于反序列化阶段对客户端提交的数据进行验证】
    """ 验证单个字段值得合法性 """

    def validate_name(self, data):
        if data == 'root':
            raise serializers.ValidationError('禁止向root用户提交数据')
        return data

    def validate_age(self, data):
        if data <= 18 and data >= 16:
            raise serializers.ValidationError('年龄不能在16~18岁')
        return data
    """ 验证多个字段的合法性 """

    def validate(self, attrs):
        print(attrs)
        name = attrs.get('name')
        age = attrs.get('age')
        workingtime = attrs.get('workingtime')
        hobby = attrs.get('hobby')
        title = attrs.get('title')
        if name == 'admin' and workingtime == 1:
            raise serializers.ValidationError('管理员上班时间禁止摸鱼！！')
        if age > 30 and '单身' in hobby:
            raise serializers.ValidationError('大龄青年不允许单身')
        if title <= 1 and '休息' in hobby:
            raise serializers.ValidationError('高级以上人员没有时间休息')
        return attrs
    # part4. 可选【用于把通过验证的数据进行数据库操作，保存到数据库。】

    def create(self, validated_data):
        """ 接收客户端提交的新增数据，不需要传入instance实例 """
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')
        # instance必须在create中创建，因为没有传入
        # 模型对象Student中未验证的其它字段，因为前端提交的数据没有，保存到数据库时，按默认值保存
        instance = Student.objects.create(name=name, age=age, sex=sex)
        # 如果采用全量的**validated_data来提交，因为验证的数据validated_data中包含Student中没有的字段，会报错：
        # Student() got unexpected keyword arguments: 'workingtime', 'hobby', 'title'
        # instance=Student.objects.create(**validated_data)
        # 查看已创建的对象实例
        print(instance)
        return instance

    def update(self, instance, validated_data):
        """ 用户反序列化对验证完成的数据进行保存更新，再传入instance实例后被调用 """
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')
        # 更新实例的值
        instance.name = name
        instance.age = age
        instance.sex = sex
        # 将实例保存到数据库
        instance.save()
        # 查看已创建的对象实例
        print(instance)
        return instance


""" 
开发中往往一个资源的序列化和反序列化阶段都是写在一个序列化器中
所以可以把两个阶段合并起来，以后再次写序列化器，则直接按照以下风格来编写
注：这里的合并是只接口形式合并，即针对不同请求方法，采用相同的接口，例如get所有数据和post数据
"""


class Student6Serializer(serializers.Serializer):
    # 声明序列化器
    # part1. 字段声明【要转换的字段，如果在part2中使用Meta声明模型和字段后，可以不用写】
    # 声明什么，就序列化什么，换句话说，没有声明的字段即便模型中有也不会被序列化；
    # 如果字段已声明，即便模型中没有也会被序列化；数据提交验证通过后也不会进入到数据库中。
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        max_length=10, min_length=4, validators=[check_user])
    sex = serializers.BooleanField(required=True)
    age = serializers.IntegerField(max_value=150, min_value=0)
    class_num = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

    # part2. 可选【如果序列化器是继承ModelSerializer，则需要声明模型model和字段feilds
# part3. 可选【用于反序列化阶段对客户端提交的数据进行验证】
    """ 验证单个字段值得合法性 """

    def validate_name(self, data):
        if data == 'root':
            raise serializers.ValidationError('禁止向root用户提交数据')
        return data

    def validate_age(self, data):
        if data <= 18 and data >= 16:
            raise serializers.ValidationError('年龄不能在16~18岁')
        return data
    """ 验证多个字段的合法性 """

    def validate(self, attrs):
        print(attrs)
        name = attrs.get('name')
        sex = attrs.get('sex')
        age = attrs.get('age')
        # workingtime = attrs.get('workingtime')
        # hobby = attrs.get('hobby')
        # title = attrs.get('title')
        # if name == 'admin' and workingtime == 1:
        #     raise serializers.ValidationError('管理员上班时间禁止摸鱼！！')
        # if age > 30 and '单身' in hobby:
        #     raise serializers.ValidationError('大龄青年不允许单身')
        # if title <= 1 and '休息' in hobby:
        #     raise serializers.ValidationError('高级以上人员没有时间休息')
        return attrs
    # part4. 可选【用于把通过验证的数据进行数据库操作，保存到数据库。】

    def create(self, validated_data):
        """ 接收客户端提交的新增数据，不需要传入instance实例 """
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')
        # instance必须在create中创建，因为没有传入
        # 模型对象Student中未验证的其它字段，因为前端提交的数据没有，保存到数据库时，按默认值保存
        instance = Student.objects.create(name=name, age=age, sex=sex)
        # 如果采用全量的**validated_data来提交，因为验证的数据validated_data中包含Student中没有的字段，会报错：
        # Student() got unexpected keyword arguments: 'workingtime', 'hobby', 'title'
        # instance=Student.objects.create(**validated_data)
        # 查看已创建的对象实例
        print(instance)
        return instance

    def update(self, instance, validated_data):
        """ 用户反序列化对验证完成的数据进行保存更新，再传入instance实例后被调用 """
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')
        # 更新实例的值
        instance.name = name
        instance.age = age
        instance.sex = sex
        # 将实例保存到数据库
        instance.save()
        # 查看已创建的对象实例
        print(instance)
        return instance


""" 
可以使用ModelSerializer来完成模型类序列化器的声明
基于ModelSerializer声明序列化器的好处：
1. 可以直接通过当前序列化器中指定的模型把在模型中已经声明的字段引用过来
2. ModelSerializer继承了Serializer的所有功能和方法，可以重写update和create方法
3. 模型中统一字段关于验证的选项，也会被序列化器复用，并作为选项参与验证
"""


class StudentModelSerializer(serializers.ModelSerializer):
    # 可以在此处声明is_18字段
    is_18 = serializers.BooleanField(default=1)

    class Meta:
        model = Student
        # fields = "__all__" # 模型中所有字段均从模型中引用
        # is_18为自定义字段，需要在models里面定义方法？def get_is_18()
        fields = ['id', 'name', 'age', 'sex', 'is_18']
        # exclude = ['age'] # 不包含某个字段
        # 传递额外的参数，为ModelSerializer添加或修改原来的选项参数
        extra_kwargs = {
            "name": {"max_length": 10, "min_length": 4, "validators": [check_user]},
            "age": {"max_value": 150, "min_value": 0}
        }

    def validtate_name(self, data):
        if data == "root":
            raise serializers.ValidationError("禁止向root提交数据")
        return data

    def validate(self, attrs):
        name = attrs.get('name')
        sex = attrs.get('sex')
        age = attrs.get('age')
        # 不需要提交到数据库，完成验证删除该字段即可
        del attrs['is_18']
        if name == "admin" and age >= 99:
            raise serializers.ValidationError("admin达到可以退休了")
        return attrs
