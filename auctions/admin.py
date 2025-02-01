from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(Notification)