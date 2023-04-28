"""API endpoints."""

import json
from django.core.exceptions import SuspiciousOperation
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest

from .forms import SupportRequestForm

SESSION_COUNT_LIMIT = 5


def dismiss_notice(request):
    """Mark the given notice as dimissed for this session."""
    if request.method != 'POST':
        return HttpResponseBadRequest()

    data = json.loads(request.body)
    datetime_modified = data.get('datetime_modified')
    if not datetime_modified:
        return HttpResponseBadRequest()

    if request.session.get('dismissed_notices'):
        request.session['dismissed_notices'] = (
            [datetime_modified]
            + request.session['dismissed_notices'][:SESSION_COUNT_LIMIT]
        )
    else:
        request.session['dismissed_notices'] = [datetime_modified]

    return HttpResponse('OK', status=201)


def subdomain_feedback(request, subdomain):
    """Process feedback form for *.usegalaxy.org.au subsites."""
    if request.method != 'POST':
        raise SuspiciousOperation
    form = SupportRequestForm(request.POST)
    if form.is_valid():
        form.dispatch(subject=f"{subdomain.title()} subdomain feedback")
        return JsonResponse({'success': True})
    return JsonResponse({
        'success': False,
        'errors_json': form.errors.as_json(),
    })
