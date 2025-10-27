import os
import django
import sys

from django.forms.models import model_to_dict
import pandas as pd

sys.path.append(os.path.abspath(".."))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_orm_lab.settings")

django.setup()

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import streamlit as st

from myapp.models import Mahasiswa, Submission, Tugas

# simpan di google drive
from django.core.files.storage import FileSystemStorage
from myapp.utils.google_drive import upload_to_drive

# fungsi


def validasi_nim(nim):
    mahasiswa = Mahasiswa.objects.filter(nim=nim).first()
    if mahasiswa:
        return True
    else:
        return False


# -----------------------------------------------
# UI Kirim Tugas
# -----------------------------------------------
st.title("Kirim Tugas")

st.header("contoh kirim tugas")

# if "mhs" in st.session_state:
#     st.session_state.mhs = None

# wizard form
if "step" not in st.session_state:
    st.session_state.step = 1

# langkah 1
if st.session_state.step == 1:
    st.subheader("Langkah 1: Validasi NIM")

    with st.form("validasi_nim"):
        nim = st.text_input("NIM")
        # judul = st.text_input("Judul Tugas")
        # deskripsi = st.text_area("Deskripsi Tugas")
        # # deadline = st.date_input("Deadline")
        # tugas = Tugas.objects.create(judul=judul, deskripsi=deskripsi, deadline=deadline)
        # mahasiswa = Mahasiswa.objects.get(nim=nim)

        submit = st.form_submit_button("Validasi")

        if submit:
            if validasi_nim(nim):
                mahasiswa = Mahasiswa.objects.get(nim=nim)
                st.write("NIM tersedia")
                st.write(pd.Series(model_to_dict(mahasiswa)))
                st.session_state.mhs = mahasiswa
                st.session_state.step = 2
            else:
                st.write("NIM tidak tersedia")

# langkah 2
elif st.session_state.step == 2:
    st.subheader("Langkah 2: Kirim Tugas")
    st.write(pd.Series(model_to_dict(st.session_state.mhs)))
    # st.write(st.session_state.mhs)

    with st.form("kirim_tugas"):
        list_tugas = pd.DataFrame(Tugas.objects.all().values()).id.to_numpy()
        # st.write(list_tugas)
        pil_tugas = st.selectbox("Pilih Tugas", list_tugas)
        file = st.file_uploader("File Jawaban", type=["pdf"])
        link_tugas = st.text_input("Link Tugas")
        # judul = st.text_input("Judul Tugas")
        # deskripsi = st.text_area("Deskripsi Tugas")
        # deadline = st.date_input("Deadline")
        # tugas = Tugas.objects.create(judul=judul, deskripsi=deskripsi, deadline=deadline)
        # mahasiswa = Mahasiswa.objects.get(nim=nim)

        btn_kembali = st.form_submit_button("Kembali")
        if btn_kembali:
            st.session_state.step = 1

        submit = st.form_submit_button("Kirim")

        if submit:
            context = {
                "mahasiswa_id": st.session_state.mhs.id,
                "tugas_id": pil_tugas,
                "file": file,
                "link_tugas": link_tugas
            }
            
            # simpan sementara di server
            # fs = FileSystemStorage()
            # file_path = fs.save(file.name, file)
            # full_path = fs.path(file_path)
            
            # upload ke goole drive
            # FOLDER_ID = "10w7eT-fCRUB87ivUwrsUr1gDZklmFlWS"
            FOLDER_ID = "1eEZfmwwb_bRF9h39Mq_KRq6GRHlB-ENJ"
            # file_id, view_link = upload_to_drive(full_path, file.name, FOLDER_ID)
            
            
            # simpan metadata ke database
            submission = Submission(
                mahasiswa_id=context["mahasiswa_id"], tugas_id=context["tugas_id"]
            )
            # submission.file.name = file.name
            submission.link_tugas = link_tugas
            # submission.drive_file_id = file_id
            # submission.file.save(file.name, file) # simpan file ke storage (MEDIA_ROOT)
            submission.save()  # simpan file ke database
            

            # st.write(context)
            # Submission.objects.create(**context)

            st.write("Tugas berhasil dikirim")
