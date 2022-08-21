# from django.shortcuts import render

# # Create your views here.

import json
from .serializers import Student3Serializer,Student4Serializer, Student6Serializer,StudentModelSerializer
from django.views import View  # 导入需要继承的视图类
from students.models import Student  # 导入模型类
from .serializers import StudentSerializer  # 导入所序列化器类
from django.http import JsonResponse

from ser import serializers  # 导入原生Django的json响应函数


class Student1View(View):  # 生成一个继承至View的视图类，get方法获取1条数据
    """ 使用序列化器类进行数据的序列化操作 """
    """ =====序列化器转换1条数据【将模型转换为字典】======= """
    # 定义get方法的四部曲
    # step1：接受前端发过来的request和pk

    def get(self, request, pk):
        # step2：根据客户端传过来的参数，通过查询参数pk进行过滤查询，得到实例化的【queryset】学生对象
        student = Student.objects.get(pk=pk)
        # step3：实例化序列化器类，转换【queryset对象】为数据类型【有序字典格式的serializer.data】
        # 3.1 实例化序列号器类
        """ 
            StudentSerializer(instance=实例化的模型对象或模型对象对象列表,data=客户端提交的数据request.data(一般为json格式或文本格式),context=额外要传递到序列化器中使用的其它数据)
        """
        serializer = StudentSerializer(instance=student)

        # 3.2 查看序列化转换结果
        print(serializer.data)
        # {'id': 2, 
        # 'name': 'admin', 
        # 'sex': True, 
        # 'age': 20,
        # 'class_num': '9527', 
        # 'description': '9527!!!'}
        # step4：向前端返回JsonResponse
        return JsonResponse(serializer.data)

# 如果要被序列化的是包含多条数据的查询集QuerySet，可以通过添加many=True参数补充说明。


class Student2View(View):  # 生成一个继承至View的视图类，get方法获取多条数据
    """ 使用序列化器类进行数据的序列化操作 """
    """ =====序列化器转换多条数据【将模型转换为字典】======= """
    # 定义get方法的四部曲
    # step1：接受前端发过来的request

    def get(self, request):
        # step2：根据客户端传过来的参数，通过查询参数pk进行过滤查询，得到实例化的【queryset】学生对象
        # 获取多条数据，实例化出来的是一个queryset对象的list
        student_list = Student.objects.all()
        # step3：实例化序列化器类，转换【queryset对象list】为数据类型【有序字典格式的serializer.data】
        # 3.1 实例化序列号器类
        """ 
            StudentSerializer(instance=实例化的模型对象或模型对象对象列表,data=客户端提交的数据request.data(一般为json格式或文本格式),context=额外要传递到序列化器中使用的其它数据)
            当instance的参数是一个list的queryset时,需要设置参数many=True
        """
        serializer = StudentSerializer(instance=student_list, many=True)

        # 3.2 查看序列化转换结果,此处的data是一个有序字典的list
        print(serializer.data)
        # [OrderedDict([('id', 2), ('name', 'admin'), ('sex', True), ('age', 20), ('class_num', '9527'), ('description', '9527！！---就是我啦')]), 
        # OrderedDict([('id', 3), ('name', 'baby'), ('sex', True), ('age', 22), ('class_num', '1312'), ('description', 'baby,baby!!')])]
        # step4：向前端返回JsonResponse,必须设置非字典对象允许被序列化！！！
        return JsonResponse(serializer.data, safe=False)


class Student3View(View):
    def post(self, request):
        data = request.body.decode()
        # 反序列化用户提交的数据
        data_dic = json.loads(data)

        # 调用序列化器进行实例化,post方法接受一个数据，因此不需要many=True
        serializer = Student3Serializer(data=data_dic)
        # is_valid()函数在执行的时候，会先自动调用字段的内置选项、自定义方法、自定义validator验证函数
        # 在执行验证代码时，rase_exception=True抛出验证错误信息，并阻止代码继续运行
        # 查看验证结果
        print(serializer.is_valid(raise_exception=False))

        # 查看验证后的错误信息
        print(serializer.errors)

        #获取验证后客户端提交的数据
        print(serializer.validated_data)

        # 向前端返回JsonResponse
        return JsonResponse(serializer.validated_data)
        # 返回serializer.validated_data和serializer.data没有区别
        #return JsonResponse(serializer.data)


