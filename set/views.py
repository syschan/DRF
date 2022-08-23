""" ViewSet视图集，继承于APIView，所以APIView有的功能，它都有；此外还具有APIView不具备的功能
例如：ViewSetMixin中调用as_view()方法建立请求方法与自定义方法的映射关系。 
"""
from students.models import Student

from rest_framework.response import Response

from set.serializers import StudentInfoModelSerializer
from set.serializers import StudentModelSerializer

from rest_framework.generics import GenericAPIView

from rest_framework.mixins import ListModelMixin, CreateModelMixin

from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from rest_framework.decorators import action


class Student1ViewSet(ViewSet):
    def get_5(self, request):
        student_list = Student.objects.all()[0:5]
        serializer = StudentModelSerializer(instance=student_list, many=True)
        return Response(serializer.data)

    def get_one(self, request, pk):
        student_obj = Student.objects.get(pk=pk)
        serializer = StudentModelSerializer(instance=student_obj)
        return Response(serializer.data)

    def get_5_boy(self, request):
        student_list = Student.objects.filter(sex=True)[:5]
        serializer = StudentModelSerializer(instance=student_list, many=True)

        return Response(serializer.data)


""" 如果希望在视图集中调用GenericAPIView，则可以采用下面的方式 """


class Student2ViewSet(ViewSet, GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get_5(self, request):
        student_list = self.get_queryset()[:5]
        serializer = StudentModelSerializer(instance=student_list, many=True)

        return Response(serializer.data)

    def get_one(self, request, pk):
        student_obj = self.get_object()
        serializer = StudentModelSerializer(instance=student_obj)

        return Response(serializer.data)

    def get_5_boy(self, request):
        student_list = self.get_queryset().filter(sex=True)[:5]
        serializer = StudentModelSerializer(instance=student_list, many=True)

        return Response(serializer.data)


""" 上面的方式，虽然实现视图集中调用GenericAPIView，其实可以直接继承GenericViewSet """


class Student3GenericViewSet(GenericViewSet):
    serializer_class = StudentModelSerializer
    queryset = Student.objects.all()

    def get_5(self, request):
        student_list = self.get_queryset()[:5]
        serializer = self.get_serializer(instance=student_list, many=True)

        return Response(serializer.data)

    def get_5_boy(self, request):
        student_list = self.get_queryset().filter(sex=True)[:5]
        serializer = self.get_serializer(instance=student_list, many=True)

        return Response(serializer.data)


""" 可以通过同时继承GenericViewSet和XModelMixin，自动调用已封装好的X()方法，根据需要快速生成API的组合"""


class Student4GenericViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    serializer_class = StudentModelSerializer
    queryset = Student.objects.all()


""" 也可以通过直接继承ModelViewSet一次性生成5个API """


class Student5ModelViewSet(ModelViewSet):
    serializer_class = StudentModelSerializer
    queryset = Student.objects.all()


""" 只读模型视图集 """


class Student6ReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


""" 路由的使用 """


class Student7ModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    # methods 指定哪些http请求可以访问当前视图
    # detail 指定生成的路由地址中是否要带有pk值，true为需要

    # 重写了url_path原来的get_6就失效了，即当detail=True时优先级url_path覆盖get_6,且url_name不可用
    # @action(methods=['get'],detail=True,url_name='get_girl',url_path='get_MM')
    @action(methods=['get'], detail=False)
    def get_4(self, request):
        print(self.action)
        serializer = self.get_serializer(
            instance=self.get_queryset().get(pk=4))

        return Response(serializer.data)

    # @action(methods=['post'],detail=False,url_path='you')
    # .../login/
    @action(methods=['post'], detail=False)
    def login(self, request):
        # 如果用户名唯一,课使用username对queryset进行过滤；如果不唯一，则需要使用id字段来过滤；否则会报错
        username = request.data['name']
        serializer = self.get_serializer(
            instance=self.get_queryset().get(name=username))
        # return Response({"msg":"ok"})
        # 自定义返回格式
        res = {
            "msg": "登录成功！",
            "code": '200',
            'data': {
                'flag': True,
                "data": serializer.data
            }
        }
        return Response(res)


""" 在多个视图类合并成一个视图类以后，有时会出现一个类中需要调用多个序列化器 """
""" 1 在视图类中重写get_serializer_class方法调用多个序列化器,默认是一个视图类调用一个序列化器 """


class Student8GenericAPIView(GenericAPIView):
    queryset = Student.objects.all()

    # GenericAPIView内部调用序列化器的方法，重写序列化器类
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StudentInfoModelSerializer
        return StudentModelSerializer

    def get(self, request):
        """ 获取所有数据的id和name """
        student_list = self.get_queryset()
        serializer = self.get_serializer(instance=student_list, many=True)

        return Response(serializer.data)

    def post(self, request):
        """ 添加1条数据 """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


""" 2 在视图集中调用多个序列化器类 """


class Student9ModelViewSet(ModelViewSet):
    queryset = Student.objects.all()

    """ 
    要求：
    列表数据list，返回2个字段
    详情数据retrieve，返回所有字段
    """
    # 重写get_serializer_class方法

    def get_serializer_class(self):
        print('当前请求方法=>', self.request.method)
        if self.action == 'list':
            return StudentInfoModelSerializer
        return StudentModelSerializer
