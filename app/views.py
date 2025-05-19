from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

class Buffet:
    def __init__(self, name, max_people, image, people_data, food_data):
        self.name = name
        self.max_people = max_people
        self.image = image
        self.people_data = people_data
        self.food_data = food_data

    def get_people(self, people_count):
        percentage = [0.1, 0.35, 0.7]
        rarity = ["свободно", "мало", "средне", "заполнено"]
        for i in range(3):
            if (people_count < self.max_people * percentage[i]):
                return rarity[i]
        return rarity[3]
    
    def get_args(self):
        return {"name": self.name, "people": self.people, "image": self.image}
    
buffet_data = {
    "people": 0,
    "food": {}
}

buffet_counter = {
}

food_names = {
    'Bulka_with_koritsa': 'Булочк и с корицей', 
    'Bulka_meat': 'Пирожки с мясом', 
    'jaguar': 'Ягуар'
}

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("Получены данные:", data)
        # return render(request, 'myapp/show_data.html', context=data), JsonResponse({'status': 'ok', 'received': data})
        return JsonResponse({'status': 'ok', 'received': data})
    return JsonResponse({'error': 'Только POST'}, status=400)

@csrf_exempt
def index(request):
    Himlab = Buffet("Буфет Химлаб", 20, "static/img/himlab.jpg", buffet_data["people"], buffet_data["food"])
    ULK = Buffet("УЛК - 3 этаж", 25, "static/img/ulk.jpg", 0, 0)
    people = Himlab.people_data
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Получены данные:", data)
            if "people" in data:
                buffet_data["people"] = data["people"]

            for item, value in data.items():
                if data[item] != "people":
                    item = food_names[item]
                    buffet_counter[item] = buffet_counter.get(item, 0) + 1
                    if buffet_counter[item] == 3:
                        buffet_counter[item] = 0
                        buffet_data["food"].update({item: 0})
                    else:    
                        buffet_data["food"].update({item: value})
        except Exception as e:
            print("Ошибка при обработке POST:", str(e))
    Himlab.people_data = buffet_data["people"]
    Himlab.food_data = buffet_data["food"]
    buffets = [
    {"name": Himlab.name, "people": Himlab.get_people(Himlab.people_data), "food": Himlab.food_data, "image": Himlab.image},
    {"name": ULK.name, "people": ULK.get_people(10), "food": {}, "image": ULK.image},
    ]
    # if request.method == 'POST':
    #     data = json.loads(request.body)
    #     # print("Получены данные:", data)
    #     # buffets[0].update(data["people"])
    #     for food in data:
    #         buffets[0]["food"].update(food)
    context = {"buffets": buffets}
    return render(request, 'index.html', context)
