"""Redirect specific requests."""

from django.shortcuts import redirect


def homepage(request):
    """Redirect requests to the homepage."""
    return redirect('/')


def support(request):
    """Redirect requests to the homepage."""
    return redirect('/request')
