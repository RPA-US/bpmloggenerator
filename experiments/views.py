from django.shortcuts import render
# Create your views here.
import os
from rest_framework import generics, status, viewsets  # , permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from private_storage.views import PrivateStorageDetailView
from .models import Experiment, Screenshot, Variations, ExperimentStatusChoice
from .serializers import ExperimentSerializer, VariationsSerializer
from users.models import CustomUser
from .functions import execute_experiment
from django.http import FileResponse
from rest_framework.decorators import api_view
from django.db import transaction
import json
from agosuirpa.system_configuration import sep
from django.shortcuts import get_object_or_404
import datetime
from django.utils import timezone
from .utils import compress_experiment, upload_mockups
from PIL import Image

def json_attributes_load(att):
    if att:
        att = json.loads(att)
    return att


class VariationsViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticatedUser]
    queryset = Variations.objects.all()
    serializer_class = VariationsSerializer


@api_view(('GET',))
def check_experiment_percentage(request, id):
    user = request.user
    res = Response({'message': 'The id experiment not corresponds to one of yours'},
                   status=status.HTTP_401_UNAUTHORIZED)
    percentage = None
    if(user.is_anonymous is False):
        user = CustomUser.objects.get(id=request.user.id)
        percentage = Experiment.objects.filter(
            pk=id, user=user.id).values('is_being_processed')
    if percentage:
        res = Response(
            {'experiment_is_being_processed': percentage[0]['is_being_processed'], 'message': 'Info. retrieved'}, status=status.HTTP_200_OK)
    return res


