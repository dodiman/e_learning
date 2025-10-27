import os
import django
import sys

sys.path.append(os.path.abspath(".."))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_orm_lab.settings")

django.setup()

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import streamlit as st

from myapp.models import Mahasiswa

# -----------------------------------------------
# 4. Streamlit UI
# -----------------------------------------------
st.title("🎓 Simulasi Database Mahasiswa (Django ORM + Streamlit)")

menu = st.sidebar.radio("Menu", ["Tambah Data", "Lihat Data"])


if menu == "Tambah Data":
    st.subheader("Tambah Mahasiswa Baru")

    nim = st.text_input("NIM")
    nama = st.text_input("Nama")
    jurusan = st.text_input("Jurusan")
    angkatan = st.number_input("Angkatan", min_value=2000, max_value=2100, step=1)
    email = st.text_input("Email")

    if st.button("Simpan"):
        if nim and nama:
            Mahasiswa.objects.create(
                nim=nim,
                nama=nama,
                jurusan=jurusan,
                angkatan=angkatan,
                email=email
            )
            st.success(f"✅ Data mahasiswa {nama} berhasil disimpan!")
        else:
            st.warning("⚠️ NIM dan Nama wajib diisi!")

elif menu == "Lihat Data":
    st.subheader("Daftar Mahasiswa")
    data = Mahasiswa.objects.all()

    if data:
        rows = [
            [m.nim, m.nama, m.jurusan, m.angkatan, m.email]
            for m in data
        ]
        st.table(rows)
    else:
        st.info("Belum ada data mahasiswa.")
