"""
Possible functions for the ``PRIVATE_STORAGE_AUTH_FUNCTION`` setting.
"""
from wizard.models import GUIComponent
from experiments.models import Screenshot
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def allow_staff(private_file):
    res = False
    request = private_file.request
    token = request.headers._store['authorization'][1].split(" ")[1]
    user = Token.objects.filter(key = token)[0].user
    screenshot = False
    guicomponent = False
    if "GUI_components" in private_file.relative_name:
        guicomponent=GUIComponent.objects.filter(path=private_file.relative_name)
    else:
        screenshot=Screenshot.objects.filter(relative_path=private_file.relative_name)
    if screenshot:
        screenshot=screenshot[0]
        res=user == screenshot.experiment.user
    if guicomponent:
        guicomponent=guicomponent[0]
        if guicomponent.preloaded:
            res=user
        else:
            res=user == guicomponent.user
    return res