from django.contrib import admin
from .models import User, Device

# Register your models here.
#admin.site.register(User)
admin.site.register(Device)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'email')
