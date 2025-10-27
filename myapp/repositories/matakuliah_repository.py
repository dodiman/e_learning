from myapp.models import Matakuliah
from django.shortcuts import get_object_or_404
from .base_repository import BaseRepository

class MatakuliahRepository(BaseRepository):
    def __init__(self):
        super().__init__(Matakuliah)
