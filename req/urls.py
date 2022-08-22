from django.urls import path, re_path
from req import views
urlpatterns =[
    # View和APIView的区别
    #get方法查询所有
    path('student1/',views.Student1View.as_view()),
    #get方法查询所有
    path('student2/',views.Student2APIView.as_view()),

    #使用APIView完成增删改查，student3和student4可以共用一个路径
    #get方法查询所有+post方法创建1条数据
    path('student3/',views.Student3APIView.as_view()),
    #get方法查询1条+put方法修改1条+delete方法删除1条数据
    re_path(r'^student4/(?P<pk>\d+)/$',views.Student4APIView.as_view()),

    #使用GenericAPIView完成增删改查，student5和student6可以共用一个路径
    #get方法查询所有+post方法创建1条数据
    path('student5/',views.Student5GenericAPIView.as_view()),
    #get方法查询1条+put方法修改1条+delete方法删除1条数据
    re_path(r'^student6/(?P<pk>\d+)/$',views.Student6GenericAPIView.as_view()),

    #使用GenericAPIView+Mixins完成增删改查，student7和student8可以共用一个路径
    #get方法查询所有+post方法创建1条数据
    path('student7/',views.Student7GenericAPIView.as_view()),
    #get方法查询1条+put方法修改1条+delete方法删除1条数据
    re_path(r'^student8/(?P<pk>\d+)/$',views.Student8GenericAPIView.as_view()),

    #使用XAPIView完成增删改查，student9和student10可以共用一个路径
    #ListAPIView：get方法查询所有+CreateAPIView：post方法创建1条数据
    path('student9/',views.Student9GenericAPIView.as_view()),
    #RetrieveAPIView：get方法查询1条+UpdateAPIView：put方法修改1条+DestroyAPIView：delete方法删除1条数据
    re_path(r'^student10/(?P<pk>\d+)/$',views.Student10GenericAPIView.as_view()),

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