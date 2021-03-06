from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
import datetime
from blog.articles.models import ARTICLES

# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html', {
        'op': datetime.date.today().isoformat(),
    }, content_type='html')

def calculate(request: HttpRequest) -> HttpResponse:

    if 'op' in request.GET:
        request.session['op'] = request.GET['op']
    if 'left' in request.GET:
        request.session['left'] = request.GET['left']
    if 'right' in request.GET:
        request.session['right'] = request.GET['right']
    op = request.session.get('op', 'Uncnown')
    left = request.session.get('left', 'Uncnown')
    right = request.session.get('right', 'Uncnown')

    operation_dict = {'+': lambda x,y: x+y, '-': lambda x,y: x-y, '*': lambda x,y: x*y, '/': lambda x,y: x/y}

    if op in operation_dict.keys():
        if op is '/':
            try:
                a = int(right)
                b = int(left)
            except BaseException:
                return HttpResponse('Неверный тип операнда: x = {}, y = {}'.format(right, left), status=400)
            if a == 0:
                return HttpResponse('Деление на ноль', status=400)
        answer = operation_dict[op](int(left), int(right))
    else:
        return HttpResponse('Нет такой операции: {}'.format(op), status=400)
    return HttpResponse('{}'.format(answer))

def archiv (request: HttpRequest):
    rtrn = []
    for i in ARTICLES:
        rtrn.append(i['title'])
    return HttpResponse('\n'.join(rtrn))

def articles_num (request: HttpRequest, id):
    for i in ARTICLES:
        if i['id'] == id:
            return HttpResponse(i['title'])
    return HttpResponse('Нет такой страницы: {}'.format(id), status=404)

def articles_year (request: HttpRequest, year):
    rtrn = []
    for i in ARTICLES:
        if i['year'] == year:
            rtrn.append(i['title'])
    return HttpResponse('\n'.join(rtrn))
