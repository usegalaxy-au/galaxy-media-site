"""Redirect specific requests."""

from django.shortcuts import redirect


def homepage(request):
    """Redirect requests to the homepage."""
    return redirect('/')


def support(request):
    """Redirect requests to the homepage."""
    return redirect('/request')


def user_request_alphafold(request):
    """Redirect alphafold requests to generic access request form."""
    return redirect('/request/access/alphafold')


def institutions(request):
    """Redirect alphafold requests to generic access request form."""
    return redirect('/list-of-institutions.html')
