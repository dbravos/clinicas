
# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("🚀 FUNCIONA - PRUEBA MÍNIMA")