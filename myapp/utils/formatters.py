from django.utils import formats

def format_tanggal(value):
    if not value:
        return ""
    return formats.date_format(value, "d M Y")