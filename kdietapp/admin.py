from django.contrib import admin
from .models import kdiet_user, comorbidity, user_comorbidity, serum_levels, food_diary
from .models import food, food_diary_entry
# admin view created users
# from .forms import NewUserForm
# Register your models here.
admin.site.register(kdiet_user)
admin.site.register(comorbidity)
admin.site.register(user_comorbidity)
admin.site.register(food_diary)
admin.site.register(food)
admin.site.register(food_diary_entry)
admin.site.register(serum_levels)
