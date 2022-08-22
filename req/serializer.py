from students.models import Student
from rest_framework import serializers


class StudentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'sex']
        extra_kwargs = {
            "name": {"max_length": 10, "min_length": 4},
            "age": {"max_value": 150, "min_value": 0}
        }

    def validate_name(self, data):
        if data == "root":
            raise serializers.ValidationError("禁止向root提交数据")
        return data

    def validate(self, attrs):
        name = attrs.get("name")
        age = attrs.get('age')

        if name == "alex" and age == 22:
            raise serializers.ValidationError("alex已经22岁了……")
        return attrs
