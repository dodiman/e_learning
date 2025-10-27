import os
import django
import sys

sys.path.append(os.path.abspath(".."))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_orm_lab.settings")

django.setup()

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"


from myapp.models import Mahasiswa
print(Mahasiswa.objects.all())