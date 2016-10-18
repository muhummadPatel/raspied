from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET


@require_GET
def index(request):
    if request.user.is_authenticated():
        return redirect('students:home')
    else:
        return render(request, 'index.html', {})
