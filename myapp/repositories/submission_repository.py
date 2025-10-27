from myapp.models import Submission
from django.shortcuts import get_object_or_404
from .base_repository import BaseRepository

class SubmissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Submission)
        
    def get_by_mahasiswa_and_tugas(self, mahasiswa, tugas):
        return self.model.objects.filter(mahasiswa=mahasiswa, tugas=tugas).first()
        
    def filter_by_mahasiswa_and_tugas(self, mahasiswa, tugas):
        return self.model.objects.filter(mahasiswa=mahasiswa, tugas=tugas)
    
    def update_or_create(self, data: dict):
        return self.model.objects.update_or_create(**data)


# class SubmissionRepository:
#     @staticmethod
#     def get_all() -> Submission:
#         return Submission.objects.all()
    
#     @staticmethod
#     def get_by_id(id) -> Submission:
#         return get_object_or_404(Submission, id=id)
    
#     @staticmethod
#     def create(data: dict) -> Submission:
#         return Submission.objects.create(**data)
    
#     @staticmethod
#     def update(submission_id, data: dict) -> Submission:
#         submission = get_object_or_404(Submission, id=submission_id)
#         for key, value in data.items():
#             setattr(submission, key, value)
#         submission.save()
#         return submission
    
#     @staticmethod
#     def delete(submission_id) -> bool:
#         submission = get_object_or_404(Submission, id=submission_id)
#         submission.delete()
#         return True