from groupsort.models import Namelist, Person, Pairing
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect



def home_view(request):
    template_name = "groupsort/home.html"
    dict = {}
    context = RequestContext(request)
    
    return render_to_response(
        template_name,
        dict,
        context)
        
def namelist_view(request):
    template_name = "groupsort/namelist_view.html"
    dict = {}
    context = RequestContext(request)