class ExperimentView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticatedUser]
    serializer_class = ExperimentSerializer

    def get_queryset(self):
        user = self.request.user
        params = self.request.query_params
        experiments = []
        if(user.is_anonymous is False):
            user = CustomUser.objects.get(id=self.request.user.id)
            if "public" in params and params["public"] == "true":
                experiments = Experiment.objects.filter(is_active=True, public=True).order_by("-created_at")
            else:
                experiments = Experiment.objects.filter(user=user.id, is_active=True).order_by("-created_at")
        else:
            experiments = Experiment.objects.filter(public=True, is_active=True).order_by("-created_at")
        return experiments

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id=self.request.user.id)
        except:
            return Response({"message": "No user found"}, status=status.HTTP_404_NOT_FOUND)

        msg = 'ok, created'
        st = status.HTTP_201_CREATED

        execute_mode = request.data.get('execute_mode')
        try:
            if execute_mode:
                if request.data.get('number_scenarios') and int(request.data.get('number_scenarios')) > 0 and not ('scenarios_conf' in request.data):
                    return Response({"message": "POST experiment executing - Incomplete data: Number scenarios greater than 1 and no scenario configuration included!"}, status=status.HTTP_400_BAD_REQUEST)
                for data in ['size_balance', 'name', 'number_scenarios',
                             'variability_conf', 'screenshots',
                             'special_colnames', 'screenshot_name_generation_function']:
                    if not data in request.data:
                        return Response({"message": "POST experiment executing - Incomplete data: " + data + " not included"}, status=status.HTTP_400_BAD_REQUEST)
            elif request.data.get('status') == ExperimentStatusChoice.PR.value:
                for data in ['name', 'screenshots',
                             'special_colnames', 'screenshot_name_generation_function']:
                    if not data in request.data:
                        return Response({"message": "POST experiment pre-saving - Incomplete data: " + data + " not included"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                for data in ['name', 'special_colnames', 'screenshot_name_generation_function']:
                    if not data in request.data:
                        return Response({"message": "POST experiment saving - Incomplete data: " + data + " not included"}, status=status.HTTP_400_BAD_REQUEST)

            # with transaction.atomic():
            experiment = Experiment(
                size_balance=json_attributes_load(
                    request.data.get('size_balance')),
                name=request.data.get('name'),
                description=request.data.get('description'),
                number_scenarios=int(request.data.get('number_scenarios')) if request.data.get(
                    'number_scenarios') else None,
                variability_conf=json_attributes_load(request.data.get(
                    'variability_conf')) if request.data.get('variability_conf') else None,
                scenarios_conf=json_attributes_load(request.data.get(
                    'scenarios_conf')) if request.data.get('scenarios_conf') else None,
                special_colnames=json_attributes_load(
                    request.data.get('special_colnames')),
                screenshots=request.data.get('screenshots'),
                user=user,
                status=ExperimentStatusChoice.PR.value,
                screenshot_name_generation_function=request.data.get(
                    'screenshot_name_generation_function'),
                last_edition=datetime.datetime.now(tz=timezone.utc),
                is_being_processed = 0
            )

            experiment.save()

            if 'screenshots' in request.data:
                # if experiment.status == ExperimentStatusChoice.PR or experiment.status == ExperimentStatusChoice.LA:
                path_without_fileextension = upload_mockups(
                    'privatefiles'+sep+experiment.screenshots.name)
                experiment.screenshots_path = path_without_fileextension
                associate_screenshots_files(experiment)

            if execute_mode:
                experiment.execution_start = datetime.datetime.now(
                    tz=timezone.utc)
                experiment.is_being_processed = 1
                experiment.foldername = execute_experiment(experiment)
                experiment.execution_finish = datetime.datetime.now(
                    tz=timezone.utc)
                experiment.is_being_processed = 100
                experiment.is_active = True
                experiment.status = ExperimentStatusChoice.LA.value
            elif request.data.get('status') != ExperimentStatusChoice.PR.value:
                experiment.status = ExperimentStatusChoice.SA.value
            experiment.save()

            response_content = {"message": msg,
                                "id": experiment.id, "status": experiment.status}

        except Exception as e:
            msg = 'Some of atributes are invalid: ' + str(e)
            st = status.HTTP_422_UNPROCESSABLE_ENTITY
            response_content = {"message": msg}

        return Response(response_content, status=st)


class ExperimentUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExperimentSerializer
    queryset = Experiment.objects.all()
    lookup_field = 'id'

    def get(self, request, id, *args, **kwargs):
        exp = Experiment.objects.get(id=id)
        if exp.public or exp.user.id==request.user.id:
            res = Response({
                "owned": exp.user.id==request.user.id,
                "experiment": ExperimentSerializer(exp).data
            })
        else:
            res = Response({"message": "No user found"}, status=status.HTTP_404_NOT_FOUND)
        return res

    def put(self, request, id, *args, **kwars):

        try:
            user = CustomUser.objects.get(id=self.request.user.id)
            experiment = get_object_or_404(Experiment, user=user.id, id=id)
        except:
            return Response({"message": "No user found"}, status=status.HTTP_404_NOT_FOUND)

        msg = 'ok, created'
        st = status.HTTP_201_CREATED

        execute_mode = request.data.get('execute_mode')

        try:
            if experiment.status == ExperimentStatusChoice.LA.value:
                if request.data.get('public'):
                    if request.data.get('public') == "false":
                        experiment.public = False
                    if request.data.get('public') == "true":
                        experiment.public = True
                    experiment.save()
                response_content = {"message": msg,
                "id": experiment.id, "status": experiment.status}
            else:
                if execute_mode:
                    if request.data.get('number_scenarios') and int(request.data.get('number_scenarios')) > 0 and not ('scenarios_conf' in request.data):
                        return Response({"message": "POST experiment executing - Incomplete data: Number scenarios greater than 1 and no scenario configuration included!"}, status=status.HTTP_400_BAD_REQUEST)
                    for data in ['size_balance', 'name', 'number_scenarios',
                                'variability_conf',
                                'special_colnames', 'screenshot_name_generation_function']:
                        if not data in request.data:
                            return Response({"message": "POST experiment executing - Incomplete data: " + data + " not included"}, status=status.HTTP_400_BAD_REQUEST)
                    if not 'screenshots_path' in request.data and not 'screenshots' in request.data:
                        return Response({"message": "POST experiment executing - Incomplete data: " + data + " not included"}, status=status.HTTP_400_BAD_REQUEST)
                elif request.data.get('status') == ExperimentStatusChoice.PR.value:
                    for data in ['name',
                                'special_colnames', 'screenshot_name_generation_function']:
                        if not data in request.data:
                            return Response({"message": "POST experiment pre-saving - Incomplete data: " + data + " not included"}, status=status.HTTP_400_BAD_REQUEST)
                    if not 'screenshots_path' in request.data and not 'screenshots' in request.data:
                        return Response({"message": "POST experiment executing - Incomplete data: " + data + " not included"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    for data in ['name', 'special_colnames', 'screenshot_name_generation_function']:
                        if not data in request.data:
                            return Response({"message": "POST experiment saving - Incomplete data: " + data + " not included"}, status=status.HTTP_400_BAD_REQUEST)

                experiment.size_balance = json_attributes_load(
                    request.data.get('size_balance'))
                experiment.name = request.data.get('name')
                experiment.description = request.data.get('description')
                experiment.number_scenarios = int(request.data.get(
                    'number_scenarios')) if request.data.get('number_scenarios') else None
                experiment.variability_conf = json_attributes_load(request.data.get(
                    'variability_conf')) if request.data.get('variability_conf') else None
                experiment.scenarios_conf = json_attributes_load(request.data.get(
                    'scenarios_conf')) if request.data.get('scenarios_conf') else None
                experiment.special_colnames = json_attributes_load(
                    request.data.get('special_colnames'))
                experiment.screenshots = request.data.get('screenshots')
                experiment.screenshot_name_generation_function = request.data.get(
                    'screenshot_name_generation_function')
                experiment.last_edition = datetime.datetime.now(tz=timezone.utc)
                if request.data.get('screenshots') == "true":
                    experiment.public = True
                else:
                    experiment.public = False

                experiment.save()

                if 'screenshots' in request.data and experiment.screenshots != request.data.get('screenshots'):
                    path_without_fileextension = upload_mockups(
                        'privatefiles'+sep+experiment.screenshots.name)
                    experiment.screenshots_path = path_without_fileextension
                    associate_screenshots_files(experiment)

                if execute_mode:
                    experiment.execution_start = datetime.datetime.now(
                        tz=timezone.utc)
                    experiment.is_being_processed = 1
                    experiment.foldername = execute_experiment(experiment)
                    experiment.execution_finish = datetime.datetime.now(
                        tz=timezone.utc)
                    experiment.is_being_processed = 100
                    experiment.is_active = True
                    experiment.status = ExperimentStatusChoice.LA.value
                elif request.data.get('status') != ExperimentStatusChoice.PR.value:
                    experiment.status = ExperimentStatusChoice.SA.value
                experiment.save()

                response_content = {"message": msg,
                                    "id": experiment.id, "status": experiment.status}

        except Exception as e:
            msg = 'Some of atributes are invalid: ' + str(e)
            st = status.HTTP_422_UNPROCESSABLE_ENTITY
            response_content = {"message": msg}
        return Response(response_content, status=st)

    def delete(self, request, id, *args, **kwars):
        st = status.HTTP_200_OK
        msg = 'deleted'

        try:
            experiment = get_object_or_404(
                Experiment, pk=id, user=request.user.id)
            experiment.delete()
        except Exception as e:
            msg = 'Cannot delete experiment: ' + str(e)
            st = status.HTTP_409_CONFLICT

        return Response(msg, status=st)


class SmallPagesPagination(PageNumberPagination):
    page_size = 8


class ListPaginatedExperimentAPIView(generics.ListAPIView):
    """
    List active experiments
    """
    pagination_class = SmallPagesPagination
    # permission_classes = [IsAuthenticatedAdmin]
    serializer_class = ExperimentSerializer

    def get_queryset(self):
        user = self.request.user
        if(user.is_anonymous is False):
            user_id = CustomUser.objects.get(user_account=self.request.user).id
            queryset = Experiment.objects.filter(user=user_id, is_active=True)
        return queryset


class DownloadExperiment(generics.RetrieveAPIView):
    """
    Download compress experiment
    """

    def get(self, request, *args, **kwargs):
        msg = "Experiment downloaded"
        st = status.HTTP_200_OK
        user = get_object_or_404(CustomUser, id=request.user.id)
        if(user.is_anonymous is False):
            experiment = get_object_or_404(
                Experiment, user=user.id, is_being_processed=100, id=kwargs["pk"])
            try:
                splitted = experiment.foldername.split(sep)
                val = splitted[len(splitted)-1]
                zip_experiment = compress_experiment(
                    experiment.foldername, val)
                filename = val + ".zip"
                response = FileResponse(open(zip_experiment, 'rb'))
                response['Content-Disposition'] = 'attachment; filename="%s"' % filename
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            except Exception as e:
                response = Response(
                    {"message": "Experiment error: " + str(e)}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            response = Response(
                {"message": "No user valid" + str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        return response


def associate_experiment(user):
    basic_path_template_experiments = 'resources'+sep+'template_experiments'+sep
    experiments = Experiment.objects.filter(user=user.id, is_active=True)
    if experiments == None or not experiments:
        data_complete = json.load(
            open(basic_path_template_experiments+'template_experiments.json'))
        for data in data_complete['results']:
            size_balance = data['size_balance']
            name = data['name']
            description = data['description']
            number_scenarios = int(data['number_scenarios'])
            variability_conf = data['variability_conf']
            screenshots = data['screenshots']
            screenshots_path = data['screenshots_path']
            special_colnames = data['special_colnames']
            screenshot_name_generation_function = data['screenshot_name_generation_function']
            foldername = data['foldername']
            scenarios_conf = data['scenarios_conf']
            last_edition = datetime.datetime.now(tz=timezone.utc)
            execution_start = datetime.datetime.now(tz=timezone.utc)
            execution_finish = datetime.datetime.now(tz=timezone.utc)

            experiment = Experiment(
                scenarios_conf=scenarios_conf,
                size_balance=size_balance,
                name=name,
                description=description,
                number_scenarios=number_scenarios,
                variability_conf=variability_conf,
                special_colnames=special_colnames,
                screenshots=screenshots,
                foldername=foldername,
                is_being_processed=100,
                is_active=True,
                user=user,
                screenshot_name_generation_function=screenshot_name_generation_function,
                screenshots_path=screenshots_path,
                status=ExperimentStatusChoice.LA.value,
                execution_start=execution_start,
                execution_finish=execution_finish,
                last_edition=datetime.datetime.now(tz=timezone.utc),
                public=False
            )
            experiment.user = user
            experiment.save()

# https://github.com/edoburu/django-private-storage
# class ScreenshotDownloadView(PrivateStorageDetailView):
#     model = Screenshot
#     model_file_field = 'image'

#     def get_queryset(self):
#         # Make sure only certain objects can be accessed.
#         return super().get_queryset().filter(...)

#     def can_access_file(self, private_file):
#         # When the object can be accessed, the file may be downloaded.
#         # This overrides PRIVATE_STORAGE_AUTH_FUNCTION
#         return True


def associate_screenshots_files(experiment):
    for root, directories, file in os.walk(experiment.screenshots_path):
        for file in file:
            if(file.endswith(".png") or file.endswith(".jpg")):
                image = Image.open(os.path.join(root, file))
                aux = experiment.screenshots_path.split(sep)
                width, height = image.size
                relative_path = aux[len(aux)-1]+sep+file
                screenshot = Screenshot(
                    relative_path=relative_path, width=width, height=height, image=file, experiment=experiment)
                screenshot.save()
