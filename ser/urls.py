from django.urls import path, re_path
from . import views


# 创建子路由，关联路径和视图
urlpatterns = [
    # ..1..
    # 方法：get方法获取1条数据，带pk;
    # 模型：采用的是students下的Student模型对象;
    # 序列化器：序列化器类StudentSerializer继承至serializers.Serializer序列化器类;
    # 视图：Student1View继承的Django原生视图类View
    re_path(r'^student1/(?P<pk>\d+)/$', views.Student1View.as_view()),

    # ..2..
    # 方法：get方法获取多条数据，不带pk;
    # 模型：采用的是students下的Student模型对象;
    # 序列化器：序列化器类StudentSerializer继承至serializers.Serializer序列化器类;
    # 视图：Student2View继承的Django原生视图类View，StudentSerializer指定many=True   
    path('students2/',views.Student2View.as_view()),

    # ..3..对提交的数据进行校验
    # 方法：post方法提交1条数据，不带pk;
    # 模型：未采用模型对象;
    # 序列化器：序列化器类Student3Serializer继承至serializers.Serializer序列化器类;
    # 视图：Student3View继承的Django原生视图类View，Student3Serializer无需指定many=True
    path('student3/',views.Student3View.as_view()),

    # ..4..对提交的数据进行校验，并提交到数据库
    # 方法：post方法提交1条数据，不带pk;
    # 模型：采用Student模型对象;
    # 序列化器：序列化器类Student4Serializer继承至serializers.Serializer序列化器类;
    # 视图：Student4View继承的Django原生视图类View，Student4Serializer无需指定many=True
    path('student4/',views.Student4View.as_view()),

    # ..5..修改1条数据并进行校验，再提交到数据库
    # 方法：put方法提交1条数据，带pk;
    # 模型：采用Student模型对象;
    # 序列化器：序列化器类Student4Serializer继承至serializers.Serializer序列化器类;
    # 视图：Student5View继承的Django原生视图类View，Student4Serializer无需指定many=True
    re_path(r"^student5/(?P<pk>\d+)/$",views.Student5View.as_view()),

    # ..6..对提交的数据进行校验，并提交到数据库+查询所有数据，两个接口合并
    # 方法：post方法提交1条数据，不带pk;get方法查看所有数据
    # 模型：采用Student模型对象;
    # 序列化器：序列化器类Student6Serializer继承至serializers.Serializer序列化器类;
    # 视图：Student6View继承的Django原生视图类View，Student6Serializer，post无需指定many=True；get时需要字段
    path('student6/',views.Student6View.as_view()),

    # ..7..对提交的数据进行校验，并提交到数据库+查询所有数据，两个接口合并
    # 方法：post方法提交1条数据，不带pk;get方法查看所有数据
    # 模型：采用Student模型对象;
    # 序列化器：序列化器类StudentModelSerializer继承至serializers.ModelSerializer序列化器类;
    # 视图：Student7View继承的Django原生视图类View，StudentModelSerializer，post无需指定many=True；get时需要
    path('student7/',views.Student7View.as_view()),
]
