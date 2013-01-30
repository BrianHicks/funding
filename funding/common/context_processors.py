from django.conf import settings

def balanced_uri(request):
    return {
        'balanced_uri': settings.BALANCED_URI
    }
