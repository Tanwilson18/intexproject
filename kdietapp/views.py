from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout  # add this
from django.contrib.auth.forms import AuthenticationForm  # add this
from .models import serum_levels
import pip._vendor.requests as requests
from .formserumlevels import serum_levels_form

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
                     "Protein", "Sodium, Na", "Phosphorus"]
    # foodType = None
    # foodType = request.POST.get("foodGroups")
    search = None
    search = request.POST.get("SearchFood")
    parameters = {
        'api_key': '9aSh1S0uTOlVQKP7ZDzmnjgGWYDfOmzK5RnZxcxQ',
        'query': search,
        'dataType': 'Foundation'  # foodType if we decide to do that
    }
    if search != None:
        response = requests.get(
            "https://api.nal.usda.gov/fdc/v1/foods/search", params=parameters)

        data = response.json()
        food_dict = {}
        for i in range(len(data["foods"])):
            food_name = data["foods"][i]["description"]
            food_dict[food_name] = {}

            for j in range(len(data["foods"][i]["foodNutrients"])):
                nutrient_name = data["foods"][i]["foodNutrients"][j]['nutrientName']

                if nutrient_name in nutrient_list:

                    if 'value' in data['foods'][i]['foodNutrients'][j].keys():
                        value = data['foods'][i]['foodNutrients'][j]['value']
                        unit = data['foods'][i]['foodNutrients'][j]['unitName']
                    else:
                        value = 0
                        unit = 0
                    food_dict[food_name][nutrient_name] = [value, unit]

        nutrients = []
        nutrientValues = {}
        # wht does this do????
        for i in food_dict:
            for key in food_dict[i]:
                if key == "Water":
                    food_dict[i][key][1] = 'mL'
                nutrientValue = str(
                    food_dict[i][key][0]) + " " + food_dict[i][key][1]
                nutrients.append(key)
                nutrientValues = {key: nutrientValue}

        context = {
            'foods': food_dict,
            'nutrients': nutrients,
            'nutrientValues': nutrientValues,
            'list': nutrients
        }
        return render(request, 'subpages/tracker.html', context)
    else:
        return render(request, 'subpages/tracker.html')


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
            return redirect("index")
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
                # once logged in automaticallt redirects
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'login.html', context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


def profile(request):
    return render(request, 'profile.html')
