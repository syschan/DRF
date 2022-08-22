一 环境准备
1. shell管理员安装virtualenv
pip install virtualenv

2. 创建目录
mkdir DRF
cd DRF

3. 创建独立运行环境-命名
virtualenv drfplus 

4. 进入虚拟环境
 source drfplus/Scripts/activate

5. 安装第三方包
#如果卡就切换源
#pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

5.1  选择单个安装
pip install django
pip install djangorestframework
pip install pymysql
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install mysqlclient
...

5.2 或者批量安装
pip install -r requirements.txt

二 项目初始化
1. 创建一个Django项目
...DRF>django-admin startproject drfdemo

2. 添加rest_framework应用
<!-- 切换到项目目录 -->
...DRF>cd drfdemo
<!-- 在vscode中打开项目 -->
...DRF\drfdemo>code .
在settings.py的INSTALLED_APPS中添加'rest_framework'
=========
INSTALLED_APPS = [
    ...
    'rest_framework',
    ...
]
=========
3. 语言和时区设置
=========
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
=========
4. 数据库配置
=========
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'drf_db',  # 数据库名称
        'USER': 'root',  # 用户名
        'PASSWORD': '123',  # 密码
        'HOST': '127.0.0.1',  # 数据库主机
        'PORT': 3306,  # 数据库端口
    }
}
=========
cmd命令窗口：
...>mysql -u root -p
输入登录密码123
(如果没有按照mysql需提前安装，安装方法直接百度)

创建drf_db数据库
mysql>CREATE DATABASE drf_db;


三 快速生成API接口示例
在项目中如果使用rest_framework框架实现API接口，主要有以下三个步骤：
--将请求的数据（如JSON格式）转换为模型类对象=>反序列化
--操作数据库
--将模型类对象转换为响应的数据（如JSON格式）=>序列化

1. 创建app和模型类
...DRF\drfdemo>python manage.py startapp students
在settings.py的INSTALLED_APPS中添加'students'
=========
INSTALLED_APPS = [
    ...
    'rest_framework',
    'students',
    ...
]
=========
在...DRF\drfdemo\students\models.py中：
=========
from django.db import models


class Student(models.Model):
    # 模型字段
    name = models.CharField(max_length=100, verbose_name='姓名')
    sex = models.BooleanField(default=1, verbose_name='性别')
    age = models.IntegerField(verbose_name='年龄')
    class_num = models.CharField(max_length=5, verbose_name='班级编号')
    description = models.TextField(max_length=100, verbose_name='个性签名')

    class Meta:
        db_table = "tb_student" #在数据库中创建名为tb_student的数据表
        verbose_name = "学生"
        verbose_name_plural = verbose_name

=========

2. 创建序列化器
在...DRF\drfdemo\students\应用目录中新建serializers.py用于保存该应用的序列化器。
在serializers.py中创建一个StudentModelSerializer用于序列化与反序列化。
=========
from rest_framework import serializers
from students.models import Student


 
class StudentModelSerializer(serializers.ModelSerializer):
    # 创建序列化器类，以便在views.py中被调用
    class Meta:
        model = Student  # model指明序列化器处理的数据字段从模型类Student中参考生成
        fields = '__all__'  # fields指明该序列化器包含模型类中的哪些字段，__all__表示所有字段
        # 补充：
        # 如果fields = ['name','sex']，则视图views中序列化后就只能显示name和sex字段
=========
注意：
序列化器类继承的是serializers.ModelSerializer，不是serializers.Serializer；如果继承后者，post提交数据会报错需要create(),因为Serializer中的post方法并没有调用create()，create方法是ListViews中的方法，ModelViewSet中继承了ListViews中具有该方法。

3. 编写视图
在...DRF\drfdemo\students应用的views.py中创建视图StudentViewSet，这是一个视图集合。
=========
from rest_framework.viewsets import ModelViewSet
from students.models import Student
from students.serializers import StudentModelSerializer


class StudentAPIView(ModelViewSet):
    # queryset指明该视图集在查询时使用的查询集
    queryset = Student.objects.all()
    # serialzer_class 指明该视图在进行序列化或反序列化时使用的序列化器
    serializer_class = StudentModelSerializer
==========
4. 定义路由
在...DRF\drfdemo\students应用新建urls.py并定义路由信息
==========
from rest_framework.routers import DefaultRouter
from students import views

urlpatterns = []  # Django的路由表

router = DefaultRouter()  # 可以处理视图的路由器

router.register('students', views.StudentAPIView)  # url关联视图，此处的路径students可以根据自己的需要来定制，和创建的students应用没有绑定。

urlpatterns += router.urls  # 将路由器中的所有路由信息追加到Django的路由表中
==========
注意：此处的urlpatterns是固定的，而且只能是urlpatterns，必须与总路由总的urlpatterns保持一致。

最后把...DRF\drfdemo\students子应用中的路由文件加载到...DRF\drfdemo总路由文件urls.py中.
==========
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('drf/', include('students.urls'))
]
==========
注意：include('students.urls')中的students是和应用有绑定的，students.urls就是去关联students应用下的urls.py文件，从而让该文件中的路由能够顺利追加到总路由

5. 数据库迁移
(注意数据库账号和密码，要和设置的保持一致)
...DRF\drfdemo>python manage.py makemigrations

...DRF\drfdemo>python manage.py migrate

6. 启动服务器
...DRF\drfdemo>python manage.py runserver 0.0.0.0:8000

增：
post=>http://localhost:8000/drf/students/
request.body=>
========
    {"name":"tellyoumore",
    "age":28,
    "sex":true,
    "class_num":"1023",
    "description":"超级管理员！！"
    }
========
返回：
response.body=>
========
    {"id":1,
    "name":"tellyoumore",
    "age":28,
    "sex":true,
    "class_num":"1023",
    "description":"超级管理员！！"
    }
========

post=>http://localhost:8000/drf/students/
request.body=>
========
    {
        "name": "admin",
        "sex": true,
        "age": 20,
        "class_num": "9527",
        "description": "9527！！"
    }
========
返回：
response.body=>
========
    {
        "id": 2,
        "name": "admin",
        "sex": true,
        "age": 20,
        "class_num": "9527",
        "description": "9527！！"
    }
========
删：
delete=>http://localhost:8000/drf/students/1/

查：
get=>http://localhost:8000/drf/students/2/
返回：
response.body=>
========
    {
        "id": 2,
        "name": "admin",
        "sex": true,
        "age": 20,
        "class_num": "9527",
        "description": "9527！！"
    }
