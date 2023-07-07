from django.shortcuts import render
from .models import *
import random
import datetime
import json
from django.http import HttpResponse, HttpResponseNotFound, QueryDict
# Create your views here.
def build_data(categories, sales, expenses):
    return {"labels":categories, "data":[{
          "label": 'Ventas',
          "backgroundColor": '#3366ff',
          "data": sales,
          "borderWidth":5,
          "barThickness":30
        }, {
          "label": 'Gastos',
          "backgroundColor": '#009999',
          "data": expenses,
          "borderWidth":5,
          "barThickness":30
        }]}
def index(request, date=None):
    if request.method == 'POST':
        print(request.POST['date-selected'])
        date = datetime.datetime.strptime(request.POST['date-selected'], "%Y-%m-%d")
        sales = income.get_daily_stats(date=date)
        print(sales)
        gastos = expenses.get_daily_stats(date=date)
        res = HttpResponse(request)
    else:
        date = datetime.datetime.now()
        sales = income.get_daily_stats(date=date)
        gastos = expenses.get_daily_stats(date=date)
        rendimiento = sum(sales) - sum(gastos)
        if request.META.get("HTTP_HX_REQUEST"):
            res = render(request, "webapp/partials/date.html", {"date_type":"date", "current_date" : datetime.datetime.now().strftime("%Y-%m-%d"),"rendimiento":rendimiento})
        else:
            res= render(request, "webapp/dashboard.html", {"date_type":"date", "current_date": datetime.datetime.now().strftime("%Y-%m-%d"), "rendimiento":rendimiento})
    categories = income.get_categories()
    dataset = build_data(categories=categories, sales=sales, expenses=gastos)
    res.headers["HX-Trigger"] = json.dumps({"changed":dataset})
    return res

def weekly(request, week=None):
    if request.method == 'POST':
        date = datetime.datetime.strptime(request.POST['date-selected']+ '-1', '%G-W%V-%u')
        sales = income.get_weekly_stats(date=date)
        gastos = expenses.get_weekly_stats(date=date)
        res = HttpResponse(request)
    else:
        date = datetime.datetime.now()
        sales = income.get_weekly_stats(date=date)
        gastos = expenses.get_weekly_stats(date=date)
        rendimiento = sum(sales) - sum(gastos)
        if request.META.get("HTTP_HX_REQUEST"):
            res = render(request, "webapp/partials/date.html", {"date_type":"week", "current_date" : datetime.datetime.now().strftime("%Y-W%W"), "rendimiento":rendimiento})
        else:
            res = render(request, "webapp/dashboard.html", {"date_type":"week", "current_date": datetime.datetime.now().strftime("%Y-W%W"), "rendimiento":rendimiento})

    categories = income.get_categories()
    dataset = build_data(categories=categories, sales=sales, expenses=gastos)
    res.headers["HX-Trigger"] = json.dumps({"changed":dataset})
    return res
def monthly(request, month=None):
    if request.method == 'POST':
        date = datetime.datetime.strptime(request.POST['date-selected'], '%Y-%m')
        sales = income.get_monthly_stats(date=date)
        gastos = expenses.get_monthly_stats(date=date)
        res = HttpResponse(request)
    else:
        date = datetime.datetime.now()
        sales = income.get_monthly_stats(date=date)
        gastos = expenses.get_monthly_stats(date=date)
        rendimiento = sum(sales) - sum(gastos)
        if request.META.get("HTTP_HX_REQUEST"):
            res = render(request, "webapp/partials/date.html", {"date_type":"month", "current_date" : datetime.datetime.now().strftime("%Y-%m"), "rendimiento":rendimiento})
        else:
            res = render(request, "webapp/dashboard.html", {"date_type":"month", "current_date" : datetime.datetime.now().strftime("%Y-%m") , "rendimiento":rendimiento})

    categories = income.get_categories()
    dataset = build_data(categories=categories, sales=sales, expenses=gastos)
    res.headers["HX-Trigger"] = json.dumps({"changed":dataset})
    return res
            

def anually(request, year=None):
    if request.method == 'POST':
        date = int(year)
        sales = income.get_anual_stats(date)
        gastos = expenses.get_anual_stats(date)
        res = HttpResponse(request)
    else:
        date = datetime.datetime.now().year
        sales = income.get_anual_stats(date)
        gastos = expenses.get_anual_stats(date)
        categories = income.get_categories()
        rendimiento = sum(sales) - sum(gastos)
        if request.META.get("HTTP_HX_REQUEST"):
            res = render(request, "webapp/partials/date.html", {"date_type":"number", "current_date" : datetime.datetime.now().year, "rendimiento": rendimiento})
        else:
            res = render(request, "webapp/dashboard.html", {"date_type":"number", "current_date" : datetime.datetime.now().year, "redimiento": rendimiento})

    dataset = build_data(categories=categories, sales=sales, expenses=gastos)
    res.headers["HX-Trigger"] = json.dumps({"changed":dataset})
    return res

    

def productos(request, cat=None):
    categorias = income.get_categories()
    if (cat and cat not in categorias):
        return HttpResponseNotFound("Categoria inexistente")
    products = Product.objects.filter(category=cat)
    if request.META.get("HTTP_HX_REQUEST"):
        res = render(request, "webapp/partials/productList.html", { "categorias": categorias, "actual": cat , "products":products })
    else:
        res = render(request, "webapp/products.html", { "categorias": categorias, "actual": cat , "products":products })
    return res
    
def editProduct(request, productID):
    # if request.META.get('HTTP_HX_REQUEST'):
    print(productID)
    prod = Product.objects.get(pk=productID)
    res = render(request, "webapp/partials/editProduct.html", { "prod": prod })
    return res

def getProduct(request, productID):
    if request.META.get('HTTP_HX_REQUEST'):
        method = request.method
        if method == 'PUT':
            data = QueryDict(request.body)
            data = {k:data[k] for k in data}
            prod = Product.objects.filter(pk=productID)
            prod.update(**data)
            prod = Product.objects.get(pk=productID)
            return render(request, "webapp/partials/productRow.html", { "prod": prod })
        if method == 'GET':
            prod = Product.objects.get(pk=productID)
            return render(request, "webapp/partials/productRow.html", { "prod": prod })
            


def test(request):
    # return Http
    print(request.POST['date-selected'])