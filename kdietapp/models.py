from django.db import models
from datetime import datetime, date


class kdiet_user(models.Model):
    username = models.CharField(max_length=50, primary_key=True, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=14)
    birth_date = models.DateField()
    sex = models.CharField(max_length=10)
    email = models.EmailField()
    weight_lbs = models.FloatField()
    height_inches = models.FloatField()

    # only returns username to the admin, may need to add more self.attributes
    def __str__(self):
        return (self.username)

    class Meta:
        db_table = 'kdiet_user'


class comorbidity(models.Model):
    comorbidity_id = models.AutoField(primary_key=True, null=False)
    comorbidity_name = models.CharField(max_length=25, null=False)

    class Meta:
        db_table = 'comorbidity'

    def __str__(self):
        return (self.comorbidity_id)


class user_comorbidity(models.Model):
    username = models.ForeignKey(kdiet_user, on_delete=models.DO_NOTHING)
    comorbidity_id = models.ForeignKey(
        comorbidity, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = 'user_comorbidity'
        # got this from slack message
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'comorbidity_id'], name='user_comorbidity_CPK')
        ]

    def __str__(self):
        return (self.username, self.comorbidity_id)


class food_diary(models.Model):
    date = models.DateField(default=date.today)
    username = models.ForeignKey(kdiet_user, on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['date', 'username'], name="food_diary_CPK")]
        db_table = 'food_diary'

    def __str__(self):
        return (self.date, self.username)


class food(models.Model):
    fdc_id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=80)
    mg_sodium = models.FloatField()
    g_protein = models.FloatField()
    l_water = models.FloatField()
    mg_potassium = models.FloatField()
    mg_phosphorus = models.FloatField()

    class Meta:
        db_table = 'food'

    def __str__(self):
        return (self.fdc_id, self.name, self.mg_sodium, self.g_protein, self.l_water, self.mg_potassium, self.mg_phosphorus)


class food_diary_entry(models.Model):
    date = models.ForeignKey(food_diary, on_delete=models.DO_NOTHING)
    # couldn't figure out how to make the date a foreign key without errors
    username = models.ForeignKey(kdiet_user, on_delete=models.DO_NOTHING)
    fdc_id = models.ForeignKey(food, on_delete=models.DO_NOTHING)
    meal_type = models.CharField(max_length=10)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['date', 'username', 'fdc_id', 'meal_type'], name="food_diary_entry_CPK")]
        db_table = 'food_diary_entry'

    def __str__(self):
        # trying to return all values
        return (self.date, self.username, self.fdc_id, self.meal_type)


# class micronutrient_info(models.Model):
#     mg_sodium = models.FloatField()
#     g_protein = models.FloatField()
#     l_water = models.FloatField()
#     mg_potassium = models.FloatField()
#     mg_phosphorus = models.FloatField()
#     fdc_id = models.ForeignKey(food, on_delete=models.DO_NOTHING)

#     class Meta:
#         db_table = 'micronutrient_info'

#     def __str__(self):
#         return (self.mg_sodium, self.g_protein, self.l_water, self.mg_potassium, self.mg_phosphorus, self.fcd_id)


class serum_levels(models.Model):
    results_date = models.DateField()
    potassium_level = models.FloatField()
    phosphorus_level = models.FloatField()
    sodium_level = models.FloatField()
    creatinine_level = models.FloatField()
    albumin_level = models.FloatField()
    blood_sugar_level = models.FloatField()
    username = models.ForeignKey(kdiet_user, on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['username', 'results_date'], name="serum_levels_CPK")]
        db_table = 'serum_levels'

    def __str__(self):
        # returning the name of the constraint
        return (self.results_date)