========
改：
put=>http://localhost:8000/drf/students/2/
request.body=>
========
    {
        "name": "admin",
        "sex": true,
        "age": 20,
        "class_num": "9527",
        "description": "9527！！---就是我啦"
    }
========
返回：
response.body=>
========
{
    "id": 2,
    "name": "admin",
    "sex": true,
    "age": 20,
    "class_num": "9527",
    "description": "9527！！---就是我啦"
}
========
说明：
以上请求均是通过DRF的web浏览器发起的，由于在没有使用modelserializer前浏览器在get单条数据时无法让body带数据提交，后面演示不友善或者无法演示，所以后续发起请求均在postman中发起。
postman下载地址：https://dl.pstmn.io/download/latest/win64

四 序列化器Serializer
<!-- 作用：
序列化------序列化器会把模型对象转换成字典,经过response以后变成json字符串
反序列化----把客户端发送过来的数据,经过request以后变成字典,序列化器可以把字典转成模型
反序列化----完成数据校验功能 -->

1. 定义序列化器
Django REST framework中的Serializer使用类来定义，须继承自rest_framework.serializers.Serializer
1.1 创建一个新的子应用ser
...DRF\drfdemo>python manage.py startapp ser
1.2 在settings.py的INSTALLED_APPS中添加'ser'
=========
INSTALLED_APPS = [
    ...
    'rest_framework',
    'students',
    'ser',
    ...
]
=========
1.3 模型类
继续使用students应用中的模型student，暂不新建模型
1.4 创建序列化器
在...DRF\drfdemo\ser\应用目录中新建serializers.py用于保存该应用的序列化器。
在serializers.py中创建一个StudentSerializer用于序列化与反序列化。
=========
from rest_framework import serializers

    #所有自定义序列化器必须直接或者间接继承于serializers.Serializer
class StudentSerializer(serializers.Serializer):
    # 声明序列化器
    # part1. 字段声明【要转换的字段，如果在part2中使用Meta声明模型和字段后，可以不用写】
    id = serializers.IntegerField()
    name = serializers.CharField()
    sex = serializers.BooleanField()
    age = serializers.IntegerField()
    class_num = serializers.CharField()
    description = serializers.CharField()

    # part2. 可选【如果序列化器是继承ModelSerializer，则需要声明模型model和字段feilds,ModelSerializer是Serializer的子类】
    
    # part3. 可选【用于反序列化阶段对客户端提交的数据进行验证】

    # part4. 可选【用于把通过验证的数据进行数据库操作，保存到数据库。】

    # ！！！注意：serializer不是只能为数据库模型类定义，也可以为非数据库模型类的数据定义。serializer是独立于数据库之外的存在。
=========
-----常用字段类型：
字段	            字段构造方式
BooleanField	    BooleanField()
NullBooleanField	NullBooleanField()
CharField	        CharField(max_length=None, min_length=None, allow_blank=False, trim_whitespace=True)
EmailField	        EmailField(max_length=None, min_length=None, allow_blank=False)
RegexField	        RegexField(regex, max_length=None, min_length=None, allow_blank=False)
SlugField	        SlugField(maxlength=50, min_length=None, allow_blank=False) 正则字段，验证正则模式 [a-zA-Z0-9-]+
URLField	        URLField(max_length=200, min_length=None, allow_blank=False)
UUIDField	        UUIDField(format='hex_verbose') format:1)'hex_verbose'如"5ce0e9a5-5ffa-654b-cee0-1238041fb31a"2）'hex' 如 "5ce0e9a55ffa654bcee01238041fb31a"3）'int' 如:"123456789012312313134124512351145145114"4）'urn' 如:"urn:uuid:5ce0e9a5-5ffa-654b-cee0-1238041fb31a"
IPAddressField	    IPAddressField(protocol='both', unpack_ipv4=False, **options)
IntegerField	    IntegerField(max_value=None, min_value=None)
FloatField	        FloatField(max_value=None, min_value=None)
DecimalField	    DecimalField(max_digits, decimal_places, coerce_to_string=None, max_value=None, min_value=None) max_digits: 最多位数 decimal_palces: 小数点位置
DateTimeField	    DateTimeField(format=api_settings.DATETIME_FORMAT, input_formats=None)
DateField	        DateField(format=api_settings.DATE_FORMAT, input_formats=None)
TimeField	        TimeField(format=api_settings.TIME_FORMAT, input_formats=None)
DurationField	    DurationField()
ChoiceField	        ChoiceField(choices) choices与Django的用法相同
MultipleChoiceField	MultipleChoiceField(choices)
FileField	        FileField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)
ImageField	        ImageField(max_length=None, allow_empty_file=False, use_url=UPLOADED_FILES_USE_URL)
ListField	        ListField(child=, min_length=None, max_length=None)
DictField	        DictField(child=)
-----选项参数：
参数名称	    作用
max_length	    最大长度
min_lenght	    最小长度
allow_blank	    是否允许为空
trim_whitespace	是否截断空白字符
max_value	    最大值
min_value	    最小值

-----通用参数：
参数名称	    说明
read_only	    表明该字段仅用于序列化输出，默认False
write_only	    表明该字段仅用于反序列化输入，默认False
required	    表明该字段在反序列化时必须输入，默认True
default	        反序列化时使用的默认值
allow_null	    表明该字段是否允许传入None，默认False
validators	    该字段使用的验证器
error_messages	包含错误编号与错误信息的字典
label	        用于HTML展示API页面时，显示的字段名称
help_text	    用于HTML展示API页面时，显示的字段帮助提示信息

2. 创建Serializer对象=>python字典
定义好Serializer类后，就可以创建Serializer对象了。Serializer的构造方法为：
    serializer=Serializer(instance=None, data=empty, **kwarg)
        ↑↑      ↑↑          ↑↑              ↑↑           ↑↑
    序列化对象=序列化器类(模型对象实例,    反序列化数据,   额外参数)
                            ↑↑              ↑↑
                        序列化阶段      反序列化阶段request.body.data

说明：
　　　　1）用于序列化时，将模型类对象传入instance参数

　　　　2）用于反序列化时，将要被反序列化的数据传入data参数

　　　　3）除了instance和data参数外，在构造Serializer对象时，还可通过context参数额外添加数据，如
    serializer = StudentSerializer(student, context={'request': request})
通过context参数附加的数据，可以通过Serializer对象的context属性获取。

