from django.contrib import admin

from .models import (
	Product,
	Rating,
	Sale,
	)
# Register your models here.


admin.site.register([Product,Rating,Sale])