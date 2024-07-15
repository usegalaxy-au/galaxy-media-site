"""API endpoints."""

import json
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest

from utils.institution import is_institution_email
from .forms import LabFeedbackForm

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


def lab_feedback(request, subdomain):
    """Process feedback form for *.usegalaxy.org.au subsites."""
    if request.method != 'POST':
        return HttpResponseBadRequest()
    form = LabFeedbackForm(request.POST)
    if form.is_valid():
        form.dispatch(subject=f"{subdomain.title()} Lab feedback")
        return JsonResponse({'success': True})
    return JsonResponse({
        'success': False,
        'errors_json': form.errors.as_json(),
    })


def validate_institutional_email(request):
    """Check given email against list of Australian institutions."""
    if request.method != 'GET':
        return HttpResponseBadRequest()
    email = request.GET.get('email')
    if not email:
        return HttpResponseBadRequest()
    try:
        if is_institution_email(email):
            return JsonResponse({'valid': True})
        return JsonResponse({'valid': False})
    except ValueError:
        return JsonResponse({'error': 'Please enter a valid email address.'})