声明：
----使用序列化器的时候一定要注意，序列化器声明了以后，不会自动执行，需要我们在视图中进行调用才可以。
----序列化器无法直接接收数据，需要我们在视图中创建序列化器对象时把使用的数据传递过来。
----序列化器的字段声明类似于我们前面使用过的表单系统。
----开发restful api时，序列化器会帮我们把模型数据转换成字典.
----drf提供的视图会帮我们把字典转换成json,或者把客户端发送过来的数据转换字典.

3. 序列化器的使用
　　序列化器的使用分两个阶段：

    前端=>后端：在客户端请求时，使用序列化器可以完成对数据的【反序列化】。
    后端=>前端: 在服务器响应时，使用序列化器可以完成对数据的【序列化】。
3.1 序列化示例1
3.1.1 创建视图类
...DRF\drfdemo\ser应用下的views.py文件中：
=====
from django.views import View # 导入需要继承的视图类
from students.models import Student # 导入模型类
from .serializers import StudentSerializer #导入所序列化器类
from django.http import JsonResponse #导入原生Django的json响应函数

class Student1View(View): #生成一个继承至View的视图类，get方法获取1条数据
    """ 使用序列化器类进行数据的序列化操作 """
    """ =====序列化器转换1条数据【将模型转换为字典】======= """
    # 定义get方法的四部曲
        # step1：接受前端发过来的request和pk
    def get(self,request,pk):
        # step2：根据客户端传过来的参数，通过查询参数pk进行过滤查询，得到实例化的【queryset】学生对象
        student=Student.objects.get(pk=pk)
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
=====
3.1.2 创建子路由
...DRF\drfdemo\ser下新建urls.py文件，调用视图类的as_view()方法：
=====
from django.urls import path, re_path
from . import views


# 创建子路由，关联路径和视图
urlpatterns = [
    # ..1..
    # 方法：get方法获取1条数据，带pk;
    # 模型：采用的是students下的Student模型对象;
    # 序列化器：序列化器类StudentSerializer继承至serializers.Serializer序列化器类;
    # 视图：继承的Django原生视图类View
    re_path(r'^student1/(?P<pk>\d+)/$', views.Student1View.as_view())
]

=====

3.1.3 将子路由追加到总路由
=====
urlpatterns = [
    path('admin/', admin.site.urls),
    path('drf/', include('students.urls')),
    path('ser/', include('ser.urls')),#追加ser应用的子路由urls.py到总路由
]
=====
3.1.4 发送get请求
查(postman)：
get=>http://localhost:8000/ser/student1/2/
返回(postman)：
response.body=>
========
{
    "id": 2,
    "name": "admin",
    "sex": true,
    "age": 20,
    "class_num": "9527",
    "description": "9527！！---就是我啦"
}
========
注意：
----截止到目前，创建了2条数据，删除了(第)1条，修改了1条；当前ser应用采用的是students应用中的模型数据，所以当前get请求只能获取的是id=2修改后的数据。
----如果是复制粘贴代码，预期结果就是上面response返回的结果；如果手写代码，需要确保：
1、所有字段名称在模型类定义的和在序列化器类定义的要保持一致，如果有；
2、追加应用ser到INSTALLED_APPS；追加ser.urls到总路由；为ser应用添加子路由；创建视图类引用序列化器类、模型对象、JsonResponse对象、get方法接收前端的参数等四部曲每一个环节都必须准确无误
3、序列化器类正确被定义
4、请求时输入正确的请求方法、主机名、路径和pk值；每次请求的地址、方法和是否带pk，甚至后缀是否带/都是需要需要的。
----即确保从发起请求到返回数据，整个数据流跑通，否则就会报错或者出不来预期结果。
----切记：复制代码易，手敲代码难！！！！

3.2 序列化示例2
3.2.1 创建视图类
在...DRF\drfdemo\ser应用下的views.py文件中：
=====
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
=====
3.2.2 更新子路由
...DRF\drfdemo\ser下更新urls.py文件，调用视图类的as_view()方法：
=====
from django.urls import path, re_path
from . import views


# 更新子路由，关联路径和视图
urlpatterns = [
    # ..2..
    # 方法：get方法获取多条数据，不带pk;
    # 模型：采用的是students下的Student模型对象;
    # 序列化器：序列化器类StudentSerializer继承至serializers.Serializer序列化器类;
    # 视图：继承的Django原生视图类View，StudentSerializer指定many=True
    path('students2/',views.Student2View.as_view()),
]
=====
3.2.3 已在一个接口中将子路追加到总路由，无需再追加
3.2.4 发送get请求
增(postman)：
由于数据库中只有id为2的1条数据，在此通过之前的接口先新增1条数据。
post=>http://localhost:8000/drf/students/
request.body=>
========
    {
        "name": "baby",
        "sex": true,
        "age": 22,
        "class_num": "1312",
        "description": "baby,baby!!"
    }
========
返回(postman)：
response.body=>
========
    {
        "id": 3,
        "name": "baby",
        "sex": true,
        "age": 22,
        "class_num": "1312",
        "description": "baby,baby!!"
    }
========
在对刚才创建的接口发送查询多条数据的请求
查：
get=>http://localhost:8000/ser/students2/
返回(postman)：
response.body=>
========
[
    {
        "id": 2,
        "name": "admin",
        "sex": true,
        "age": 20,
        "class_num": "9527",
        "description": "9527！！---就是我啦"
    },
    {
        "id": 3,
        "name": "baby",
        "sex": true,
        "age": 22,
        "class_num": "1312",
        "description": "baby,baby!!"
    }
]
========
注意：
student1和students2两个接口的关系
----student1查询单条数据，带pk值，获取序列化对象serializer不需对StudentSerializer设置参数many=True，返回的是一个json字典
----students2查询多条数据，不带pk字，获取序列化对象serializer需对StudentSerializer设置参数many=True，返回的是一个json列表
----带pk的student是单数，不带pk的students是复数，二者在路径上有意思的做了区分。

3.3 反序列化-数据校验示例3
　　使用序列化器进行反序列化时，需要对数据进行验证后，才能获取验证成功的数据或保存成模型类对象。

　　在获取反序列化的数据前，必须调用is_valid()方法进行验证，验证成功返回True，否则返回False。

