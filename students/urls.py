from rest_framework.routers import DefaultRouter
from students import views

urlpatterns = []  # Django的路由表

router = DefaultRouter()  # 可以处理视图的路由器

router.register('students', views.StudentAPIView)  # url关联视图

urlpatterns += router.urls  # 将路由器中的所有路由信息追加到Django的路由表中


