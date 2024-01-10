from django.contrib import admin
from .models import Room,Topic,message,User
# Register your models here.


admin.site.register(User)
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(message)