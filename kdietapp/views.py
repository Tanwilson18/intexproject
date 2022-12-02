from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this
from .models import serum_levels
import pip._vendor.requests as requests
from .models import kdiet_user, food, food_diary, food_diary_entry
from datetime import datetime
import json

# Create your views here.


def indexPageView(request):
    return render(request, 'index.html')


def serumLevelPageView(request):
    # request the current users information and assign it to variable
    variable = request.user

    data = serum_levels.objects.filter(username=variable.username)
    context = {
        'data': data,
    }
    if request.method == 'POST':

        variable = request.user
        varibale2 = kdiet_user.objects.get(username=variable.username)

        user_serum = serum_levels()

        user_serum.username = varibale2
        user_serum.results_date = request.POST['results_date']
        user_serum.potassium_level = request.POST['potassium_level']
        user_serum.phosphorus_level = request.POST['phosphorus_level']
        user_serum.sodium_level = request.POST['sodium_level']
        user_serum.creatinine_level = request.POST['creatinine_level']
        user_serum.albumin_level = request.POST['albumin_level']
        user_serum.blood_sugar_level = request.POST['blood_sugar_level']

        user_serum.save()

    return render(request, 'subpages/serum_levels.html', context)


def trackerPageView(request):
    # query from food_diary entry to grab the user and entry_id

    user = request.user
    person = kdiet_user.objects.get(username=request.user.username)
    if person.sex == 'male':
        rwater = 3700
    else:
        rwater = 2700
    if food_diary.objects.filter(
            username=user.username, date=datetime.today()).exists():
        dates = food_diary.objects.get(
            username=user.username, date=datetime.today())
        data1 = food_diary_entry.objects.filter(
            date=dates)

        sodium = 0
        protein = 0
        potassium = 0
        phosphorus = 0
        water = 0

        for data in data1:
            # .get(entry_id=data1.entry_id)
            food1 = food.objects.get(entry_id=data.entry_id.entry_id)
            sodium += food1.mg_sodium
            protein += food1.g_protein * 1000
            potassium += food1.mg_potassium
            phosphorus += food1.mg_phosphorus
            water += food1.l_water

        recommended = [2300, 600, 3000, 1000, rwater]

        alert1 = ''
        alert2 = ''
        alert3 = ''
        alert4 = ''
        alert5 = ''
        if sodium > recommended[0]:
            alert1 = "You've eaten too much sodium! "
        if protein > recommended[1]:
            alert2 = "You've eaten too much protein! "
        if potassium > recommended[2]:
            alert3 = "You've drank too much potassium! "
        if phosphorus > recommended[3]:
            alert4 = "You've eaten too much phosphorus! "
        if water > recommended[4]:
            alert5 = "You've drank too much water! "
            ### do something###
    else:
        ### do otherthing###
        sodium = 0
        protein = 0
        potassium = 0
        phosphorus = 0
        water = 0
        alert1 = ''
        alert2 = ''
        alert3 = ''
        alert4 = ''
        alert5 = ''

    nutrient_list = ["Potassium, K", "Water",
                     "Protein", "Sodium, Na", "Phosphorus, P"]
    # foodType = None
    # foodType = request.POST.get("foodGroups")
    if request.method == "POST":
        search = request.POST["SearchFood"]
        parameters = {
            'api_key': '9aSh1S0uTOlVQKP7ZDzmnjgGWYDfOmzK5RnZxcxQ',
            'query': search,
            # 'dataType': 'Foundation'  # foodType if we decide to do that
        }

        response = requests.get(
            "https://api.nal.usda.gov/fdc/v1/foods/search", params=parameters)

        data = response.json()
        food_dict = {}
        if len(data['foods']) == 0:
            context = {
                'totals': [sodium, protein, water, potassium, phosphorus],
                'rwater': rwater,
                'alert1': alert1,
                'alert2': alert2,
                'alert3': alert3,
                'alert4': alert4,
                'alert5': alert5,
            }
            return render(request, 'subpages/tracker.html', context)
        for i in range(10):
            # for i in range(len(data["foods"])):
            if len(data['foods']) < 10 and i >= len(data['foods']):
                break
            food_name = data["foods"][i]["description"]
            food_dict[food_name] = {}

            for j in range(len(data["foods"][i]["foodNutrients"])):
                nutrient_name = data["foods"][i]["foodNutrients"][j]['nutrientName']

                if nutrient_name in nutrient_list:

                    if 'value' in data['foods'][i]['foodNutrients'][j].keys():
                        value = data['foods'][i]['foodNutrients'][j]['value']
                        # unit = data['foods'][i]['foodNutrients'][j]['unitName']
                    else:
                        value = 0
                        # unit = 0
                    food_dict[food_name][nutrient_name] = [value]  # , unit]

        nutrients = []
        nutrientValues = {}
        for i in food_dict:
            for key in food_dict[i]:
                # if key == "Water":
                #    food_dict[i][key][1] = 'mL'
                nutrientValue = food_dict[i][key]  # [0]
                # nutrientMeasure = food_dict[i][key][1]
                nutrients.append(key)
                nutrientValues = {key: nutrientValue}
                # nutrientMeasures = {key: nutrientMeasure}
        context = {
            'foods': food_dict,
            'nutrients': nutrients,
            'nutrientValues': nutrientValues,
            # 'nutrientMeasure': nutrientMeasures,
            'list': nutrients,
            'totals': [sodium, protein, potassium, phosphorus, water],
            'rwater': rwater,
            'alert1': alert1,
            'alert2': alert2,
            'alert3': alert3,
            'alert4': alert4,
            'alert5': alert5,
        }
        return render(request, 'subpages/tracker.html', context)
    else:
        context = {
            'totals': [sodium, protein, potassium, phosphorus, water],
            'rwater': rwater,
            'alert1': alert1,
            'alert2': alert2,
            'alert3': alert3,
            'alert4': alert4,
            'alert5': alert5,
        }
        return render(request, 'subpages/tracker.html', context)

