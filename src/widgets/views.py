from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import psutil

# Create your views here.

def CorePercent(InputRequest):
    return render(InputRequest,"CPU_Percent.html")

def RAMPercent(InputRequest):
    return render(InputRequest,"Memory_Percent.html") 

def Get_CPU_Precent(InputRequest):
    cpu_percent = psutil.cpu_percent()
    return JsonResponse({'data':cpu_percent})

def Get_RAM_Precent(InputRequest):
    memory_percent = psutil.virtual_memory().percent
    return JsonResponse({'data':memory_percent})