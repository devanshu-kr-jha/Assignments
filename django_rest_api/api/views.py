from django.http import HttpResponse


def test(request):
    return HttpResponse("<h2>Hello world</h2>")


# Create your views here.
