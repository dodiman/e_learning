from django.urls import path

from . import views

urlpatterns = [
    path("about/", views.about, name="about"),
    path("matakuliah/", views.matakuliah, name="matakuliah"),
    path("matakuliah/<int:id>/", views.matakuliah_detail, name="matakuliah_detail"),
    path("kirim-tugas/<int:id_matakuliah>/", views.kirim_tugas, name="kirim_tugas"),
    path("daftar-tugas/<int:id_matakuliah>/", views.daftar_tugas, name="daftar_tugas"),
    path("tugas/<int:id>/", views.tugas_detail, name="tugas_detail"),
    path("", views.home, name="home"),
]