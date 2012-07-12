from groupsort.models import NameList, Person, Pairing
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect



def home_view(request, namelist_id=None):
    template_name = "groupsort/home.html"
    dict = {}
    context = RequestContext(request)
    dict['groups'] = NameList.objects.all()
    if namelist_id:
        namelist = NameList.objects.get(id=namelist_id)
        people = Person.objects.filter(namelist=namelist)
        dict['people'] = people
    
    return render_to_response(
        template_name,
        dict,
        context)
        
def namelist_view(request):
    template_name = "groupsort/namelist_view.html"
    dict = {}
    context = RequestContext(request)