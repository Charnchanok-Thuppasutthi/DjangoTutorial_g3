from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('',views.menu , name='menu'),
    path('poll/', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('poll/sort/', views.sortingQuestion , name='sortQ'),
    path('<int:question_id>/results/sort/', views.sortingVote , name='sortV'),
]