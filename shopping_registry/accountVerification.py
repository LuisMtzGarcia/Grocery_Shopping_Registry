from django.core.exceptions import PermissionDenied

from .models import Purchase

def check_account(username, object=Purchase.objects.none()):
    """Checks if the user is using the demo account and if they're the owner of 
        the object."""
        
    # Demo account check.
    if username == 'supercuenta':
        raise PermissionDenied

    # Owner of the object check.
    if hasattr(object, 'owner'):
        if username != object.owner.username:
            raise Http404