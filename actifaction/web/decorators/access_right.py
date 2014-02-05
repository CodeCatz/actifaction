__author__ = 'svetka'

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from web.processors.action import get_action

def permission_to_event(func):
    def decorator(request,*args,**kwargs):
        action = get_action(kwargs['action_id'])
        if request.user.id == action.organizer.id:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect(reverse('web.index'))

    return decorator




