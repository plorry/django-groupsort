from groupsort.models import NameList, Person, Pairing
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q

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
        
def save(request):
    get = request.GET.copy()
    
        
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
    print len(groups)
    people = Person.objects.filter(namelist=namelist).order_by('?')
    for person in people:
        pairings = Pairing.objects.filter(people__id=person.id)
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
    while remaining_people.count() != 0:
        group = groups[group_num]
        if len(groups[group_num]) == 0:
            person = remaining_people[0]
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