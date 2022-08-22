""" 测试代码：区分Django的View和DRF的APIView """
from django.views import View
from django.http import JsonResponse

from req import serializer

class Student1View(View):
    def get(self,request):
        print(request) # 这是Django提供的HttpRequest类
        # <WSGIRequest: GET '/req/student1/'>
        print(request.GET)
        # <QueryDict: {'username': ['admin'], 'pwd': ['110']}>
        data_dic = {'name':"alex", 'age':18}

        return JsonResponse(data=data_dic)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class Student2APIView(APIView):
    def get(self, request):
        print(request) # 这是rest_framework扩展的request
        # <rest_framework.request.Request: GET '/req/student2/?username=admin&pwd=110'>
        print(request.query_params)
        # <QueryDict: {'username': ['admin'], 'pwd': ['110']}>
        print(request.data)
        # {'name': '我是大白兔', 'age': 26, 'sex': True}

        data_dic = {'name':"alex", 'age':18}

        return Response(data=data_dic,status=status.HTTP_204_NO_CONTENT,headers={'self':'TomK'})

"""
使用APIView提供学生信息的5个API接口
GET    /req/student3/               # 获取全部数据
POST   /req/student3/               # 添加数据

GET    /req/student3/(?P<pk>\d+)    # 获取一条数据
PUT    /req/student3/(?P<pk>\d+)    # 更新一条数据
DELETE /req/student3/(?P<pk>\d+)    # 删除一条数据
"""

from students.models import Student
from req.serializer import StudentModelSerializer


class Student3APIView(APIView):
    def get(self, request):
        """ 获取所有数据 """
        student_list = Student.objects.all()
        # 实例化序列化器类
        serializer =StudentModelSerializer(instance=student_list,many= True)

        return Response(serializer.data)

    def post(self,request):
        # 获取用户提交的数据
        data_dic= request.data
        # 实例化序列化器类
        serializer = StudentModelSerializer(data= data_dic)
        # 数据校验
        serializer.is_valid(raise_exception=True)
        # 保存数据到数据库
        serializer.save()

        return Response(serializer.validated_data)

