"""
Definition of views.
"""
import json
import requests
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import View
from django.template.response import TemplateResponse
from django.template import loader
from .models import Shops
from .forms import Searching_shops



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def error(request):
    """Renders the about page."""
    
    return render(
        request,
        'app/error.html',
        {
            'title':'Ошибка',
            'message':'Произошла непредвиденная ошибка',
            'year':datetime.now().year,
        }
    )

def search_shops(request):
    form = Searching_shops()
    if request.method == "POST":
        form = Searching_shops(request.POST)
        if form.is_valid:
            search_api_server = "https://search-maps.yandex.ru/v1/"
            api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
            print(form)
            search_params = {
                "apikey": api_key,
                "text": f"Радиодетали, Воронеж",
                "lang": "ru_RU",
                "type": "biz"
            }

            response = requests.get(search_api_server, params=search_params)
            # Преобразуем ответ в json-объект
            store_dic = {}
            json_response = response.json()
            organization = json_response["features"]
            for i in range(len(organization)):
                store_dic[i] = store_dic.get(i, organization[i])
            for i, t in store_dic.items():
                print(i, t)
            return render(
                request,
                'app/list_shops.html',
                {
                    'title':'Поиск магазина',
                    'year':datetime.now().year,
                    'shops':store_dic,
                    'form':form,
                }
            )        
    return render(
        request,
        'app/search_shops.html',
        {
            'title':'Поиск магазина',
            'year':datetime.now().year,
            'form':form,
        }
    )        






class TemplateResponseMixin:
    """A mixin that can be used to render a template."""
    template_name = None
    template_engine = None
    response_class = TemplateResponse
    content_type = None

    def get_template_names(self):
       
        if self.template_name is None:
            raise ImproperlyConfigured(
                "TemplateResponseMixin requires either a definition of "
                "'template_name' or an implementation of 'get_template_names()'")
        else:
            return [self.template_name]

    def render_to_response(self, context, **response_kwargs):
        """
        Return a response, using the `response_class` for this view, with a
        template rendered with the given context.

        Pass response_kwargs to the constructor of the response class.
        """
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(
            request=self.request,
            template=self.get_template_names(),
            context=context,
            using=self.template_engine,
            **response_kwargs
        )

class JsonResponseMixin(object):
    def render_to_reponse(self, context):
        return HttpResponse(self.convert_context_to_json(context),
                                 content_type='application/json')

    def convert_context_to_json(self, context, extract_from_queryset=None):
        pass

class MixedView(View, JsonResponseMixin, TemplateResponseMixin):
    def get_context(self, request):
        pass
    
    def get(self, request, *args, **kwargs):
        context = self.get_context(request)
        if request.GET.get('format', 'html') == 'json' or self.template_name is None:
            return JsonResponseMixin.render_to_reponse(self, context)
        else:
            return TemplateResponseMixin.render_to_response(self, context)

class ShopsView(MixedView):
    def get_context(self, request):
        context = None
        return context

    template_name = 'app/search_shops.html'

    def convert_context_to_json(self, context):
        json_context = dict()
        return json.dumps(json_context, encoding='utf-8', ensure_ascii=False)
