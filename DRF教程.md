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


# 创建序列化器类，以便在views.py中被调用
class StudentModelSerializer(serializers.ModelSerializer):
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


