from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Company, Department, Section, Position

User = get_user_model()


admin.site.register(User)
admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Section)
admin.site.register(Position)
