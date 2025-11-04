class ClinicaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from .models import ClinicaManager
        ClinicaManager._request = request
        response = self.get_response(request)
        return response