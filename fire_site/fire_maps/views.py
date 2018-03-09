from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse
from django.views import generic
#from django.views import View

from . import maps_maker
from map_maker import draw_map


class IndexView(generic.View):
    template_name = 'fire_maps/index.html'
    countries = ["", "Colombia", "Ecuador", "Bolivia"]

    def get(self, request):
        return render(request, self.template_name, {"countries": self.countries}) 

    def post(self, response):
        country = response.POST["country"]
        html_ = maps_maker.draw_map(country, "2018-02-26", "2018-03-03", "normal")
        return HttpResponse(country)

