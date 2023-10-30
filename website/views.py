from django.shortcuts import render

# Create your views here.

def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')


def Privacy_Policy(request):
    return render(request, 'privacy_policy.html')