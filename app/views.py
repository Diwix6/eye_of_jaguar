from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse


def index(request):
    buffets = [
    {"name": "Буфет Химлаб", "people": 20, "food": 15, "image": "static/img/himlab.jpg"},
    {"name": "Буфет 2", "people": 60, "food": 10},
    {"name": "Буфет 3", "people": 25, "food": 5},
    ]
    context = {"buffets": buffets}
    return render(request, 'index.html', context)
