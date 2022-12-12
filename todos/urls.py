from django.urls import path
from .views import ListTodo, TodoRUD, TodoCreateView, TodoFilterView

urlpatterns = [
    path('<int:pk>/', TodoRUD.as_view()),
    path('', ListTodo.as_view()),
    path('create/', TodoCreateView.as_view()),

    path('filter/', TodoFilterView.as_view())

]
