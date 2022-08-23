from rest_framework import serializers
from students.models import Student


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
class StudentModelSerializer(serializers.ModelSerializer):


    class Meta:
        model = Student
        # fields = "__all__" # 模型中所有字段均从模型中引用
        fields = ['id', 'name', 'age', 'sex']
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

        if name == "admin" and age >= 99:
            raise serializers.ValidationError("admin达到可以退休了")
        return attrs

class StudentInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model =Student
        fields = ['id', 'name']