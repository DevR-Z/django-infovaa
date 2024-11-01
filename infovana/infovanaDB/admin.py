from django.contrib import admin
from .models import TituloxUser,Titulo,Movie,Serie,Episode

# Register your models here.
admin.site.register(TituloxUser)
admin.site.register(Titulo)
admin.site.register(Movie)
admin.site.register(Serie)
admin.site.register(Episode)