class Student4APIView(APIView):
    def get(self,request,pk):
        #通过pk值过滤模型对象
        student_obj = Student.objects.get(pk=pk)

        #实例化序列化器类
        serializer = StudentModelSerializer(instance=student_obj)

        return Response(serializer.data)

    def put(self,request,pk):
        # 获取前端提交的数据
        data_dic = request.data
        # 通过pk值过滤模型对象
        student_obj= Student.objects.get(pk=pk)
        
        #实例化序列化器类
        serializer = StudentModelSerializer(instance=student_obj,data=data_dic)

        # 数据校验
        serializer.is_valid(raise_exception=True)

        #数据保存
        serializer.save()

        return Response(serializer.validated_data)

    def delete(self,request,pk):
        # 通过pk过滤模型对象
        Student.objects.get(pk=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
使用GenericAPIView提供学生信息的5个API接口
GET    /req/student5/               # 获取全部数据
POST   /req/student5/               # 添加数据

GET    /req/student6/(?P<pk>\d+)    # 获取一条数据
PUT    /req/student6/(?P<pk>\d+)    # 更新一条数据
DELETE /req/student6/(?P<pk>\d+)    # 删除一条数据
"""
from rest_framework.generics import GenericAPIView


class Student5GenericAPIView(GenericAPIView):
    #当前视图类中操作的公共数据，先从数据库查询出来
    queryset = Student.objects.all()
    #设置类视图中所有方法共有调用的序列化器类
    serializer_class = StudentModelSerializer

    def get(self, request):
        # 获取模型数据
        student_list=self.get_queryset()

        # 调用序列化器
        serializer = self.get_serializer(instance = student_list, many = True)

        return Response(serializer.data)

    def post(self, request):
        # 新增1条数据
        # 获取客户端提交的数据并实例化序列化器
        serializer = self.get_serializer(data=request.data)
        #数据校验
        #方式1：raise_exception=False自定义错误、状态信息、headers等返回的数据格式
        if not serializer.is_valid(raise_exception=False):
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            # 保存数据到数据库
            serializer.save()
            
            return Response(serializer.validated_data)

class Student6GenericAPIView(GenericAPIView):
    #当前视图类中操作的公共数据，先从数据库查询出来
    queryset = Student.objects.all()
    #设置类视图中所有方法共有调用的序列化器类
    serializer_class = StudentModelSerializer

    def get(self,request,pk):
        """ 参数pk是固定名称 """
        # 获取1个模型对象，调用get_object()方法
        student_obj = self.get_object()
        #实例化序列化器对象
        serializer = self.get_serializer(instance=student_obj)

        return Response(serializer.data)

    def put(self, request, pk):
        student_obj= self.get_object()
        #获取前端数据并实例化序列化器对象
        serializer = self.get_serializer(instance = student_obj, data = request.data)
        #数据校验
        #方式2：raise_exception = True，验证不通过自动把错误信息返回给前端，后续代码不再继续执行
        serializer.is_valid(raise_exception = True)
        #数据保存
        serializer.save()

        return Response(serializer.Validated_data)

    def delete(self,request,pk):
        #通过pk获取对象并删除
        self.get_object().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        #或者自定义返回
        # instance = self.get_object()
        # serializer = self.get_serializer(instance=instance)
        # instance.delete()
        #return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)
"""
使用GenericAPIView结合视图Mixin扩展类，快速实现数据接口的APIView
ListModelMixin      实现查询所有数据功能
CreateModelMixin    实现添加数据的功能
RetrieveModelMixin  实现查询一条数据功能
UpdateModelMixin    更新一条数据的功能
DestroyModelMixin   删除一条数据的功能
"""
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin,UpdateModelMixin,ListModelMixin,RetrieveModelMixin


class Student7GenericAPIView(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self,request):
        return self.list(request)

    def post(self,request):
        return self.create(request)

class Student8GenericAPIView(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self,request,pk):
        return self.retrieve(request,pk)

    def put(self,request,pk):
        return self.update(request,pk)

    def delete(self,request,pk):
        return self.destroy(request,pk)

"""
DRF里面，内置了一些同时继承了GenericAPIView和Mixins扩展类的视图子类，
我们可以直接继承这些子类就可以生成对应的API接口
"""

"""
ListAPIView      获取所有数据
CreateAPIView    添加数据
ListAPIView是GenericAPIView和ListMixinMode的多继承，该视图类内置了：
def get(self,request):
    return self.list(request)
CreateAPIView是GenericAPIView和CreateMinxinMode的多继承，该视图类内置了：
def post(self,request):
    return self.create(request)
    ....
"""


#分别导入2个单一的视图扩展子类实现查所有数据的ListAPIView和新增1条数据的CreateAPIView
from rest_framework.generics import ListAPIView,CreateAPIView
#等价于导入1个组合的视图扩展子类ListCreateAPIView
#from rest_framework.generics import ListCreateAPIView

class Student9GenericAPIView(ListAPIView,CreateAPIView):
#等价于继承ListCreateAPIView组合的视图扩展子类
#class Student9GenericAPIView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


"""
RetrieveAPIView                 获取一条数据
UpdateAPIView                   更新一条数据
DestorAPIView                   删除一条数据
RetrieveUpdateDestoryAPIView    上面三个的缩写
"""


#分别导入3个单一的视图扩展子类实现查1条数据的RetrieveAPIView、更新1条数据的UpdateAPIView和删除1条数据的DestroyAPIView
from rest_framework.generics import RetrieveAPIView,UpdateAPIView,DestroyAPIView
#等价于导入1个组合的视图扩展子类RetrieveUpdateDestroyAPIView
# from rest_framework.generics import RetrieveUpdateDestroyAPIView


class Student10GenericAPIView(RetrieveAPIView,UpdateAPIView,DestroyAPIView):
#等价于继承RetrieveUpdateDestroyAPIView组合的视图扩展子类
#class Student10GenericAPIView(RetrieveUpdateDestroyAPIView):


    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

"""
视图集
上面５个接口使用了８行代码生成，但是我们可以发现有一半的代码重复了
所以，我们要把这些重复的代码进行整合，但是依靠原来的类视图，其实有２方面产生冲突的
1. 查询所有数据、添加数据是不需要声明pk的，而其他的接口需要    [路由冲突了]
2. 查询所有数据和查询一条数据，都是属于get请求                 [请求方法冲突了]
为了解决上面的２个问题，所以DRF提供了视图集来解决这个问题
"""
# 分别导入GenericViewSet和5个XModeMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin



# 可以根据需要，同时继承GenericViewSet和XModeMixin中的一个或多个；如果同时继承5个XModeMixin
class Student11GenericViewSet(GenericViewSet,ListModelMixin,CreateModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):

    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    
#以上GenericViewSet+5个XModeMixin
# 等价于导入
from rest_framework.viewsets import ModelViewSet
#等价于继承ModelViewSet
class Student12ModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer