from django.conf import settings

def balanced_uri(request):
    return {
        'BALANCED_URI': settings.BALANCED_URI
    }
