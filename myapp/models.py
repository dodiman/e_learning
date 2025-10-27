from django.db import models

from django.db import models
from django.utils import timezone

class Mahasiswa(models.Model):
    nim = models.CharField(max_length=15, unique=True)
    nama = models.CharField(max_length=100)
    jurusan = models.CharField(max_length=100)
    angkatan = models.IntegerField()
    email = models.EmailField(blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    tempat_lahir = models.CharField(max_length=100, blank=True, null=True)
    tanggal_lahir = models.DateField(blank=True, null=True)
    no_wa = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.nim} - {self.nama}"
    
    
class Matakuliah(models.Model):
    nama = models.CharField(max_length=100)
    kode = models.CharField(max_length=10, unique=True, null=True, blank=True)
    deskripsi = models.TextField()
    
    def __str__(self):
        return self.nama
    
class Tugas(models.Model):
    judul = models.CharField(max_length=100)
    deskripsi = models.TextField()
    deadline = models.DateField()
    matakuliah = models.ForeignKey(Matakuliah, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.judul
    
# class Submission(models.Model):
#     mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE)
#     tugas = models.ForeignKey(Tugas, on_delete=models.CASCADE)
#     file = models.FileField(upload_to='submissions/')
#     tanggal_pengumpulan = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.mahasiswa} - {self.tugas}"
    

class Submission(models.Model):
    mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE)
    tugas = models.ForeignKey(Tugas, on_delete=models.CASCADE)
    link_tugas = models.URLField(blank=True, null=True)
    tanggal_pengumpulan = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.mahasiswa} - {self.tugas}"


class Grade(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    feedback = models.TextField()
    
    def __str__(self):
        return f"{self.tugas} - {self.mahasiswa}"