# follow this link to learn about django messages
# https://ordinarycoders.com/blog/article/django-messages-framework
# "it'll be fun" they said


def addFoodPageView(request):
    if request.method == 'POST':
        # create object food, assign attributes from post method
        foodItem = food()
        foodItem.name = request.POST.get('foodName')
        foodItem.mg_sodium = request.POST.get('sodium', 0)
        foodItem.g_protein = request.POST.get('protein', 0)
        foodItem.l_water = request.POST.get('water', 0)
        foodItem.mg_potassium = request.POST.get('potassium', 0)
        foodItem.mg_phosphorus = request.POST.get('phosphorus', 0)
        foodItem.save()

        z_user = request.user
        username = z_user.username

        # username = kdiet_user.objects.get(username=uname)
        date = request.POST.get('date')
        if not food_diary.objects.filter(date=date, username=username).exists():

            variable = request.user
            varibale2 = kdiet_user.objects.get(username=variable.username)

            foodDiary = food_diary()
            foodDiary.date = date
            foodDiary.username = varibale2
            foodDiary.save(force_insert=True)
        else:
            foodDiary = food_diary.objects.get(date=date, username=username)

        foodEntry = food_diary_entry()

        foodEntry.date = foodDiary
        foodEntry.username = foodDiary.username
        foodEntry.entry_id = foodItem
        foodEntry.meal_type = request.POST.get('meal_type')
        foodEntry.save(force_insert=True)
        return render(request, 'index.html')

    nutrients = ""
    nutrients_dict = {}
    foodName = request.GET.get("foodName")
    nutrients = request.GET.get(foodName+"-nutrients")
    # mealType = request.POST.get('mealtype')

    if nutrients is None:
        pass
    else:
        nutrients = nutrients.replace('\'', '\"')
        nutrients_dict = json.loads(nutrients)
        if 'Water' in nutrients_dict:
            water = nutrients_dict['Water'][0]
        else:
            water = 0
        if 'Potassium, K' in nutrients_dict:
            potassium = nutrients_dict['Potassium, K'][0]
        else:
            potassium = 0
        if 'Protein' in nutrients_dict:
            protein = nutrients_dict['Protein'][0]
        else:
            protein = 0
        if 'Sodium, Na' in nutrients_dict:
            sodium = nutrients_dict['Sodium, Na'][0]
        else:
            sodium = 0
        if 'Phosphorus, P' in nutrients_dict:
            phosphorus = nutrients_dict['Phosphorus, P'][0]
        else:
            phosphorus = 0

        test = json.dumps(nutrients_dict, indent=4)

        # create entry in food table

    context = {
        'foodName': foodName,
        # 'nutrients': nutrients_dict,
        # 'mealType': mealType,
        'water': water,
        'potassium': potassium,
        'protein': protein,
        'sodium': sodium,
        'phosphorus': phosphorus,
        'requestType': request.method
    }

    return render(request, 'subpages/addFood.html', context)


def showFoodPageView(request):
    variable = request.user
    entries_data = food_diary_entry.objects.filter(username=variable.username)

    context = {
        "foodEntries": entries_data
    }
    return render(request, 'subpages/showFood.html', context)


def editFoodPageView(request):
    if request.method == "POST":
        k_user = request.user
        finduser = kdiet_user.objects.filter(
            username=k_user.username)
        z_user = kdiet_user(username=finduser)

        # variable = food_diary_entry.objects.filter(username=k_user.username)
        if request.POST.get('meal_type') != None:
            pass
        else:
            food_id = request.POST.get("entry_id")
            foodInstance = food.objects.get(entry_id=food_id)
            foodEntry = food_diary_entry.objects.get(entry_id=foodInstance)
            foodEntry.entry_id = foodInstance
            foodUser = foodEntry.username
            context = {
                "username": foodUser,
                "entry_id": foodInstance
            }
            return render(request, 'subpages/editFood.html', context)

        # foodEntry.meal_type = request.POST.get("meal_type")
        if request.POST.get('meal_type') == None:
            pass
        else:
            # foodEntry.username = variable
            food_id = request.POST.get("entry_id")
            foodInstance = food.objects.get(entry_id=food_id)
            foodEntry = food_diary_entry.objects.get(entry_id=foodInstance)
            foodEntry.entry_id = foodInstance
            foodUser = foodEntry.username
            meal_type = request.POST.get('meal_type')

            # set values
            foodEntry.meal_type = meal_type

            date = request.POST.get('date')
            if not food_diary.objects.filter(date=date, username=z_user).exists():

                variable = request.user
                varibale2 = kdiet_user.objects.get(username=variable.username)

                foodDiary = food_diary()
                foodDiary.date = date
                foodDiary.username = varibale2
                foodDiary.save(force_insert=True)
            else:
                foodDiary = food_diary.objects.get(date=date, username=z_user)
            foodEntry.date = foodDiary

            foodEntry.save()

            return render(request, 'subpages/tracker.html')
    else:
        return render(request, 'subpages/editFood.html')


