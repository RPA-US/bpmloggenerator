"""
Possible functions for the ``PRIVATE_STORAGE_AUTH_FUNCTION`` setting.
"""
import wizard.models as Wizard_model
from users.models import CustomUser
from rest_framework.authtoken.models import Token


def allow_staff(private_file):
    res = False
    request = private_file.request
    token = request.headers._store['authorization'][1].split(" ")[1]
    user = Token.objects.filter(key = token)[0].user
    guicomponent=Wizard_model.GUIComponent.objects.filter(path=private_file.relative_name)
    if guicomponent:
        guicomponent=guicomponent[0]
        if guicomponent.preload:
            res=user
        else:
            res=user == guicomponent.user
    return res
