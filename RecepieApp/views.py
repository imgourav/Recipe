from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def recipes(request):

  if request.method == "POST":
    data = request.POST
    recipe_name = data.get('recipe_name')
    recipe_description = data.get('recipe_description')
    recipe_image = request.FILES.get('recipe_image')

    Recipes.objects.create(
      recipe_name = recipe_name,
      recipe_description = recipe_description,
      recipe_image = recipe_image,
    )
    return redirect('/recipes/')

  querySet = Recipes.objects.all()
  context = {'recipes' : querySet}

  return render(request, "recipes.html", context)

def update_recipe(request, id):
  querySet = Recipes.objects.get(id = id)
  
  if request.method == "POST":
    data = request.POST
    recipe_name = data.get('recipe_name')
    recipe_description = data.get('recipe_description')
    recipe_image = request.FILES.get('recipe_image')

    querySet.recipe_name = recipe_name
    querySet.recipe_description = recipe_description

    if recipe_image:
      querySet.recipe_image = recipe_image

    querySet.save()
    return redirect('/recipes/')
  
  context = {'recipes' : querySet}
  return render(request, "update_recipe.html", context)

def delete_recipe(request, id):
  querySet = Recipes.objects.get(id = id)
  querySet.delete()
  return redirect('/recipes/')

# @logout_required(login_url='/logout/')
def login_page(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not User.objects.filter(username=username).exists():
      messages.error(request,"Invalid Username")
      return redirect('/login/')\
      
    user = authenticate(username=username, password=password)
    if user is None:
      messages.error(request,'Invalid Password')
      return redirect('/login/')
    else:
      login(request,user)
      return redirect('/recipes/')
    
  return render(request, 'login.html')

def register_page(request):
  if  request.method == "POST":
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = User.objects.filter(username = username)
    if user.exists():
      messages.error(request,"Username already exists!")
      return redirect("/register/")
    

    user = User.objects.create(
      first_name=first_name,
      last_name=last_name,
      username=username,
    )

    user.set_password(password)
    user.save()

    messages.info(request,"Account Created Successfully!")  
    return redirect('/register/')

  return render(request, 'register.html')

def logout_page(request):
  logout(request)
  return redirect('/login/')