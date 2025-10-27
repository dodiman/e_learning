# from myapp.models import Tugas
from django.shortcuts import get_object_or_404

class BaseRepository:
    def __init__(self, model):
        self.model = model
        
    def get_all(self):
        return self.model.objects.all()
    
    def get_by_id(self, id):
        return get_object_or_404(self.model, id=id)
    
    def create(self, data: dict):
        return self.model.objects.create(**data)
    
    def update(self, id, data: dict):
        model = get_object_or_404(self.model, id=id)
        for key, value in data.items():
            setattr(model, key, value)
        model.save()
        return model
    
    @staticmethod
    def delete(self, id) -> bool:
        model = get_object_or_404(self.model, id=id)
        model.delete()
        return True