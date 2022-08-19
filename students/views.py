from rest_framework.viewsets import ModelViewSet
from students.models import Student
from students.serializers import StudentModelSerializer


class StudentAPIView(ModelViewSet):
    # queryset指明该视图集在查询时使用的查询集
    queryset = Student.objects.all()
    # serialzer_class 指明该视图在进行序列化或反序列化时使用的序列化器
    serializer_class = StudentModelSerializer
