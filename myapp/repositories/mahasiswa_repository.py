from myapp.models import Mahasiswa
from django.shortcuts import get_object_or_404
from .base_repository import BaseRepository

class MahasiswaRepository(BaseRepository):
    def __init__(self):
        super().__init__(Mahasiswa)
        
    def get_by_nim(self, nim) -> Mahasiswa:
        return get_object_or_404(self.model, nim=nim)

# class MahasiswaRepository:
#     @staticmethod
#     def get_by_nim(nim) -> Mahasiswa:
#         return get_object_or_404(Mahasiswa, nim=nim)
    
#     @staticmethod
#     def get_by_id(id) -> Mahasiswa:
#         return get_object_or_404(Mahasiswa, id=id)
    
#     @staticmethod
#     def get_all() -> Mahasiswa:
#         return Mahasiswa.objects.all()
    
#     @staticmethod
#     def create(data: dict) -> Mahasiswa:
#         return Mahasiswa.objects.create(**data)
    
#     @staticmethod
#     def update(mahasiswa_id, data: dict) -> Mahasiswa:
#         mahasiswa = get_object_or_404(Mahasiswa, id=mahasiswa_id)
#         for key, value in data.items():
#             setattr(mahasiswa, key, value)
#         mahasiswa.save()
#         return mahasiswa
    
#     @staticmethod
#     def delete(mahasiswa_id) -> bool:
#         mahasiswa = get_object_or_404(Mahasiswa, id=mahasiswa_id)
#         mahasiswa.delete()
#         return True