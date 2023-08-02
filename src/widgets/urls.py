from django.urls import path

from . import views

urlpatterns = [
    path('widgets/CPU_Percent', views.CorePercent, name='ManageModel'), #编辑模型
    path('widgets/RAM_Percent', views.RAMPercent, name='ManageModel'), #编辑模型
    path('widgets/Get_CPU_DATA', views.Get_CPU_Precent, name='ManageModel'), #编辑模型
    path('widgets/Get_RAM_DATA', views.Get_RAM_Precent, name='ManageModel'), #编辑模型
]