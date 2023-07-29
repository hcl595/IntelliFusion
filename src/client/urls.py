from django.urls import path

from . import views

urlpatterns = [
    path('', views.root, name='root'),
    path('openai/', views.request_openai_response, name="openai"), #请求Openai
    path('llm/', views.request_api_response, name="api"), #请求API接口
    path('EditSetting/', views.EditSetting, name="EditSettings"), #编辑设置
    path('ManageModel/', views.ManageModel, name='ManageModel'), #编辑模型
    # path('login/', views.login_check, name='Login'), #登录
    # path('register/', views.register, name='register'), #注册
    path('logout/', views.logout, name="Logout"),#登出
    path('CorePercent/', views.WidgetsCorePercent, name="CorePercent"),#CPU占用状态
    path('RamPercent/', views.WigetsRamPercent, name="RamPercent"),#内存占用状态
    path('static/js/echarts.min.js/', views.js, name="echarts"),#数据可视化JavaScripts
    path('test/', views.test, name="Test"),
]