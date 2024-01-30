#!/usr/bin/env python3

"""
Author: Nickolos Monk
Date: 
License: MIT
"""

from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name = 'index'),

    path("<int:pk>/", views.DetailView.as_view(), name = 'detail'),

    path("<int:pk>/results/", views.ResultsView.as_view(), name = 'results'),

    path("<int:question_id>/vote/", views.vote, name = 'vote'),

    # Ex. /polls/
    #path("", views.index, name="index"),
    # Ex. /polls/5/
    #path("<int:question_id>/", views.detail, name="detail"),
    # Ex. /polls/5/results/
    #path("<int:question_id>/results/", views.results, name="results"),
    # Ex. /polls/5/vote/
    #path("<int:question_id>/vote/", views.vote, name="vote"),
]
