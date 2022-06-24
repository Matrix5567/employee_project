from django.contrib import admin
from .models import CustomUser, Employee , Timecalc ,Leave

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Employee)
admin.site.register(Timecalc)
admin.site.register(Leave)