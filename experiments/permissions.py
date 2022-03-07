"""
Possible functions for the ``PRIVATE_STORAGE_AUTH_FUNCTION`` setting.
"""
import experiments.models as Experiments_model
from users.models import CustomUser
from rest_framework.authtoken.models import Token


def allow_staff(private_file):
    res = False
    request = private_file.request
    token = request.headers._store['authorization'][1].split(" ")[1]
    user = Token.objects.filter(key = token)[0].user
    screenshot=Experiments_model.Screenshot.objects.filter(
        relative_path=private_file.relative_name)
    if screenshot:
        screenshot=screenshot[0]
        res=user == screenshot.experiment.user
    return res
