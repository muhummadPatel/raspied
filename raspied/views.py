from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET


@require_GET
def index(request):
    """
    Render and return the index page or home page if the user is logged in.
    """

    if request.user.is_authenticated():
        return redirect('students:home')
    else:
        return render(request, 'index.html', {})
