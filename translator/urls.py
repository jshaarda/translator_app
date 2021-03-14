from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tranG/', views.TranGView.as_view(), kwargs={'lang':'g'}, name='tranG'),
    path('tranE/', views.TranEView.as_view(), kwargs={'lang':'e'}, name='tranE'),
    path('tranG/tranGresults/', views.TranGResultsView.as_view(), name='trang_results'),
    path('tranE/tranEresults/', views.TranEResultsView.as_view(), name='trane_results'),
    path('quiz/', views.quiz, name='quiz'),
    path('quiz/detail', views.QuizDetailView.as_view(), name='quiz_detail'),
    path('quiz/result', views.QuizResultView.as_view(), name='quiz_result'),
]
