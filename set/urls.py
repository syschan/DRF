from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from set import views
urlpatterns = [
    # ViewSet
    path('student1/', views.Student1ViewSet.as_view({'get': 'get_5'})),
    path('student1/get_5_boy/',
         views.Student1ViewSet.as_view({'get': 'get_5_boy'})),
    re_path(r'^student1/(?P<pk>\d+)/$',
            views.Student1ViewSet.as_view({'get': 'get_one'})),

    # ViewSet+GenericAPIView
    path('student2/', views.Student2ViewSet.as_view({'get': 'get_5'})),
    path('student2/get_5_boy/',
         views.Student2ViewSet.as_view({'get': 'get_5_boy'})),
    re_path(r'^student2/(?P<pk>\d+)/$',
            views.Student2ViewSet.as_view({'get': 'get_one'})),

    # GenericViewSet
    path('student3/', views.Student3GenericViewSet.as_view({'get': 'get_5'})),
    path('student3/get_5_boy/',
         views.Student3GenericViewSet.as_view({'get': 'get_5_boy'})),

    # GenericViewSet+N*XModeMixin,快速生成API组合
    path('student4/',
         views.Student4GenericViewSet.as_view({'get': 'list', 'post': 'create'})),

    # ModelViewSet,一次性快速生成5个API，也可以根据需要减少不需要的API
    path('student5/',
         views.Student5ModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^student5/(?P<pk>\d+)/$', views.Student5ModelViewSet.as_view(
        {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

    # 也可以根据需要去掉不用的API
    # path('student5/',views.Student5ModelViewSet.as_view({'get':'list'})),
    # re_path(r'^student5/(?P<pk>\d+)/$',views.Student5ModelViewSet.as_view({'delete':'destroy'})),

    # ReadOnlyModelViewSet,一次性生成2个只读API
    path('student6/',
         views.Student6ReadOnlyModelViewSet.as_view({'get': 'list'})),
    re_path(r'^student6/(?P<pk>\d+)/$',
            views.Student6ReadOnlyModelViewSet.as_view({'get': 'retrieve'})),

    # 在视图类中调用多个序列化器
    path('student8/', views.Student8GenericAPIView.as_view()),

    # 在视图集中调用多个序列化器
    path('student9/',
         views.Student9ModelViewSet.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^student9/(?P<pk>\d+)/$',
            views.Student9ModelViewSet.as_view({'get': 'retrieve', 'put': 'update'}))

]

""" 
有了视图集以后，视图文件中多个视图类可以合并成一个，但是路由的代码就变得复杂了；
需要我们经常在as_view()方法中编写http请求和视图方法的对应关系 
事实上，在路由中DRF提供了一个路由类给我们对路由代码进行简写。
当然这个路由类【仅针对视图集可用】
视图集，包括ViewSet、GenericViewSet、ModelViewSet、ReadOnlyModelViewSet。
"""

# 路由类默认只会给视图集中的基本5个API生成地址，即增删改查查

# 实例化路由类
router = DefaultRouter()

# 注册视图集类到路由，router.register('访问地址前缀','视图集','访问别名')
router.register('student7', views.Student7ModelViewSet)

# 追加生成的路由到子路由中
urlpatterns += router.urls
