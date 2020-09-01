from datetime import datetime
from django.utils.timezone import make_aware


def user_activity_middleware(get_response):

    def middleware(request):
        response = get_response(request)

        user = request.user
        if user.is_authenticated:
            # user.last_request = make_aware(datetime.now())
            user.last_request = datetime.now()
            user.save()

        return response

    return middleware
