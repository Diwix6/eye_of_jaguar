from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

class Buffet:
    def __init__(self, name, max_people, image):
        self.name = name
        self.max_people = max_people
        self.image = image

    def get_people(self, people_count):
        percentage = [0.1, 0.35, 0.7]
        rarity = ["свободно", "мало", "средне", "заполнено"]
        for i in range(3):
            if (people_count < self.max_people * percentage[i]):
                return rarity[i]
        return rarity[3]
    
    def get_args(self):
        return {"name": self.name, "people": self.people, "image": self.image}
    
@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("Получены данные:", data)
        return render(request, 'myapp/show_data.html', context=data), JsonResponse({'status': 'ok', 'received': data})
        # return JsonResponse({'status': 'ok', 'received': data})
    return JsonResponse({'error': 'Только POST'}, status=400)

def index(request):
    
        # return render(request, 'myapp/show_data.html', context=data), JsonResponse({'status': 'ok', 'received': data})
        # return JsonResponse({'status'w: 'ok', 'received': data})
    # return JsonResponse({'error': 'Только POST'}, status=400)

    Himlab = Buffet("Буфет Химлаб", 20, "static/img/himlab.jpg")
    ULK = Buffet("УЛК - 3 этаж", 25, "static/img/ulk.jpg")
    
    buffets = [
    {"name": Himlab.name, "people": Himlab.get_people(5), "food": {}, "image": Himlab.image},
    {"name": ULK.name, "people": ULK.get_people(10), "food": {}, "image": ULK.image},
    ]
    if request.method == 'POST':
        data = json.loads(request.body)
        print("Получены данные:", data)
        buffets[0].update(data["people"])
        for food in data:
            buffets[0]["food"].update(food)
    context = {"buffets": buffets}
    return render(request, 'index.html', context)