验证失败，可以通过序列化器对象的errors属性获取错误信息，返回字典，包含了字段和字段的错误。is_valid()方法还可以在验证失败时抛出异常serializers.ValidationError，可以通过传递raise_exception=True参数开启。
验证成功，可以通过序列化器对象的validated_data属性获取数据。
　　在定义序列化器时，指明每个字段的序列化类型和选项参数，本身就是一种验证行为。
3.3.1 创建序列化器类
在...DRF\drfdemo\ser\应用目录中的serializers.py中创建一个Student3Serializer用于序列化与反序列化。
=====
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
=====
3.3.2 创建视图类
在...DRF\drfdemo\ser应用下的views.py文件中：
======
import json
from .serializers import Student3Serializer
class Student3View(View):
    def post(self,request):
        data= request.body.decode()
        # 反序列化用户提交的数据
        data_dic=json.loads(data)

        # 调用序列化器进行实例化,post方法接受一个数据，因此不需要many=True
        serializer=Student3Serializer(data=data_dic)
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
======
3.3.3 更新子路由
...DRF\drfdemo\ser下更新urls.py文件，调用视图类的as_view()方法：
=====
from django.urls import path, re_path
from . import views


# 更新子路由，关联路径和视图
urlpatterns = [
    # ..3..对提交的数据进行校验
    # 方法：post方法提交1条数据，不带pk;
    # 模型：未采用模型对象;
    # 序列化器：序列化器类Student3Serializer继承至serializers.Serializer序列化器类;
    # 视图：Student3View继承的Django原生视图类View，Student3Serializer无需指定many=True
    path('student3/',views.Student3View.as_view()),
]
=====
3.3.4 已在一个接口中将子路追加到总路由，无需再追加
3.3.5 发送post请求
增(postman)：
由于没有用students中的模型，向后端提交数据是并不会保存到数据库，相当于是验证完成后直接返回给前端。
post=>http://localhost:8000/ser/student3/
request.body=>
========
{
    "name": "admin",
    "age": 25,
    "sex": true,
    "workingtime": 2,
    "hobby": "你好，老弟！！",
    "title": 0
}
========
返回(postman)：
response.body=>
========
{
    "name": "admin",
    "sex": true,
    "age": 25,
    "workingtime": 2,
    "hobby": "你好，老弟！！",
    "title": 0
}
========

其它验证数据的post请求略……

3.4 反序列化-保存数据示例4

3.4.1 创建序列化器类
----前面的验证数据成功后,我们可以使用序列化器来完成数据反序列化的过程.这个过程可以把数据转成模型类对象.可以通过在序列化器中实现create()和update()两个方法来实现。
----在...DRF\drfdemo\ser\应用目录中的serializers.py中创建一个Student4Serializer用于序列化与反序列化。
=====
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
        #instance=Student.objects.create(**validated_data)
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
=====
3.4.2 创建视图类
在...DRF\drfdemo\ser应用下的views.py文件中：
======
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
=====

3.4.3 更新子路由
...DRF\drfdemo\ser下更新urls.py文件，调用视图类的as_view()方法：
=====
from django.urls import path, re_path
from . import views


# 更新子路由，关联路径和视图
urlpatterns = [
    # ..4..对提交的数据进行校验，并提交到数据库
    # 方法：post方法提交1条数据，不带pk;
    # 模型：采用Student模型对象;
    # 序列化器：序列化器类Student4Serializer继承至serializers.Serializer序列化器类;
    # 视图：Student3View继承的Django原生视图类View，Student3Serializer无需指定many=True
    path('student4/',views.Student4View.as_view()),
]
=====
3.4.4 已在一个接口中将子路追加到总路由，无需再追加
3.4.5 发送post请求
增(postman)：
使用students中的模型，向后端提交数据并保存到数据库。
post=>http://localhost:8000/ser/student4/
request.body=>
========
{
    "name": "MeiMei",
    "age": 25,
    "sex": true,
    "workingtime": 2,
    "hobby": "你好，老弟！！",
    "title": 0
}
========
返回(postman)：
response.body=>
========
{
    "name": "MeiMei",
    "sex": true,
    "age": 25,
    "workingtime": 2,
    "hobby": "你好，老弟！！",
    "title": 0
}
========
注意：
需要搞清楚A：post提交的字段、B:模型对象Student中的字段、C:序列化器返回的已验证数据字段之间的关系：
A中提交的data字段作为反序列化阶段的字段来源，可以是B中的字段，也可以不是；可以是C中的字段，也可以不是。
B中的字段是可能保存数据到数据库的最大字段范围，具体保存哪些字段到数据取决于A提交的字段和B中字段的交集
C中的字段是序列化器类中定义的字段，定义了哪些,serializer.validated_data就返回哪些；如果C中定义了，A没传，要报错；如果A传了，C中没定义，C也不会返回。

3.5 反序列化-保存数据示例5

3.5.1 序列化器类
沿用Student4Serializer

3.5.2 创建视图类
在...DRF\drfdemo\ser应用下的views.py文件中：
=====
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
=====

3.5.3 更新子路由
...DRF\drfdemo\ser下更新urls.py文件，调用视图类的as_view()方法：
=====
from django.urls import path, re_path
from . import views


# 更新子路由，关联路径和视图
urlpatterns = [
    # ..5..修改1条数据并进行校验，再提交到数据库
    # 方法：put方法提交1条数据，带pk;
    # 模型：采用Student模型对象;
    # 序列化器：序列化器类Student4Serializer继承至serializers.Serializer序列化器类;
    # 视图：Student5View继承的Django原生视图类View，Student4Serializer无需指定many=True
    re_path(r"^student5/(?P<pk>\d+)/$",views.Student5View.as_view()),
]
=====
3.5.4 已在一个接口中将子路追加到总路由，无需再追加
3.5.5 发送put请求
改(postman)：
使用students中的模型，向后端提交数据并保存到数据库。
put=>http://localhost:8000/ser/student5/3/
request.body=>
========
{
    "name": "MeiGa",
    "sex": false,
    "age": 24,
    "workingtime": 1,
    "hobby": "木拉",
    "title": 1
}
========
返回(postman)：
response.body=>
========
{
    "name": "MeiGa",
    "sex": false,
    "age": 24,
    "workingtime": 1,
    "hobby": "木拉",
    "title": 1
}
========

3.6 序列化与反序列化合并使用示例6
3.6.1 创建序列化器类
----在...DRF\drfdemo\ser\应用目录中的serializers.py中创建一个Student6Serializer用于序列化与反序列化。
=====
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
=====
3.6.2 创建视图类
在...DRF\drfdemo\ser应用下的views.py文件中：
=====
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
=====
3.6.3 更新子路由
...DRF\drfdemo\ser下更新urls.py文件，调用视图类的as_view()方法：
=====
from django.urls import path, re_path
from . import views


