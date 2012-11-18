from groupsort.models import NameList, Person, Pairing
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json

def home_view(request, namelist_id=None, person_id=None):
    template_name = "groupsort/home.html"
    dict = {}
    context = RequestContext(request)
    dict['groups'] = NameList.objects.all()
    if namelist_id:
        namelist = NameList.objects.get(id=namelist_id)
        people = Person.objects.filter(namelist=namelist)
        dict['this_namelist'] = namelist
        dict['people'] = people
        
    if person_id:
        person = Person.objects.get(id=person_id)
        print person
        dict['person'] = person
        dict['list_pairings'] = person.pairings.all().order_by('count')
        print dict['list_pairings']
    
    return render_to_response(
        template_name,
        dict,
        context)
        
def save_person(request):
    get = request.POST.copy()
    name = get['new_name']
    namelist_id = get['namelist_id']
    namelist = NameList.objects.get(id=namelist_id)
    this_person = Person.objects.create(name=name, namelist=namelist)
    d = { 'name':this_person.name, 'name_id':this_person.id }
    for person in namelist.people.all():
        if person != this_person:
            pairing = Pairing.objects.filter(people__id=person.id)
            if pairing.count() == 0:
                pairing = Pairing.objects.create(namelist=namelist)
                pairing.people.add(this_person)
                pairing.people.add(person)
                pairing.save()
    if request.is_ajax():
        return HttpResponse(json.dumps(d))
    else:
        return HttpResponseRedirect('/groupsort/namelist/' + namelist_id)

def groups_view(request, namelist_id, num_groups):
    template_name = "groupsort/groups_view.html"
    dict = {}
    context = RequestContext(request)
    
    pairings = []
    namelist = NameList.objects.get(id=namelist_id)
    groups = groupsort(namelist, int(num_groups))
    for group in groups:
        for person_1 in group:
            group_pairings = Pairing.objects.filter(people=person_1)
            for person_2 in group:
                if person_1 != person_2:
                    pairings.append(group_pairings.get(people=person_2))
    
    for pairing in pairings:
        pairing.count = pairing.count + 1
        pairing.save()
        
    dict['groups'] = groups
    dict['this_namelist'] = namelist
    
    return render_to_response(
        template_name,
        dict,
        context)
    
def groupsort(namelist, num_groups):
    groups = []
    for i in range(num_groups):
        groups.append([])
    people = Person.objects.filter(namelist=namelist).order_by('?')
    namelist_pairings = Pairing.objects.filter(namelist=namelist)
    should_be = (people.count() * (people.count() + 1)) / 2
    if namelist_pairings.count() < should_be:
        for person in people:
            pairings = namelist_pairings.filter(people__id=person.id)
            for person_2 in people:
                if person_2 != person:
                    pairing = pairings.filter(people__id=person_2.id)
                    if pairing.count() == 0:
                        pairing = Pairing.objects.create(namelist=namelist)
                        pairing.people.add(person)
                        pairing.people.add(person_2)
                        pairing.save()
    all_pairings = Pairing.objects.filter(namelist=namelist).order_by('count')
    group_num = 0
    remaining_people = people
    #Sort algorithm
    next_person = None
    while remaining_people.count() != 0:
        group = groups[group_num]
        if len(groups[group_num]) == 0 and not next_person:
            person = remaining_people[0]
            highest_pair = Pairings.objects.filter(people__id=person.id).order_by('-count')[0]
            for a_person in highest_pair:
                if a_person != person:
                    next_person = a_person
        elif len(groups[group_num]) == 0 and next_person:
            person = next_person
            highest_pair = Pairings.objects.filter(people__id=person.id).order_by('-count')[0]
            for a_person in highest_pair:
                if a_person != person:
                    next_person = a_person
        else:
            lowest_tally = False
            for person_1 in remaining_people:
                this_tally = 0
                for person_2 in group:
                    this_pairing = all_pairings.filter(people__id=person_1.id)
                    this_pairing = this_pairing.get(people__id=person_2.id)
                    this_tally += this_pairing.count
                if lowest_tally is False or this_tally < lowest_tally:
                    lowest_tally = this_tally
                    person = person_1                
        
        group.append(person)
        remaining_people = remaining_people.filter(~Q(id=person.id))
        group_num += 1
        if group_num == num_groups:
            group_num = 0
              
    return groups
