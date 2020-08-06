from django.contrib import admin
from .models import Users,ConfirmString,BlogPost

admin.site.register(Users)
admin.site.register(ConfirmString)
admin.site.register(BlogPost)
# Register your models here.
