from django.contrib import admin
from .models import CustomUser, Employee , Timecalc

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Employee)
admin.site.register(Timecalc)