from django.shortcuts import render
import os

# Create your views here.

def map(request):
    module_dir = os.path.dirname(__file__)  
    file_path = os.path.join(module_dir, 'test/static/LiveTracking/BusesPos.txt')   #full path to text.
    data_file = open(file_path , 'r')       
    busList = []
    for line in data_file:
      #strLine = line.split
      busList.append(line.strip().split(","))
    print(busList)
    context = {'buses': busList}
    return render(request, 'map.html', context)


