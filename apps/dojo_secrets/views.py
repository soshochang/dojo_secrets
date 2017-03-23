from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .models import Secret
from .models import Like
from IPython import embed
from django.db.models import Count

# Create your views here.
def index(request):
  return render(request, "dojo_secrets/index.html")

def register(request):
  user_hash = {
    "first_name" : request.POST['first_name'],
    "last_name" : request.POST['last_name'],
    "email" : request.POST['email'],
    "password" : request.POST['password'],
    "password_confirmation" : request.POST['password_confirmation']
  }
  user = User.objects.register(user_hash)
  if user[0] == True:
    request.session['user_id'] = user[1].id
    messages.success(request, request.POST['email'] + ' successfully created')
    return redirect("/success/"+ str(user[1].id))
  else:  
    # user[1] is an array of errors
    for m in user[1]:
      messages.error(request, m)

  return redirect("/")

def login(request):
  user_hash = {
    "email" : request.POST['email'],
    "password" : request.POST['password']
  }
  user = User.objects.login(user_hash)
  if user[0] == True:
    request.session['user_id'] = user[1].id
    messages.success(request, request.POST['email'] + ' successfully logged in')
    return redirect("/success/" + str(user[1].id))
  else:  
    # user[1] is an array of errors
    for m in user[1]:
      messages.error(request, m)
    return redirect("/")
  
def success(request, id):
  if 'user_id' not in request.session:
    return redirect("/")
  else: 
    context = {
      "user" : User.objects.get(id=id)
    }
    if str(request.session['user_id']) == id:
      return render(request, "dojo_secrets/success.html", context)
    else:
      return redirect("/")

def logout(request):
  request.session.clear()
  return redirect("/")



def home(request):
  secrets = Secret.objects.all().order_by('-id')[:5]
  secrets_and_is_liked = []
  for s in secrets:
    if s.likes.all().filter(user_id=request.session['user_id']).count() > 0:
      is_liked_by_logged_in_user = True
    else:
      is_liked_by_logged_in_user = False
    secrets_and_is_liked.append([s,is_liked_by_logged_in_user])

  context = {
    "secrets_and_is_liked" : secrets_and_is_liked,
    "user_id" : request.session['user_id']
  }

  return render(request, "dojo_secrets/home.html", context)

def most_popular(request):
  # Player.objects.annotate(num_teams=Count('all_teams')).order_by('-num_teams')
  secrets = Secret.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')
  # secrets = Secret.objects.all().order_by('-id')
  secrets_and_is_liked = []
  for s in secrets:
    if s.likes.all().filter(user_id=request.session['user_id']).count() > 0:
      is_liked_by_logged_in_user = True
    else:
      is_liked_by_logged_in_user = False
    secrets_and_is_liked.append([s,is_liked_by_logged_in_user])

  context = {
    "secrets_and_is_liked" : secrets_and_is_liked,
    "user_id" : request.session['user_id']
  }

  return render(request, "dojo_secrets/most_popular.html", context)  

def create_secret(request):
  content = request.POST['content']
  user_id = request.session['user_id']
  Secret.objects.create(content=content, creator_id=user_id)
  return redirect("/home")

def delete_secret(request):
  secret_id = request.POST['secret_id']
  s = Secret.objects.get(pk=secret_id)
  s.delete()
  return redirect("/home")  

# Like.objects.create(secret=s1, user=u1)
def create_like(request):
  secret_id = request.POST['secret_id']
  user_id = request.session['user_id']
  Like.objects.create(secret_id=secret_id, user_id=user_id)
  return redirect("/home")

#PLAN
# draw ERD
  # user, secret, like(secret_id, user_id)
# add the routes
# build the views - just display something
  # index(home) page for 5 or 10 most recent secrets
  # most popular page of sorted secrets
# can create secrets
# add delete functionality of secrets
# add like functionality of secret