# 更新子路由，关联路径和视图
urlpatterns = [
    # ..6..对提交的数据进行校验，并提交到数据库+查询所有数据，两个接口合并
    # 方法：post方法提交1条数据，不带pk;get方法查看所有数据
    # 模型：采用Student模型对象;
    # 序列化器：序列化器类Student6Serializer继承至serializers.Serializer序列化器类;
    # 视图：Student6View继承的Django原生视图类View，Student6Serializer无需指定many=True
    path('student6/',views.Student6View.as_view()),
]
=====
3.6.4 已在一个接口中将子路追加到总路由，无需再追加
3.6.5 发送get和post请求
查(postman)：
get=>http://localhost:8000/ser/student6/
……略
增(postman)
post=>http://localhost:8000/ser/student6/
request.body=>
========
   {
        "name": "我是丹丹",
        "age":35,
        "sex": true,
        "class_num": "265",
        "description": "小表弟"
    }
========
返回(postman)：
response.body=>
========
{
    "name": "我是丹丹",
    "sex": true,
    "age": 35
}
========
注意：
截止目前，以上所有的序列化器类继承的都是serializer.Serializer类；
序列化器类中定义的字段和模型类中定义的字段是相对独立的
还是需要自己去实现post、get等方法，一旦用到save方法，需要重写create或者update方法。

3.7 模型类序列化器示例7
3.7.1 创建序列化器类
----在...DRF\drfdemo\ser\应用目录中的serializers.py中创建一个StudentModelSerializer用于序列化与反序列化。
=====
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
=====
3.7.2 创建视图类
在...DRF\drfdemo\ser应用下的views.py文件中：
=====
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
=====
3.7.3 更新子路由
...DRF\drfdemo\ser下更新urls.py文件，调用视图类的as_view()方法：
=====
from django.urls import path, re_path
from . import views


# 更新子路由，关联路径和视图
urlpatterns = [
    # ..6..对提交的数据进行校验，并提交到数据库+查询所有数据，两个接口合并
    # 方法：post方法提交1条数据，不带pk;get方法查看所有数据
    # 模型：采用Student模型对象;
    # 序列化器：序列化器类Student6Serializer继承至serializers.Serializer序列化器类;
    # 视图：Student6View继承的Django原生视图类View，Student6Serializer无需指定many=True
    path('student6/',views.Student6View.as_view()),
]
=====
3.7.4 已在一个接口中将子路追加到总路由，无需再追加
3.7.5 发送get和post请求
查(postman)：
get=>http://localhost:8000/ser/student7/
……略
增(postman)
post=>http://localhost:8000/ser/student7/
request.body=>
========
   {
        "name": "我是嘻嘻22",
        "age":35,
        "sex": true,
        "class_num": "265",
        "description": "小表弟"
    }
========
返回(postman)：
response.body=>
========
{
    "name": "我是嘻嘻22",
    "sex": true,
    "age": 35
}
========

4. Django-DRF(视图相关)
drf除了在数据序列化部分简写代码以外，还在视图中提供了简写操作。所以在django原有的django.views.View类基础上，drf封装了多个子类出来提供给我们使用。

Django REST framwork 提供的视图的主要作用：

控制序列化器的执行（检验、保存、转换数据）
控制数据库查询的执行
调用请求类和响应类（这两个类也是由drf帮我们再次扩展了一些功能类）。

4.1 请求与响应
4.1.1 Request
REST framework 传入视图的request对象不再是Django默认的HttpRequest对象，而是REST framework提供的扩展了HttpRequest类的Request类的对象。

　　REST framework 提供了Parser解析器，在接收到请求后会自动根据Content-Type指明的请求数据类型（如JSON、表单等）将请求数据进行parse解析，解析为类字典[QueryDict]对象保存到Request对象中。

　　Request对象的数据是自动根据前端发送数据的格式进行解析之后的结果。

　　无论前端发送的哪种格式的数据，我们都可以以统一的方式读取数据。

　　常用属性：

　　1. data

　　request.data 返回解析之后的请求体数据。类似于Django中标准的 request.POST 和 request.FILES 属性，但提供如下特性：

包含了解析之后的文件和非文件数据
包含了对POST、PUT、PATCH请求方式解析后的数据
利用了REST framework的parsers解析器，不仅支持表单类型数据，也支持JSON数据
　　2. query_params

　　request.query_params与Django标准的 request.GET 相同，只是更换了更正确的名称而已。

4.1.2 Response
=====
from rest_framework.response import Response
=====
REST framework提供了一个响应类Response，使用该类构造响应对象时，响应的具体数据内容会被转换（render渲染）成符合前端需求的类型。

　　REST framework提供了 Renderer 渲染器，用来根据请求头中的Accept（接收数据类型声明）来自动转换响应数据到对应格式。如果前端请求中未进行Accept声明，则会采用默认方式处理响应数据，我们可以通过配置来修改默认响应格式。

　　可以在rest_framework.settings查找所有的drf默认配置项
=====
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (  # 默认响应渲染类
        'rest_framework.renderers.JSONRenderer',  # json渲染器
        'rest_framework.renderers.BrowsableAPIRenderer',  # 浏览API渲染器
    )
}
=====
构造方式：
=====
Response(data, status=None, template_name=None, headers=None, content_type=None)
=====
data数据不要是render处理之后的数据，只需传递python的内建类型数据即可，REST framework会使用 renderer 渲染器处理data。

　　data不能是复杂结构的数据，如Django的模型类对象，对于这样的数据我们可以使用 Serializer 序列化器序列化处理后（转为了Python字典类型）再传递给data参数。

　　参数说明：

data: 为响应准备的序列化处理后的数据；
status: 状态码，默认200；
template_name: 模板名称，如果使用HTMLRenderer 时需指明；
headers: 用于存放响应头信息的字典；
content_type: 响应数据的Content-Type，通常此参数无需传递，REST framework会根据前端所需类型数据来设置该参数。
　　常用属性（用的不多）：

　　1. data：传给response对象的序列化后，但尚未render处理的数据

　　2. status_code：状态码的数字

　　3. content：经过render处理后的响应数

4.1.3 状态码
为了方便设置状态码， REST Framework在rest_framework.status模块中提供了常用状态码常量。

4.1.3.1 信息告知---1XX
HTTP_100_CONTINUE
HTTP_101_SWITCHING_PROTOCOLS

