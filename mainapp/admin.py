from django.contrib import admin
from .models import *


admin.site.register([CustomUser,NewsCategory,Staff,Contact,NewsComment])
