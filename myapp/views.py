from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from .models import *
from .forms import *

# repository
from .repositories.matakuliah_repository import *
from .repositories.tugas_repository import *

# services
from .services import *

# csrf_token menual
from django.middleware.csrf import get_token


def home(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/about.html")


def matakuliah(request):
    list_matakuliah = MatakuliahRepository().get_all()
    qs = MatakuliahRepository().get_all()
    page_number = request.GET.get("page", 1)
    headers = get_headers_querset(qs, exclude=["tugas"])
    page_obj = tabel_dengan_navigasi_service(qs, page_number, per_page=5)

    context = {
        "list_matakuliah": list_matakuliah,
        "page_obj": page_obj,
        "headers": headers,
    }
    return render(request, "pages/matakuliah.html", context)


def matakuliah_detail(request, id):
    matakuliah = Matakuliah.objects.get(id=id)
    context = {"matakuliah": matakuliah}
    return render(request, "pages/matakuliah_detail.html", context)


def kirim_tugas(request, id_matakuliah):
    csrf_token = get_token(request)
    # matakuliah = Matakuliah.objects.get(id=id_matakuliah)
    matakuliah = MatakuliahRepository().get_by_id(id_matakuliah)

    form = KirimTugasForm()
    if request.method == "POST":
        form = KirimTugasForm(request.POST)
        if form.is_valid():
            # ambil data
            nim = form.cleaned_data["nim"]
            link_tugas = form.cleaned_data["link_tugas"]
            id_tugas = form.cleaned_data["tugas"]

            try:
                kirim_tugas_service(
                    nim=nim,
                    link_tugas=link_tugas,
                    id_matakuliah=id_matakuliah,
                    id_tugas=id_tugas,
                )
                messages.success(request, "Tugas berhasil dikirim")
                return redirect("kirim_tugas", id_matakuliah=id_matakuliah)
            except Exception as e:
                messages.error(request, str(e))

    messages.info(request, "silakan kirim tugas")
    # list_tugas = TugasRepository().get_by_matakuliah(id_matakuliah)
    list_tugas = (
        TugasRepository()
        .get_by_matakuliah(id_matakuliah)
        .filter(deadline__gte=timezone.now().date())
    )
    context = {
        "matakuliah": matakuliah,
        "form": form,
        "csrf_token": csrf_token,
        "list_tugas": list_tugas,
    }
    return render(request, "pages/kirim_tugas.html", context)


def daftar_tugas(request, id_matakuliah):
    matakuliah = MatakuliahRepository().get_by_id(id_matakuliah)
    list_tugas = get_by_matakuliah_service(id_matakuliah)
    
    headers = get_headers_querset(list_tugas, exclude=["sudah_lewat"])
    page_number = request.GET.get("page", 1)
    page_obj = get_page_obj(list_tugas, page_number, per_page=5)
    
    csrf_token = get_token(request)

    context = {
        "list_tugas": list_tugas,
        "matakuliah": matakuliah,
        "page_obj": page_obj,
        "headers": headers,
        "csrf_token": csrf_token,
        "url_pencarian": reverse("daftar_tugas", kwargs={"id_matakuliah": id_matakuliah}),
    }
    return render(request, "pages/daftar_tugas.html", context)


def tugas_detail(request, id):
    csrf_token = get_token(request)
    tugas = TugasRepository().get_by_id(id)

    if request.method == "POST":
        # salin data POST agar bisa dimodifikasi
        form_data = request.POST.copy()

        # tambah atau ubah nilai
        form_data["tugas"] = id

        form = KirimTugasForm(form_data)
        if form.is_valid():
            # ambil data
            nim = form.cleaned_data["nim"]
            link_tugas = form.cleaned_data["link_tugas"]
            id_tugas = form.cleaned_data["tugas"]

            try:
                kirim_tugas_service(
                    nim=nim,
                    link_tugas=link_tugas,
                    id_matakuliah=tugas.matakuliah.id,
                    id_tugas=id_tugas,
                )
                messages.success(request, "Tugas berhasil dikirim")
                return redirect("tugas_detail", id=id)
            except Exception as e:
                messages.error(request, str(e))

    context = {"tugas": tugas, "crsf_token": csrf_token, "timezone": timezone}
    return render(request, "pages/tugas_detail.html", context)