def addProfilePageView(request):
    if request.method == 'POST':

        k_user = kdiet_user()

        k_user.username = request.POST['username']
        k_user.first_name = request.POST['first_name']
        k_user.last_name = request.POST['username']
        k_user.email = request.POST['email']
        k_user.phone_number = request.POST['phone_number']
        k_user.birth_date = request.POST['birth_date']
        k_user.sex = request.POST['sex']
        k_user.weight_lbs = request.POST['weight_lbs']
        k_user.height_inches = request.POST['height_inches']

        k_user.save()

        return indexPageView(request)
    else:
        return render(request, 'subpages/addProfile.html')


def editProfilePageView(request):
    if request.method == 'POST':
        k_user = request.user

        sfirst_name = request.POST['first_name']
        slast_name = request.POST['last_name']
        newEmail = request.POST['email']
        newPhoneNumber = request.POST['phone_number']
        newBirthDate = request.POST['birth_date']
        newSex = request.POST['sex']
        newWeight = request.POST['weight_lbs']
        newHeight = request.POST['height_inches']

        k_user.first_name = sfirst_name
        k_user.last_name = slast_name
        k_user.email = newEmail
        k_user.phone_number = newPhoneNumber
        k_user.birth_date = newBirthDate
        k_user.sex = newSex
        k_user.weight_lbs = newWeight
        k_user.height_inches = newHeight

        k_user.save()

        return indexPageView(request)
    else:
        return render(request, 'subpages/editProfile.html')


def deleteFoodPageView(request):
    food_id = request.POST.get("entry_id")
    foodInstance = food.objects.get(entry_id=food_id)
    foodEntry = food_diary_entry.objects.get(entry_id=foodInstance)
    foodEntry.entry_id = foodInstance

    foodEntry.delete()
    return showFoodPageView(request)


def suggestionsPageView(request):
    return render(request, 'subpages/suggestions.html')


def bloghomePageView(request):
    return render(request, 'subpages/blog-home.html')


def blogpostPageView(request):
    return render(request, 'subpages/blog-post.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("addProfile")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'register.html', context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                # once logged in automatically redirects
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'login.html', context={"login_form": form})


def logout_request(request):
    messages.info(request, "You have successfully logged out.")
    logout(request)
    return render(request, 'logout.html')


def profile(request):
    return render(request, 'profile.html')

    # username = k_user.username
    # entry = food.objects.get(entry_id=entry2)

    # foodEntry = food_diary_entry()

    # entry2 = request.POST['entry_id']
    # foodEntry.meal_type = request.POST.get('meal_type')
    # foodEntry.date = request.POST.get('date')

    # entry = food.objects.get(entry_id=entry)
    # foodEntry = food_diary_entry()

    # foodEntry.entry_id = entry


def importNutrientsPageView(request):
    if request.method == 'POST':
        # create object food, assign attributes from post method
        foodItem = food()
        foodItem.name = request.POST.get('name')
        foodItem.mg_sodium = request.POST.get('sodium', 0)
        foodItem.g_protein = request.POST.get('protein', 0)
        foodItem.l_water = request.POST.get('water', 0)
        foodItem.mg_potassium = request.POST.get('potassium', 0)
        foodItem.mg_phosphorus = request.POST.get('phosphorus', 0)
        foodItem.save()

        z_user = request.user
        username = z_user.username

        # username = kdiet_user.objects.get(username=uname)
        date = request.POST.get('date')
        if not food_diary.objects.filter(date=date, username=username).exists():

            variable = request.user
            varibale2 = kdiet_user.objects.get(username=variable.username)

            foodDiary = food_diary()
            foodDiary.date = date
            foodDiary.username = varibale2
            foodDiary.save(force_insert=True)
        else:
            foodDiary = food_diary.objects.get(date=date, username=username)

        foodEntry = food_diary_entry()

        foodEntry.date = foodDiary
        foodEntry.username = foodDiary.username
        foodEntry.entry_id = foodItem
        foodEntry.meal_type = request.POST.get('meal_type')
        foodEntry.save(force_insert=True)
        return render(request, 'subpages/tracker.html')

    return render(request, 'subpages/importNutrients.html')
