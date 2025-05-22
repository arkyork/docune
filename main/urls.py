from django.urls import path

from . import views

app_name = "main"  # 名前空間


urlpatterns = [
    path("", views.RefList.as_view(), name="list"),
    path("new/", views.RefCreate.as_view(), name="create"),
    path("<int:pk>/edit/", views.RefUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", views.RefDelete.as_view(), name="delete"),
    path("<int:pk>/pdf/", views.pdf_view, name="reference_pdf"),
    path("<int:pk>/", views.ref_detail, name="reference_detail"),
    path("<int:pk>/update-progress/", views.update_progress, name="update_progress"),
    path("api/similar/<int:pk>/", views.similar_references_api, name="similar_api"),

]
