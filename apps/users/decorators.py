from django.http import HttpResponseForbidden


def admin_required(function):
    def wrapper(request, *args, **kwargs):
        try:
            if request.user.role != 0:
                return HttpResponseForbidden('403 Forbidden')
            return function(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return HttpResponseForbidden('403 Forbidden')
    return wrapper