class Student4View(View):
    def post(self, request):
        data = request.body.decode()
        # 反序列化用户提交的数据
        data_dic = json.loads(data)

        # 调用序列化器进行实例化,post方法接受一个数据，因此不需要many=True
        serializer = Student4Serializer(data=data_dic)
        # is_valid()函数在执行的时候，会先自动调用字段的内置选项、自定义方法、自定义validator验证函数
        # 在执行验证代码时，rase_exception=True抛出验证错误信息，并阻止代码继续运行
        # 查看验证结果
        print(serializer.is_valid(raise_exception=False))

        # 查看验证后的错误信息
        print(serializer.errors)

        #获取验证后客户端提交的数据
        print(serializer.validated_data)

        # 序列化阶段只传了data=data_dic，所以调用save方法只会执行序列化器中的反序列create代码，instance在create中创建
        serializer.save()

        # 向前端返回JsonResponse
        return JsonResponse(serializer.validated_data)

        # ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        # serializer.data=>序列化阶段：序列化器定义的所有字段，包括在模型对象中需要验证的部分字段和不在模型对象中需要验证的字段，序列化器按照该字段向模型对象取数据；如果字段不在模型对象中，有默认值值返回默认值，没有默认值则报错；与前端是否提交该字段无关
        # serializer.validated_data=>反序列化阶段：序列化器定义的所有字段，包括前端提交的部分字段和前端未提交的部分字段，经过序列化器验证过后的字段，序列化器向前端取数据；如果字段不在提交数据中，有默认值返回默认值，没有默认值，按校验规则报错或者填充值；不依赖于模型对象的字段。
        # 返回serializer.validated_data和serializer.data有区别,serializer.data按照序列化器中的字段从数据库中取数，如果序列化器中的字段包含Student对象中没有的字段且有无法正常补全则会报错。
        # 如果post提交的字段全部是Student对象中声明的字段，就不会报错，而且是按照序列化器中的字段来返回，二者就没有区别了。
        #return JsonResponse(serializer.data)
        # ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

class Student5View(View):
    def put(self, request,pk):
        data = request.body.decode()
        # 反序列化用户提交的数据
        data_dic = json.loads(data)
        # 通过参数参数获得查询对象
        student_obj=Student.objects.get(pk=pk)

        # 调用序列化器进行实例化,post方法接受一个数据，因此不需要many=True
        serializer = Student4Serializer(instance=student_obj,data=data_dic)
        # is_valid()函数在执行的时候，会先自动调用字段的内置选项、自定义方法、自定义validator验证函数
        # 在执行验证代码时，rase_exception=True抛出验证错误信息，并阻止代码继续运行
        # 查看验证结果
        print(serializer.is_valid(raise_exception=False))

        # 查看验证后的错误信息
        print(serializer.errors)

        #获取验证后客户端提交的数据
        print(serializer.validated_data)

        # 序列化阶段传入了student_obj实例，所以调用save方法只会执行序列化器中的反序列update代码
        serializer.save()

        # 向前端返回JsonResponse
        return JsonResponse(serializer.validated_data)

class Student6View(View):
    # 四部曲
    # step1：接受前端发过来的request
    def get(self,request):
        #获取所有数据
        # step2：根据客户端传过来的参数，通过查询参数pk进行过滤查询，得到实例化的【queryset】学生对象
        # 获取多条数据，实例化出来的是一个queryset对象的list
        student_list= Student.objects.all()

        # step3：实例化序列化器类，转换【queryset对象list】为数据类型【有序字典格式的serializer.data】
        serializer=Student6Serializer(instance=student_list,many=True)

        # step4：向前端返回JsonResponse,必须设置非字典对象允许被序列化！！！
        #return JsonResponse(serializer.validated_data,safe=False)
        # 返回serializer.validated_data和serializer.data有区别，因为没有调用is_valid()，所以不会产生validated_data
        return JsonResponse(serializer.data,safe=False)      

    def post(self,request):
        data=request.body.decode()
        data_dic=json.loads(data)

        serializer=Student6Serializer(data=data_dic)
        # 查看验证结果
        print(serializer.is_valid(raise_exception=False))
        # 查看保存提交结果
        instance = serializer.save()
        print(instance)
        return JsonResponse(serializer.validated_data)
        # 返回serializer.validated_data和serializer.data无区别(data会把id返回来)
        #return JsonResponse(serializer.data)   

class Student7View(View):
    def get(self,request):
        student_list=Student.objects.all()
        serializer = StudentModelSerializer(instance=student_list,many=True)
        return JsonResponse(serializer.data,safe=False)

    def post(self, request):
        data = request.body.decode()
        data_dic=json.loads(data)
        serializer= StudentModelSerializer(data=data_dic)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)