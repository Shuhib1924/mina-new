from django.urls import redirect


class MenuRedirect:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path == "detail":
            return redirect("menu")
        return self.get_response(request)
