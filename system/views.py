import os
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from ltosim import settings
from ltosim.settings import MAX_LESSON1_LEVELS_ENV, MAX_LESSON2_LEVELS_ENV, MAX_LESSON3_LEVELS_ENV
from system.forms import NewUserForm
from django.contrib import messages
from rest_framework import viewsets, mixins, generics
from system.mixins import SuperuserRequiredMixin
from system.models import Announcement, CustomUser, Download, Question, Reviewer, Score
from system.serializers import QuestionSerializer, ReviewerSerializer, ScoreSerializer
from django.views.generic import ListView
from django_tables2.config import RequestConfig
from system.tables import AnnouncementTable, ScoreTable
from .filters import ScoreFilter
from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django.db.models import Max
from django.contrib.auth.views import LoginView
from rest_framework.permissions import AllowAny
from django.views.decorators.gzip import gzip_page
from django.utils import translation
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test
import requests
from django.http import JsonResponse

from .models import TopUpRecord
from .serializers import TopUpRecordSerializer

class TopUpRecordViewSet(viewsets.ModelViewSet):
    queryset = TopUpRecord.objects.all()
    serializer_class = TopUpRecordSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        email = self.request.query_params.get('email', None)
        if email is not None:
            queryset = queryset.filter(email=email)
        return queryset

def index(request):
    context = {}
    return render(request, 'pages/lessons.html', context)

# @gzip_page
def play(request):
    context = {}
    return render(request, 'index.html', context)

class MyLoginView(LoginView):
    # form_class=LoginForm
    redirect_authenticated_user=True
    template_name='registration/login.html'

    def get_success_url(self):
        # write your logic here
        if self.request.user.is_superuser:
            return '/progress/'
        return '/'


def register_request(request):
    context = {}
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("system:index")
        context['form_errors'] = form.errors
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context["register_form"] = form
    return render(request=request, template_name="registration/register.html", context=context)


class ScoreViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = (AllowAny,)


class AnnouncementListView(SingleTableView):
    model = Announcement
    context_object_name = 'announcement_list'
    template_name = 'pages/announcements.html'

    def get_queryset(self):
        qs = super().get_queryset()
        now = timezone.now()
        return qs.filter(active=True, date_valid__gt=now)


class DownloadListView(SingleTableView):
    model = Download
    context_object_name = 'download_list'
    template_name = 'pages/downloads.html'

    def get_queryset(self):
        qs = super().get_queryset()

        return qs.filter(downloadable=True)
    

class ScoreListView(LoginRequiredMixin, SuperuserRequiredMixin, SingleTableView, FilterView):
    model = Score
    table_class = ScoreTable
    template_name = 'pages/progress.html'
    filterset_class = ScoreFilter
    table_pagination = {
        'per_page': 10,
    }
    strict=False

    def get_queryset(self):
        qs = super().get_queryset()

        user = self.request.GET.get('user', None)
        if user is None or len(user) == 0:
            return qs.order_by('date').reverse()
        else:
            return qs.filter(user=user).order_by('date').reverse()

    def get_context_data(self, **kwargs):
        context = super(ScoreListView, self).get_context_data(**kwargs)
        user = self.request.GET.get('user', None)
        species=self.get_queryset()
        f = self.filterset_class(self.request.GET, queryset=species)
        context['filter'] = f
        table = self.table_class(f.qs)
        RequestConfig(self.request, paginate={"per_page": 10}).configure(table)
        context['table'] = table

        session_no = self.request.GET.get('session_no', "")
        if len(session_no) == 0:
            session_no = 1
        context['session_progress_lesson1'] = get_progress(user, session_no, MAX_LESSON1_LEVELS_ENV, 'Learn ABC')
        context['session_progress_lesson2'] = get_progress(user, session_no, MAX_LESSON2_LEVELS_ENV, 'Spelling')
        context['session_progress_lesson3'] = get_progress(user, session_no, MAX_LESSON3_LEVELS_ENV, 'Math')

        max_sessions = 1
        
        if user is None or len(user) == 0:
            max = Score.objects.all().aggregate(Max('session_no'))
        else:
            max = Score.objects.filter(user=user).aggregate(Max('session_no'))
            context['user_to_progress'] = CustomUser.objects.get(id=user)
        if not 'session_no__max' in max or max['session_no__max'] is None:
            max_sessions = 1
        else:
            max_sessions = max['session_no__max']
        context['max_sessions'] = range(max_sessions)

        return context

def get_progress(user, session_no, lesson_max, lesson_name):
    if user is None:
        return 0
    progress = 0
    try:
        max = int(lesson_max)
        current = Score.objects.filter(user__id=user, session_no=session_no, lesson_name=lesson_name).count()
        
        progress = (current / max) * 100
    except Exception:
        pass

    return round(min(progress, 100), 2)

    
class ReviewerViewSet(viewsets.ModelViewSet):
    queryset = Reviewer.objects.all().order_by('order_position')
    serializer_class = ReviewerSerializer

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        lang = request.query_params.get('lang', 'en')
        translation.activate(lang)
        return request

    def finalize_response(self, request, response, *args, **kwargs):
        translation.deactivate()
        return super().finalize_response(request, response, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category is not None:
            queryset = queryset.filter(category=category)
        return queryset
    
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def user_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to view this page.")
    # Logic for the view
    return render(request, 'admin/user_list.html')

@user_passes_test(is_admin)
def get_users(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to view this page.")
    api_url = "https://5E1B8.playfabapi.com/Admin/GetPlayersInSegment"
    request_data = {
        "SegmentId": "7B295BFF21FA3646"
    }
    headers = {
        "Content-Type": "application/json",
        "X-SecretKey": settings.PLAYFAB_SECRET_KEY  # Load the secret key from settings
    }

    try:
        response = requests.post(api_url, headers=headers, json=request_data)
        response_data = response.json()
        if response.status_code == 200 and response_data.get("status") == "OK":
            return JsonResponse(response_data)
        else:
            return JsonResponse({"error": "Error fetching player data"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@user_passes_test(is_admin)
def delete_user(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to view this page.")
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    # Get data from request
    playerId = request.POST.get('playerId', None)

    if playerId is None:
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    api_url = "https://5E1B8.playfabapi.com/Admin/DeleteMasterPlayerAccount"
    headers = {
        "Content-Type": "application/json",
        "X-SecretKey": settings.PLAYFAB_SECRET_KEY  # Load the secret key from settings
    }
    request_data = {
        "PlayFabId": playerId
    }

    try:
        response = requests.post(api_url, headers=headers, json=request_data)
        response_data = response.json()
        if response.status_code == 200 and response_data.get("status") == "OK":
            return JsonResponse(response_data)
        else:
            return JsonResponse({f"error": "Error deleting user: {response_data}"}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)