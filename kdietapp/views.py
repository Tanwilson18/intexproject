from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this
from .models import serum_levels
import pip._vendor.requests as requests
from .formserumlevels import serum_levels_form
from .models import kdiet_user, food
import json

# Create your views here.


def indexPageView(request):
    return render(request, 'index.html')


def serumLevelPageView(request):
    data = serum_levels.objects.all()
    if request.method == 'POST':
        form = serum_levels_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/serum_levels')
    else:
        form = serum_levels_form()
    context = {
        'data': data,
        'form': form,
    }
    return render(request, 'subpages/serum_levels.html', context)


def trackerPageView(request):
    nutrient_list = ["Potassium, K", "Water",
                     "Protein", "Sodium, Na", "Phosphorus, P"]
    # foodType = None
    # foodType = request.POST.get("foodGroups")
    search = None
    search = request.POST.get("SearchFood")
    parameters = {
        'api_key': '9aSh1S0uTOlVQKP7ZDzmnjgGWYDfOmzK5RnZxcxQ',
        'query': search,
        # 'dataType': 'Foundation'  # foodType if we decide to do that
    }
    if search != None:
        response = requests.get(
            "https://api.nal.usda.gov/fdc/v1/foods/search", params=parameters)

        data = response.json()
        food_dict = {}
        if len(data['foods']) == 0:
            return render(request, 'subpages/tracker.html')
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
                        #unit = data['foods'][i]['foodNutrients'][j]['unitName']
                    else:
                        value = 0
                        #unit = 0
                    food_dict[food_name][nutrient_name] = [value]  # , unit]

        nutrients = []
        nutrientValues = {}
        for i in food_dict:
            for key in food_dict[i]:
                # if key == "Water":
                #    food_dict[i][key][1] = 'mL'
                nutrientValue = food_dict[i][key][0]
                #nutrientMeasure = food_dict[i][key][1]
                nutrients.append(key)
                nutrientValues = {key: nutrientValue}
                #nutrientMeasures = {key: nutrientMeasure}

            context = {
                'foods': food_dict,
                'nutrients': nutrients,
                'nutrientValues': nutrientValues,
                # 'nutrientMeasure': nutrientMeasures,
                'list': nutrients
            }

        return render(request, 'subpages/tracker.html', context)
    else:
        return render(request, 'subpages/tracker.html')


def addFoodPageView(request):
    nutrients = ""
    nutrients_dict = {}
    foodName = request.GET.get("foodName")
    nutrients = request.GET.get(foodName+"-nutrients")
    mealType = request.POST.get('mealtype')
    # date = request.POST.get('date')

    if nutrients is None:
        pass
    else:
        nutrients = nutrients.replace('\'', '\"')
        nutrients_dict = json.loads(nutrients)
        test = json.dumps(nutrients_dict, indent=4)
        print(test)

    context = {
        'foodName': foodName,
        'nutrients': nutrients_dict,
        'mealType': mealType
    }

    # if request.method == "Post":
    #     foodItem = food()
    #     foodItem.name = request.GET.get('foodName')

    #     foodItem.save()

    return render(request, 'subpages/addFood.html', context)


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


def deleteUserPageView(request, username):
    data = kdiet_user.objects.get(id=username)
    data.delete()
    return indexPageView(request)


def pricingPageView(request):
    return render(request, 'subpages/pricing.html')


def bloghomePageView(request):
    return render(request, 'subpages/blog-home.html')


def blogpostPageView(request):
    return render(request, 'subpages/blog-post.html')


def faqPageView(request):
    return render(request, 'subpages/faq.html')


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
