"""API endpoints."""

import json
from django.http import HttpResponse, HttpResponseBadRequest

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
