"""
Possible functions for the ``PRIVATE_STORAGE_AUTH_FUNCTION`` setting.
"""
import experiments.models as Experiments_model

def allow_staff(private_file):
    res = False
    request = private_file.request
    screenshot = Experiments_model.Screenshot.objects.filter(relative_path=private_file.relative_name)
    if screenshot:
        screenshot = screenshot[0]
        user = screenshot.experiment.user_id
        res = user == request.user.id
    return res