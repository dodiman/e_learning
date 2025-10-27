from .repositories.matakuliah_repository import MatakuliahRepository
from .repositories.tugas_repository import TugasRepository
from .repositories.submission_repository import SubmissionRepository
from .repositories.mahasiswa_repository import  MahasiswaRepository
from myapp.models import *

from django.forms.models import model_to_dict
import pandas as pd

from typing import List, Dict, Any
from django.db.models import Q, QuerySet

from datetime import date
from django.utils import timezone

# paginasi
from django.core.paginator import Paginator

class TugasService:
    pass

class TugasService:
    pass

def kirim_tugas_service(nim, link_tugas, id_matakuliah, id_tugas):
    matakuliah = MatakuliahRepository().get_by_id(id_matakuliah)
    tugas = TugasRepository().get_by_id(id_tugas)
    mahasiswa = MahasiswaRepository().get_by_nim(nim)
    
    if not tugas:
        raise ValueError("tugas tidak ditemukan")
    
    # validasi tanggal kirim
    waktu_sekarang = timezone.now().date()
    if tugas.deadline < waktu_sekarang:
        raise ValueError("tanggal pengumpulan sudah lewat")
    
    # validasi apakah sudah pernah kirim tugas
    if SubmissionRepository().filter_by_mahasiswa_and_tugas(mahasiswa, tugas).exists():
        # get
        submission = SubmissionRepository().get_by_mahasiswa_and_tugas(mahasiswa, tugas)
        # update
        return SubmissionRepository().update(submission.id, {"link_tugas": link_tugas})
    
    submission = SubmissionRepository()
    data = {
        "mahasiswa": mahasiswa,
        "tugas": tugas,
        "link_tugas": link_tugas,
    }
    return submission.create(data)

def get_by_matakuliah_service(id_matakuliah) -> List[Dict[str, Any]]:
    tugas_qs = TugasRepository().get_by_matakuliah(id_matakuliah)
    if tugas_qs.count() == 0:
        return tugas_qs
    tugas_df = pd.DataFrame(tugas_qs.values())
    tugas_df["deadline"] = pd.to_datetime(tugas_df["deadline"], errors="coerce")
    tugas_df["sudah_lewat"] = tugas_df["deadline"].dt.date < date.today()
    tugas_df["deadline"] = tugas_df["deadline"].dt.strftime("%d-%m-%Y")
    tugas_df = tugas_df.sort_values(by="deadline", ascending=False)
    
    return tugas_df.to_dict(orient="records")

def get_paginated_tugas_service(page, id_matakuliah) -> List[Dict[str, Any]]:
    tugas_qs = TugasRepository().get_by_matakuliah(id_matakuliah)
    paginator = Paginator(tugas_qs, 5)
    tugas_df = pd.DataFrame(paginator.page(page).object_list.values())
    tugas_df["deadline"] = pd.to_datetime(tugas_df["deadline"], errors="coerce")
    tugas_df["sudah_lewat"] = tugas_df["deadline"].dt.date < date.today()
    tugas_df["deadline"] = tugas_df["deadline"].dt.strftime("%d-%m-%Y")
    tugas_df = tugas_df.sort_values(by="deadline", ascending=False)
    
    return tugas_df.to_dict(orient="records")


def tabel_dengan_navigasi_service(qs: QuerySet, page_number, per_page=5):
    paginator = Paginator(qs, per_page)
    
    # ambil parameter ?page= dari url
    # page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    return page_obj

def get_page_obj(qs: QuerySet, page_number, per_page=5):
    paginator = Paginator(qs, per_page)
    return paginator.get_page(page_number)
    
    
def get_headers_querset(qs: QuerySet | List, exclude: List[str] = []) -> List[str]:
    hasil = []
    if isinstance(qs, QuerySet):
        hasil = [field.name for field in qs.model._meta.get_fields()]
    
    # jika qs adalah list dict
    elif isinstance(qs, list):
        hasil = list(qs[0].keys())
        
    else:
        raise ValueError("qs harus QuerySet atau list dict")
        
    # exclude list
    if exclude:
        for field in exclude:
            if field in hasil:
                hasil.remove(field)
    
    return hasil