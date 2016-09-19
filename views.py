from .models import NameList, Person, Pairing
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
import json


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return context


class GroupSortView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, request, *args, **kwargs):
        context = super(GroupSortView, self).get_context_data(*args, **kwargs)

        context.update({
            'groups': NameList.objects.all()
        })

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)

        return self.render_to_response(context)

class AjaxAddNamelistView(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST

        title = data.get('title')
        namelist = NameList.objects.create(
            title=title
        )
        response = {
            'namelist': {
                'id': namelist.id,
                'title': namelist.title
            }
        }

        return self.render_to_response(response)


class AjaxAddPersonView(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST

        name = data.get('name')
        namelist_id = data.get('namelist_id')

        person = Person.objects.create(
            name=name,
            namelist_id=namelist_id
        )

        response = {
            'person': {
                'id': person.id,
                'name': person.name,
                'namelist_id': person.namelist_id,
            }
        }

        return self.render_to_response(response)


class AjaxGetNamelists(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get(self, request, *args, **kwargs):
        namelists = NameList.objects.all()
        response = {
            'titles': [{'id': namelist.id, 'title': namelist.title} for namelist in namelists]
        }
        return self.render_to_response(response)


class AjaxGetNamelist(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get(self, request, *args, **kwargs):
        data = request.GET
        try:
            namelist = NameList.objects.get(id=data.get('namelist'))
            members = namelist.people.all()
            response = {
                'members': [{'id': person.id, 'name': person.name} for person in members]
            }
        except NameList.DoesNotExist:
            response = {'message': ['big', 'dog', 'fug']}
        return self.render_to_response(response)


class Group(object):
    def __init__(self, size):
        self.people = []
        self.size = size

    def add_person(self, person):
        self.people.append(person)

    def get_size(self):
        return self.size

    def is_full(self):
        return len(self.people) >= self.size

    def serialize(self):
        return [{'id': person.id, 'name': person.name} for person in self.people]


class AjaxCreateGroups(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def generate_pairs(self, namelist):
        people = namelist.people.all()

        for person1 in people:
            for person2 in people:
                if person1 != person2:
                    pairing = Pairing.objects.filter(people__in=[person1.id]).filter(people__in=[person2.id])
                    if pairing.count() == 0:
                        pairing = Pairing.objects.create(namelist=namelist)
                        pairing.people.add(person1)
                        pairing.people.add(person2)

    def get(self, request, *args, **kwargs):
        namelist = NameList.objects.get(id=request.GET.get('namelist_id'))
        groups_data = request.GET.get('groups').split(',')
        all_people = Person.objects.filter(namelist=namelist).order_by('?')
        groups = []

        self.generate_pairs(namelist)

        for group_size in groups_data:
            group = Group(int(group_size))
            groups.append(group)

        pairings = namelist.pairings.all().order_by('count')

        ordered_people = []
        for pairing in pairings:
            for person in pairing.people.all():
                if person not in ordered_people:
                    ordered_people.append(person)

        for group in groups:
            # get group leaders
            group.add_person(ordered_people.pop())

        while len(ordered_people) > 0:
            for group in groups:
                if group.is_full():
                    continue
                # Find the person with the lowest total matching count
                person_to_use = None
                lowest_count = None
                for person in ordered_people:
                    count = 0
                    for people in group.people:
                        pairing = pairings.filter(people__in=[people]).filter(people__in=[person])
                        count += pairing.count()
                    if lowest_count == None or count < lowest_count:
                        lowest_count = count
                        person_to_use = person
                ordered_people.remove(person_to_use)
                group.add_person(person_to_use)

        serialized_groups = [group.serialize() for group in groups]
        return self.render_to_response({
            'groups': serialized_groups
        })

'''
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
            highest_pair = Pairing.objects.filter(people__id=person.id).order_by('-count')[0]
            for a_person in highest_pair.people.all():
                if a_person != person:
                    next_person = a_person
        elif len(groups[group_num]) == 0 and next_person:
            person = next_person
            highest_pair = Pairing.objects.filter(people__id=person.id).order_by('-count')[0]
            for a_person in highest_pair.people.all():
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
'''
