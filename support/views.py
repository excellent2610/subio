from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib import messages

@login_required
def support_page(request):
    return render(request, "support/support.html")


@login_required
def become_supporter(request):
    if request.method == "POST":
        request.user.is_supporter = True
        request.user.save()
        messages.success(request, "Дякуємо за підтримку ❤️")
    return redirect("dashboard:index")

