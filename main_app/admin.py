from django.contrib import admin
from .models import Profile, Posting, Contact, Photo

# Register your models here.
admin.site.register(Profile)
admin.site.register(Posting)
admin.site.register(Contact)
admin.site.register(Photo)