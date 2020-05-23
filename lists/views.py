from django.http import HttpResponse
from django.shortcuts import render

def home_page(request):
    html = (
        "<html>"
        "<title>To-Do lists</title>"
        "</html>"
    )
    return render(request, "home.html")
    return HttpResponse(html)
