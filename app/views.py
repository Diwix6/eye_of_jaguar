from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse

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
    

def index(request):
    Himlab = Buffet("Буфет Химлаб", 20, "static/img/himlab.jpg")
    ULK = Buffet("УЛК - 3 этаж", 25, "static/img/ulk.jpg")
    buffets = [
    {"name": Himlab.name, "people": Himlab.get_people(5), "food": {}, "image": Himlab.image},
    {"name": ULK.name, "people": ULK.get_people(10), "food": {}, "image": ULK.image},
    {"name": "Буфет 3", "people": 25, "food": {}},
    ]
    context = {"buffets": buffets}
    return render(request, 'index.html', context)