4.1.3.2 成功---2XX
HTTP_200_OK
HTTP_201_CREATED
HTTP_202_ACCEPTED
HTTP_203_NON_AUTHORITATIVE_INFORMATION
HTTP_204_NO_CONTENT
HTTP_205_RESET_CONTENT
HTTP_206_PARTIAL_CONTENT
HTTP_207_MULTI_STATUS

4.1.3.3 重定向---3XX
HTTP_300_MULTIPLE_CHOICES
HTTP_301_MOVED_PERMANENTLY
HTTP_302_FOUND
HTTP_303_SEE_OTHER
HTTP_304_NOT_MODIFIED
HTTP_305_USE_PROXY
HTTP_306_RESERVED
HTTP_307_TEMPORARY_REDIRECT

4.1.3.4 客户端错误---4XX
HTTP_400_BAD_REQUEST
HTTP_401_UNAUTHORIZED
HTTP_402_PAYMENT_REQUIRED
HTTP_403_FORBIDDEN
HTTP_404_NOT_FOUND
HTTP_405_METHOD_NOT_ALLOWED
HTTP_406_NOT_ACCEPTABLE
HTTP_407_PROXY_AUTHENTICATION_REQUIRED
HTTP_408_REQUEST_TIMEOUT
HTTP_409_CONFLICT
HTTP_410_GONE
HTTP_411_LENGTH_REQUIRED
HTTP_412_PRECONDITION_FAILED
HTTP_413_REQUEST_ENTITY_TOO_LARGE
HTTP_414_REQUEST_URI_TOO_LONG
HTTP_415_UNSUPPORTED_MEDIA_TYPE
HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
HTTP_417_EXPECTATION_FAILED
HTTP_422_UNPROCESSABLE_ENTITY
HTTP_423_LOCKED
HTTP_424_FAILED_DEPENDENCY
HTTP_428_PRECONDITION_REQUIRED
HTTP_429_TOO_MANY_REQUESTS
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS

4.1.3.5 服务器错误---5XX
HTTP_500_INTERNAL_SERVER_ERROR
HTTP_501_NOT_IMPLEMENTED
HTTP_502_BAD_GATEWAY
HTTP_503_SERVICE_UNAVAILABLE
HTTP_504_GATEWAY_TIMEOUT
HTTP_505_HTTP_VERSION_NOT_SUPPORTED
HTTP_507_INSUFFICIENT_STORAGE
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED

4.2视图
　　REST framework 提供了众多的通用视图基类与扩展类，以简化视图的编写。

　　Django REST framwork 提供的视图的主要作用：

控制序列化器的执行（检验、保存、转换数据）
控制数据库查询的执行
　　下面我们介绍一下两个视图基类

4.2.1 APIView
=====
from rest_framework.views import APIView
=====
APIView 是REST framework提供的所有视图的基类，继承自Django的View父类。

　　APIView 与View的不同之处在于：

①request对象：传入到视图方法中的是REST framework的request对象，而不是Django的HttpRequest对象；
②response对象：视图方法可以返回REST framework的Response对象，视图会为响应数据设置（render）符合前端要求的格式；
③异常处理：任何APIException异常都会被捕获到，并且处理成合适的响应信息；
④扩展功能：在进行dispatch()分发前，会对请求进行身份认证、权限检查、流量控制。
　　支持定义的类属性

authentication_classes 列表或元祖，身份认证类
permissoin_classes 列表或元祖，权限检查类
throttle_classes 列表或元祖，流量控制类
　　在APIView中仍以常规的类视图定义方法来实现get() 、post() 或者其他请求方式的方法。

4.2.2 GenericAPIView（通用视图类）
=====
from rest_framework.generics import GenericAPIView
=====
继承自APIView，主要增加了操作序列化器和数据库查询的方法，作用是为下面Mixin扩展类的执行提供方法支持。通常在使用时，可搭配一个或多个Mixin扩展类。

　　提供的关于序列化器使用的属性与方法

属性：

serializer_class 指明视图使用的序列化器
方法：

get_serializer_class(self)

当出现一个视图类中调用多个序列化器时,那么可以通过条件判断在get_serializer_class方法中通过返回不同的序列化器类名就可以让视图方法执行不同的序列化器对象了。

返回序列化器类，默认返回serializer_class，可以重写，例如：
=====
def get_serializer_class(self):
    if self.request.user.is_staff:
        return FullAccountSerializer
    return BasicAccountSerializer
=====

get_serializer(self, *args, **kwargs)

　　　　　　返回序列化器对象，主要用来提供给Mixin扩展类使用，如果我们在视图中想要获取序列化器对象，也可以直接调用此方法。

　　提供的关于数据库查询的属性与方法

属性：

queryset 指明使用的数据查询集
方法：

get_queryset(self)

返回视图使用的查询集，主要用来提供给Mixin扩展类使用，是列表视图与详情视图获取数据的基础，默认返回queryset属性，可以重写，例如：
=====
def get_queryset(self):
    user = self.request.user
    return user.accounts.all()
=====
get_object(self)

　　　　　　返回详情视图所需的模型类数据对象，主要用来提供给Mixin扩展类使用。

　　　　　　在试图中可以调用该方法获取详情信息的模型类对象。

　　其他可以设置的属性

pagination_class 指明分页控制类

filter_backends 指明过滤控制后端

　　简单介绍了一下，下面我们就通过代码来感受一下。

4.2.3 View与APIView-----示例1
4.2.3.1 创建一个新的子应用req
=====
python manage.py startapp req
=====

...DRF\drfdemo>python manage.py startapp req
4.2.3.2 在settings.py的INSTALLED_APPS中添加'req'
=========
INSTALLED_APPS = [
    ...
    'rest_framework',
    'students',
    'ser',
    'req',
    ...
]
=========
4.2.3.3 模型类
继续使用students应用中的模型student，暂不新建模型
4.2.3.4 创建序列化器
在...DRF\drfdemo\req\应用目录中新建serializers.py用于保存该应用的序列化器。
在serializers.py中创建一个StudentModelSerializer用于序列化与反序列化。
=====
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
=====
4.2.3.5 创建视图类
在...DRF\drfdemo\req应用下的views.py文件中：
=====
""" 测试代码：区分Django的View和DRF的APIView """

from django.views import View
from django.http import JsonResponse

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
=====
4.2.3.6 创建子路由
...DRF\drfdemo\req下新建urls.py文件，调用视图类的as_view()方法：
=====
from django.urls import path, re_path
from req import views

