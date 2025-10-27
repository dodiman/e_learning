from myapp.models import Tugas
from django.shortcuts import get_object_or_404
from .base_repository import BaseRepository

class TugasRepository(BaseRepository):
    def __init__(self):
        super().__init__(Tugas)
        
    def get_by_matakuliah(self, id_matakuliah):
        return Tugas.objects.filter(matakuliah=id_matakuliah)

# class TugasRepository:
#     @staticmethod
#     def get_all() -> Tugas:
#         return Tugas.objects.all()
    
#     @staticmethod
#     def get_by_id(id) -> Tugas:
#         return get_object_or_404(Tugas, id=id)
    
#     @staticmethod
#     def create(data: dict) -> Tugas:
#         return Tugas.objects.create(**data)
    
#     @staticmethod
#     def update(tugas_id, data: dict) -> Tugas:
#         tugas = get_object_or_404(Tugas, id=tugas_id)
#         for key, value in data.items():
#             setattr(tugas, key, value)
#         tugas.save()
#         return tugas
    
#     @staticmethod
#     def delete(tugas_id) -> bool:
#         tugas = get_object_or_404(Tugas, id=tugas_id)
#         tugas.delete()
#         return True