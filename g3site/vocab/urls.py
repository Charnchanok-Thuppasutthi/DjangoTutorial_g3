from django.urls import path

from . import views

app_name='vocab'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('search/',views.search, name="searchWord"),
    path('addWord/',views.addWordView, name='addWord'),
    path('addWord/submit/',views.submit,name='submit'),
]