# 创建子路由，关联路径和视图
urlpatterns =[
    # View和APIView的区别
    path('student1/',views.Student1View.as_view()),
    path('student2/',views.Student2APIView.as_view())
]

=====
4.2.3.7 将子路由追加到总路由
=====
urlpatterns = [
    path('admin/', admin.site.urls),
    path('drf/', include('students.urls')),
    path('ser/', include('ser.urls')), #追加ser应用的子路由urls.py到总路由
    path('req/', include('req.urls')), #追加req应用的子路由urls.py到总路由
]
=====
4.2.3.8 发送get请求
----View实现----
查(postman)：
get=>http://localhost:8000/req/student1/?username=admin&pwd=110
返回(postman)：
response.body=>
========
{
    "name": "alex",
    "age": 18
}
========

----APIView实现----
查(postman)：
get=>http://localhost:8000/req/student2/?username=admin&pwd=110
request.body=>
========
    {
        "name": "我是大白兔",
        "age": 26,
        "sex": true
    }
========
返回(postman)：
response.body=>
========
{
    "name": "alex",
    "age": 18
}
========

4.2.4 使用APIView完成增删改查---示例2
4.2.4.1 借用已创建的模型对象Student
4.2.4.2 借用已创建的序列化器类StudentModelSerializer
4.2.4.3 创建视图类
在...DRF\drfdemo\req应用下的views.py文件中：
=====
"""
使用APIView提供学生信息的5个API接口
GET    /req/student3/               # 获取全部数据
POST   /req/student3/               # 添加数据

GET    /req/student4/(?P<pk>\d+)    # 获取一条数据
PUT    /req/student4/(?P<pk>\d+)    # 更新一条数据
DELETE /req/student4/(?P<pk>\d+)    # 删除一条数据
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
=====
4.2.4.4 更新子路由
...DRF\drfdemo\req下更新urls.py文件，调用视图类的as_view()方法：
=====
from django.urls import path, re_path
from . import views


# 更新子路由，关联路径和视图
urlpatterns = [
    #使用APIView完成增删改查，student3和student4可以共用一个路径
    #get方法查询所有+post方法创建1条数据
    path('student3/',views.Student3APIView.as_view()),
    #get方法查询1条+put方法修改1条+delete方法删除1条数据
    re_path(r'^student4/(?P<pk>\d+)/$',views.Student4APIView.as_view()),
]
=====
4.2.4.5 已在一个接口中将子路追加到总路由，无需再追加
4.2.4.6 对student3发送get、post请求
查(postman)：
get=>http://localhost:8000/req/student3/
……略
增(postman)
post=>http://localhost:8000/req/student3/
request.body=>
========
   {
        "name": "我是老白兔",
        "age":35,
        "sex": true
    }
========
返回(postman)：
response.body=>
========
{
    "name": "我是老白兔",
    "age": 35,
    "sex": true
}
========
4.2.4.7 对student4发送get、put和delete请求
查(postman)：
get=>http://localhost:8000/req/student4/3/
返回(postman)：
response.body=>
========
{
    "id": 3,
    "name": "MeiGa",
    "age": 24,
    "sex": false
}
========
改(postman)
post=>http://localhost:8000/req/student4/3/
request.body=>
========
{
    "name": "MeiGaLI",
    "age": 55,
    "sex": true
}
========
返回(postman)：
response.body=>
========
{
    "name": "MeiGaLI",
    "age": 55,
    "sex": true
}
========
删(postman)
post=>http://localhost:8000/req/student4/id/
返回(postman)：
response.body=>
========
{}
========
注意：需要把id换成需要删除的id，默认成功删除后返回{}，也可以根据需要返回自定义的数据格式。

小结：View=>APIView
1 原生的View提供的request和相应需要做数据转换，DRF重写了request，并提供新的Response方法，可以确保不同类型的输入到了DRF的request中都转换成字典格式的data，Response也会更加请求中要求返回的数据格式来返回，如果没有指定，则按原来的数据格式返回。
2 APIView引入了序列化器，可以在序列化器中定义序列化和反序列化规则，确保前端到后端，后端到前端的中间环节具有标准化的、统一的解决方案。
3 APIView重写了as_view()方法，不再是简单的返回一个view函数，而是经过一系列处理再返回view函数。

4.2.5 GenericAPIView完成增删改查---示例3
略
(方法和过程同示例2，只是用GenericAPIView的方式实现了增删改查，serializer.py/总路由urls.py和settings.py都不需要改动，相应改动的代码见views.py/子路由urls.py。)

小结：APIView=>GenericAPIView
1 把不同的请求方法中用到的模型对象查询集和序列化器类抽离出来，作为GenericAPIView的属性，不同的模型对象和序列化器类只需要改共同的属性即可，不用再到具体每个请求方法中去改模型对象查询集合序列化器类。
2 不同的请求方法逻辑结构不同，同一种请求方法逻辑结构基本相同，可以针对不同的请求方法封装成相应的同一类方法，这是XModeMixin的使命。

4.2.6 五个视图扩展类---示例4
4.2.6.1 借用已创建的模型对象Student
4.2.6.2 借用已创建的序列化器类StudentModelSerializer
4.2.6.3 创建视图类
在...DRF\drfdemo\req应用下的views.py文件中：
=====
"""
使用GenericAPIView结合视图Mixin扩展类，快速实现数据接口的APIView
ListModelMixin      实现查询所有数据功能
CreateModelMixin    实现添加数据的功能
RetrieveModelMixin  实现查询一条数据功能
UpdateModelMixin    更新一条数据的功能
DestroyModelMixin   删除一条数据的功能

注意：只有单一的XModeMixin，没有组合的XYZModeMixin！！！
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
=====
4.2.6.4 更新子路由
...DRF\drfdemo\req下更新urls.py文件，调用视图类的as_view()方法：
=====
from django.urls import path, re_path
from . import views


# 更新子路由，关联路径和视图
urlpatterns = [
    #使用GenericAPIView+Mixins完成增删改查，student7和student8可以共用一个路径
    #get方法查询所有+post方法创建1条数据
    path('student7/',views.Student7GenericAPIView.as_view()),
    #get方法查询1条+put方法修改1条+delete方法删除1条数据
    re_path(r'^student8/(?P<pk>\d+)/$',views.Student8GenericAPIView.as_view()),
]
=====
4.2.6.5 已在一个接口中将子路追加到总路由，无需再追加
4.2.6.6 对student7发送get和post，对student8发送get、put和delete请求
略(本示例实现了中对两个接口发"增删改查查"5个接口，发起请求和响应与之前postman中的操作类似，以下如无必要，将不在单独展示发起请求和响应的内容，仅展示操作步骤以示提醒。)

