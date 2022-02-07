"""
Possible functions for the ``PRIVATE_STORAGE_AUTH_FUNCTION`` setting.
"""
import experiments.models as Experiment_model

def allow_staff(private_file):
    request = private_file.request
    exp = Experiment_model.Product.objects.filter(screenshots=private_file.relative_name, user=request.user)
    return exp and exp.exists()
