"""Cache lab pages because rendering is expensive."""

from django.core.cache import cache
from django.utils.http import urlencode
from django.http import HttpResponse
from hashlib import md5

CACHE_KEY_IGNORE_GET_PARAMS = (
    'cache',
)


class LabCache:
    @staticmethod
    def get(request):
        if request.GET.get('cache', '').lower() == 'false':
            return

        cache_key = _generate_cache_key(request)
        body = cache.get(cache_key)
        if body:
            response = HttpResponse(body)
            response['X-Cache-Status'] = 'HIT'
            return response

    @staticmethod
    def put(request, body):
        cache_key = _generate_cache_key(request)
        cache.set(cache_key, body, timeout=3600)
        response = HttpResponse(body)
        response['X-Cache-Status'] = 'MISS'
        return response


def _generate_cache_key(request):
    """Create a unique cache key from request path."""
    params = {
        k: v for k, v in request.GET.items()
        if k not in CACHE_KEY_IGNORE_GET_PARAMS
    }
    key = f"{request.path}?{urlencode(params)}"
    return md5(key.encode('utf-8')).hexdigest()
