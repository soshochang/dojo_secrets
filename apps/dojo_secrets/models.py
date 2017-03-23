from __future__ import unicode_literals
from IPython import embed
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
  def register(self, postData):
    errors = []
    
    if len(User.objects.filter(email=postData['email'])) > 0:
      errors.append("Email Address already taken!")

    if len(postData['first_name']) < 2:
      errors.append("First Name cannot be empty!")
    if len(postData['last_name']) < 2:
      errors.append("Last Name cannot be empty!")
    if len(postData['email']) < 1:
      errors.append("Email cannot be empty!")
    elif not EMAIL_REGEX.match(postData['email']):
      errors.append("Invalid Email Address!")

    if len(postData['password']) < 1:
      errors.append("Password cannot be empty!")
    elif len(postData['password']) <= 8:
      errors.append("Password must be greater than 8 characters!") 
    if len(postData['password_confirmation']) < 1:
      errors.append("Password confirmation cannot be empty!")      
    elif postData['password'] != postData['password_confirmation']:
      errors.append("Password must match password confirmation")       

    if has_numbers(postData['first_name']):
      errors.append("First Name cannot contain numbers")
    if has_numbers(postData['last_name']):
      errors.append("Last Name cannot contain numbers")  

    if len(errors) == 0:
      hashed_pw = bcrypt.hashpw(postData['password'].encode('utf-8'), bcrypt.gensalt()) 
      u = User.objects.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], password = hashed_pw)
      return (True, u)
    else:
      return (False, errors)

  def login(self, postData):
    errors = []
    u = User.objects.filter(email=postData['email'])
    if len(u) == 0:
      errors.append("Invalid Email/Password")
    else:
      stored_hash = u[0].password
      input_hash = bcrypt.hashpw(postData['password'].encode(), stored_hash.encode())
      if not input_hash == stored_hash:
        errors.append("Invalid Email/Password")

    if len(errors) == 0:
      return (True, u[0])
    else:
      return (False, errors)

def has_numbers(inputString):
  return any(char.isdigit() for char in inputString)

# from apps.dojo_secrets.models import User
class User(models.Model):
  first_name = models.CharField(max_length=38)
  last_name = models.CharField(max_length=38)
  email = models.CharField(max_length=38)
  password = models.CharField(max_length=38)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()

  def __unicode__(self):
    return "id: " + str(self.id) + ", email: " + self.email

# Secret.objects.all()
# Secret.objects.create(content="secret2", creator=u1)
class Secret(models.Model):
  content = models.CharField(max_length=38)
  creator = models.ForeignKey(User, related_name="secrets") 
  created_at = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):
    return "id: " + str(self.id) + ", content: " + self.content

  # def test_name(self):
  #   return "hi"    

  # def liked_by_logged_in_user(self):
  #   embed()
  #   return True

# if Like.objects.filter(secret_id=s.id, user_id=user_id).count() > 0
class Like(models.Model):
  user = models.ForeignKey(User, related_name="likes")
  secret = models.ForeignKey(Secret, related_name="likes") 

  def __unicode__(self):
    return "id: " + str(self.id) + ", user_id: " + str(self.user.id) + ", secret_id: " + str(self.secret.id)
 
