from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def profile_view(request):
    user = request.user
    return render(request, "profile.html", {"user": user})
