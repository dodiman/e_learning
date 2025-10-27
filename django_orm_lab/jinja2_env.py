# projectname/jinja2_env.py
from jinja2 import Environment
from django.templatetags.static import static
from django.urls import reverse, reverse_lazy
from django.contrib.messages import get_messages

def environment(**options):
    env = Environment(**options)
    
    # Tambahkan fungsi Django ke global scope Jinja2
    env.globals.update({
        "static": static,   # agar bisa pakai {{ static('path') }}
        "url": reverse,     # agar bisa pakai {{ url('route_name') }}
    })
    env.globals['get_messages'] = get_messages
    return env
