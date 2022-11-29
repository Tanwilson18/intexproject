from django.contrib import admin
from .models import user, comorbidity, user_comorbidity, serum_levels, food_diary
# Register your models here.
admin.site.register(user)
admin.site.register(comorbidity)
admin.site.register(user_comorbidity)
admin.site.register(serum_levels)
admin.site.register(food_diary)
