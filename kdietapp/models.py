from django.db import models

# Create your models here.
# class user(models.Model):
#     username = models.CharField(max_length=50)
#     password = models.CharField(max_length=50)
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     phone_number = models.IntegerField(max_length=11)
#     birth_date = models.DateField()
#     gender = models.CharField(max_length=20)
#     street_address = models.CharField(max_length=150)
#     city = models.CharField(max_length=50)
#     state = models.CharField(max_length=50)
#     zipcode = models.IntegerField()
#     weight_lbs = models.FloatField()
#     height_inches = models.FloatField()

#     class Meta:
#         db_table = 'user'

# class serum_levels(models.Model):
#     results_date = models.DateField()
#     potassium_level = models.FloatField()
#     phosphorus_level = models.FloatField()
#     sodium_level = models.FloatField()
#     creatinine_level = models.FloatField()
#     albumin_level = models.FloatField()
#     blood_sugar_level = models.FloatField()

#     class Meta:
#         db_table = 'serum_levels'

# class food_diary(models.Model) :
#     date = models.DateField()

#     class Meta:
#         db_table = 'food_diary'

# class food_diary_entry(models.Model) :
#     meal_type = models.CharField(max_length=25)

#     class Meta:
#         db_table = 'food_diary_entry'

# class food(models.Model) :
#     fdcId = models.CharField(max_length=25)
#     name = models.CharField(max_length=50)
#     amount = models.CharField(max_length=50)
#     measurement = models.CharField(max_length=50)

# class micronutrient_info(models.Model) :
#     mg_sodium = models.FloatField()
#     g_protein = models.FloatField()
#     l_water = models.FloatField()
#     mg_potassium = models.FloatField()
#     mg_phosphorus = models.FloatField()
#     calories = models.FloatField()
