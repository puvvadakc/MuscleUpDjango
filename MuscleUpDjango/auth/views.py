from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect 
from django.contrib.auth import authenticate, login, logout
from main.models import Users
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
from django.db import DatabaseError
import json

# Create your views here.
JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."
KeyErrorMessage = "Erros when accessing the object"
ExceptionMessage = "Some Exceptions Happened"
AuthorizationError = "Not Authorized"

def adminUser():
    """ This will create an admin user, which is specifically for internal use.
    The user will only be created if it does not exist already. """

    # Checking if admin exists
    if len(Users.objects.all().values().filter(membership="administrator",
           username="admin")) == 0:
        
        # Try to create admin user if it does not already exist
        try:
            user = Users.objects.create_user(username = "admin", 
                   password = "admin", first_name = "Admin",
                   last_name = 'Account', email = 'admin@email.com')
            user.membership="administrator"
            user.gender = "female"
            user.dob = '1997-01-01'
            user.height = 100
            user.save()
        
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status=400)

adminUser()

@csrf_exempt
@sensitive_post_parameters()
def jsonHandling(request):
    """ This function's main purpose is to manage error handling for 
    when retrieving and decoding the JSON from the request body. """
    # check if there are errors in the posted data
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JSONDecodeFailMessage
    except Exception:
        return ExceptionMessage
    else:
        return data

@csrf_exempt
@sensitive_post_parameters()
def register(request):
    """This will register a new user according to the data
       provided in the form.
       POST: submit the registration application 
    """
    # This checks the HTTP methods.
    if request.method == 'POST':
        posted_data = jsonHandling(request)
        if posted_data == JSONDecodeFailMessage:
            return HttpResponse(JSONDecodeFailMessage, status = 400)
        try:
            password = posted_data['password']
            passwordconf = posted_data['passwordconf']
            if not password == passwordconf:
                return HttpResponse("Passwords did not match.", status = 400)
            username = posted_data['username']
            email = posted_data['email']
            first_name = posted_data['first_name']
            last_name = posted_data['last_name']
            gender = posted_data['gender']
            dob = posted_data['dob']
            height = posted_data['height']

            user = Users.objects.create_user(username = username, 
                    password = password, first_name = first_name,
                    last_name = last_name, email = email, gender = gender,
                    dob = dob, height = height)
            user.save()
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status = 400)
        except KeyError:
            return HttpResponse(KeyErrorMessage, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            return HttpResponse("Registration Successful", status = 200)
    else:
        return HttpResponse("Method not allowed", status = 405)

@csrf_exempt
@sensitive_post_parameters()
def signin(request):
    """This will check the user's authentification and 
       decides if he or she is legal to sign in.

       'POST': sign in the user if the username and 
       password are all correct
    """
    if request.method == 'POST':
        posted_data = jsonHandling(request)
        if posted_data == JSONDecodeFailMessage:
            return HttpResponse(JSONDecodeFailMessage, status = 400)
            # try to sign in a user
        try:
            username = posted_data['username']
            password = posted_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("Sign In Successful", status = 200)
            else:
                return HttpResponse("Invalid credentials.", status = 401)
        except KeyError:
            return HttpResponse(KeyError, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
    else:
        return HttpResponse("Method not allowed on /auth/signin.", status = 405)

@csrf_exempt
@sensitive_post_parameters()
def signout(request):
    """This lets user sign out if he has logged in.

    'GET': tells the user whether he has logged out 
    successfully.
    """
    if request.method == 'GET':
        # logs out a user if he has signed in
        if request.user.is_authenticated:
            logout(request)
            return HttpResponse('Sign out successful.', status = 200)
        else:
            return HttpResponse('Not logged in.', status = 200)
    else:
        return HttpResponse("Method not allowed on /auth/signout.", status = 405)


@csrf_exempt
@sensitive_post_parameters()
def update(request):
    """This will register a new user according to the data
       provided in the form.
       PATCH: submit the update application 
    """
    # This checks the HTTP methods.
    if request.method == 'PATCH':
        if request.user.is_authenticated:
            posted_data = jsonHandling(request)
            if posted_data == JSONDecodeFailMessage:
                return HttpResponse(JSONDecodeFailMessage, status = 400)
            try:
                the_user = Users.objects.filter(id = request.user.id).get()
                if 'password' in posted_data and 'passwordconf' in posted_data:
                    password = posted_data['password']
                    passwordconf = posted_data['passwordconf']
                    if not password == passwordconf:
                        return HttpResponse("Passwords did not match.", status = 400)
                    the_user.set_password(password)
                if 'email' in posted_data:
                    the_user.email = posted_data['email']
                if 'username' in posted_data:
                    the_user.username = posted_data['username']


                the_user.save()
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status = 400)
            except KeyError:
                return HttpResponse(KeyErrorMessage, status = 400)
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)
            else:
                return HttpResponse("Update Successful", status = 200)
        else:
            return HttpResponse('Not logged in.', status = 200)
    else:
        return HttpResponse("Method not allowed", status = 405)


@csrf_exempt
@sensitive_post_parameters()
def delete(request):
    """This lets user sign out if he has logged in.

    'DELETE': tells the user whether he has logged out 
    and delete successfully.
    """
    if request.method == 'DELETE':
        # logs out a user if he has signed in
        if request.user.is_authenticated:
            logout(request)
            u = Users.objects.get(id = request.user.id)
            u.delete()
            return HttpResponse('Deletion successful.', status = 200)
        else:
            return HttpResponse('Not logged in.', status = 400)
    else:
        return HttpResponse("Method not allowed on /auth/signout.", status = 405)