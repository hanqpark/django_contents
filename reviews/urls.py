from django.urls import path
from reviews import views

app_name="reviews"

urlpatterns = [
  path("<int:pk>", views.create_review, name="review"),
  path("<int:obj_pk>/<int:review_pk>/delete", views.delete_review, name="delete"),
  path("write/<int:pk>", views.write_review, name="write"),
]