小结：GenericAPIView=>GenericAPIView+N*XModeMixin
1 将GenericAPIView中具体相同逻辑的不同的请求方法封装成相应的XModeMixin，只要继承了GenericAPIView+N*XModeMixin，然后在调用请求方法时，返回相应的X()方法即可即可
2 建立多个GenericAPIView时，大量具有相同结构的代码重复，如：
XGenericAPIView下
def post(self,request):
    return self.create(request)
和YGenericAPIView下：
def post(self,request):
    return self.create(request)
完全相同，还需要进一步封装。这是XAPIView的任务。

4.2.7 内置的扩展子类----示例5
4.2.7.1 借用已创建的模型对象Student
4.2.7.2 借用已创建的序列化器类StudentModelSerializer
4.2.7.3 创建视图类
在...DRF\drfdemo\req应用下的views.py文件中：
=====
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
=====

4.2.7.4 更新子路由
...DRF\drfdemo\req下更新urls.py文件，调用视图类的as_view()方法：
=====
# 更新子路由，关联路径和视图
urlpatterns = [
    #使用XAPIView完成增删改查，student9和student10可以共用一个路径
    #ListAPIView：get方法查询所有+CreateAPIView：post方法创建1条数据
    path('student9/',views.Student9GenericAPIView.as_view()),
    #RetrieveAPIView：get方法查询1条+UpdateAPIView：put方法修改1条+DestroyAPIView：delete方法删除1条数据
    re_path(r'^student10/(?P<pk>\d+)/$',views.Student10GenericAPIView.as_view()),
]
=====
4.2.7.5 已在一个接口中将子路追加到总路由，无需再追加
4.2.7.6 对student9发送get和post，对student10发送get、put和delete请求

小结：GenericAPIView+N*XModeMixin=>XAPIView/XYZAPIView
1 通过多继承GenericAPIView和XModeMixin封装为XAPIView，可以实现直接用XAPIView灵活创建增删改查的1个或者多个接口；
2 较未封装之前，不用再在视图类中定义请求方法并返回XModeMixin中的X方法，即不用再写类似
def get(self,request):
    return self.retrieve(request)
的代码，因为继承XModeMixin就相当于已经有了该方法
3 封装之后存在的不足是，从请求方法到XModeMixin中X方法的关联在继承时就写死了，没办法自定义请求方法名，也是就说重写请求方法必须是get、post、put和delete这种固定名称的方法。这种限制，在ViewSet中得到了解决。

4.2.8 视图集----示例6
4.2.8.1 借用已创建的模型对象Student
4.2.8.2 借用已创建的序列化器类StudentModelSerializer
4.2.8.3 创建视图类
在...DRF\drfdemo\req应用下的views.py文件中：
=====
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
=====

4.2.8.4 更新子路由
...DRF\drfdemo\req下更新urls.py文件，调用视图类的as_view()方法：
=====
# 更新子路由，关联路径和视图
urlpatterns = [
  # 使用GenericViewSet完成增删改查，可以共用一个路径
    # GenericViewSet+ListModeMixin：get方法查询所有;
    # GenericViewSet+CreateModeMixin：post方法创建1条数据
    # GenericViewSet重写了as_view方法，通过{"get":"list","post":"create"}建立请求方法和XModeMixin中方法的映射关系
    # 可以在视图集定义时，重写get或者post对应的方法，只要与请求方法保持一致的对应关系
    path('student11/',views.Student11GenericViewSet.as_view({"get":"list","post":"create"})),
    # GenericViewSet+RetrieveModeMixin：get方法查询1条数据;
    # GenericViewSet+UpdateModeMixin：put方法更新1条数据
    # GenericViewSet+DestroyModeMixin：delete方法删除1条数据
    # GenericViewSet重写了as_view方法，通过{"get":"retrieve","put":"update","delete":"destroy"}建立请求方法和和XModeMixin中方法的映射关系
    # 可以在视图集定义时，重写get或者post对应的方法，只要与请求方法保持一致的对应关系
    re_path(r'^student11/(?P<pk>\d+)/$',views.Student11GenericViewSet.as_view({"get":"retrieve","put":"update","delete":"destroy"})),

    # 使用ModelViewSet完成增删改查，可以共用一个路径
    # ModelViewSet：get方法查询所有;post方法创建1条数据
    # ModelViewSet继承了GenericViewSet，重写了as_view方法，通过{"get":"list","post":"create"}建立请求方法和和XModeMixin中方法的映射关系
    # 可以在视图集定义时，重写get或者post对应的方法，只要与请求方法保持一致的对应关系
    path('student12/',views.Student12ModelViewSet.as_view({"get":"list","post":"create"})),
    # ModelViewSet：get方法查询1条数据;put方法更新1条数据；delete方法删除1条数据
    # ModelViewSet继承了GenericViewSet重写了as_view方法，通过{"get":"retrieve","put":"update","delete":"destroy"}建立请求方法和和XModeMixin中方法的映射关系
    # 可以在视图集定义时，重写get、put和delete对应的方法，只要与请求方法保持一致的对应关系
    re_path(r'^student12/(?P<pk>\d+)/$',views.Student12ModelViewSet.as_view({"get":"retrieve","put":"update","delete":"destroy"})),
]
=====
4.2.8.5 已在一个接口中将子路追加到总路由，无需再追加
4.2.8.6 对student11发送get、post、put和delete请求

小结：XAPIView/XYZAPIView=>GenericViewSe+N*XModeMixin=>ModelViewSet
1 可以根据需要GenericViewSet和N个XModeMixin的方式任意组合，通过映射请求，不在受制于GenericAPIView+Mixins中重写请求方法时必须要采用get、post、put和delete命名请求方式。
2 相应的路由，只要在子路由中as_view()方法中保持请求方法和XModeMixin中的X()方法的对应即可
3 ModelViewSet通过多继承一次性封装了GenericViewSet和5个XModeMixin，路由也需要在as_view()方法中定义请求方法和XModeMixin中的X()方法的对应关系
4 当前的不足是如果多个ModelViewSet生成路由时，除了路径是变量其它均是重复，需要需要进一步封装；注册router组件为采用ModelViewSet后自动注册提供了解决方案


