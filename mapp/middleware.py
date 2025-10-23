# middleware.py - CREA este archivo en tu app mapp
class ClinicaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Pasar la request al manager para que pueda acceder a la sesión
        from .models import ClinicaManager
        ClinicaManager._request = request

        response = self.get_response(request)
        return response