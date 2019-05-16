from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Programs, Users
from django.db import DatabaseError
import json
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.

JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."
KeyErrorMessage = "Erros when accessing the object"
ExceptionMessage = "Some Exceptions Happened"
AuthorizationError = "Not Authorized"

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
def programs(request):
    """ This view handles all requests made to /programs route. When a
    GET request is made, all the programs currently within the website
    database will be displayed, including their information about address.
    When a POST request is made (only admins can add program to website)
    new Programs can be added to database, by specifying name and address 
    info."""
    if request.method == 'GET':
        try:
            program_list = list(Programs.objects.all().values())
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            # return all programs into the template
            return JsonResponse(program_list, safe = False, content_type = 'application/json', status = 201)

    elif request.method == 'POST':
        # if the user is logged in
        if not request.user.is_authenticated:
             return HttpResponse(AuthorizationError, status = 401)
        current_user = request.user
        # check if the user has right authorization

        posted_data = jsonHandling(request)
        if posted_data == JSONDecodeFailMessage:
            return HttpResponse(JSONDecodeFailMessage, status = 400)
        else:
            try:
                # create a new program
                new_program = Programs.objects.create(
                    name = posted_data['name'], 
                    description = posted_data['description'], 
                    fitness_goal = posted_data['fitness_goal'], 
                    author = Users.objects.get(id=current_user.id)
                    )
                new_program.save()
                new_program_info = Programs.objects.all().values().filter(pk = new_program.pk)[0]
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status = 400)
            except KeyError:
                return HttpResponse(KeyErrorMessage, status = 400)
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)
            else:
                # return the newly created program as a json object
                return JsonResponse(
                    new_program_info, 
                    safe = False, 
                    content_type = 'application/json', 
                    status = 201
                    )
    else:
        return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt
@sensitive_post_parameters()
def specificProgram(request, program_id):
    """ This view handles all requests made to /programs/<id>. When a GET
    request is made, all the information specific to the program is displayed.
    When a PATCH request is made (only admins can patch and delete) information
    about the theater such as name and address can be changed and saved. When 
    a DELETE request is made, the specific program will be deleted from the
    website. """
    if request.method == 'GET':
        try: 
            # filter the specified program
            the_program = Programs.objects.filter(id = program_id).get()
            the_program_data = {
                "name": the_program.name, 
                'description': the_program.description, 
                'fitness_goal': the_program.fitness_goal, 
                'author': the_program.author.username, 
                'date': the_program.date
                }
        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            # return the program data as a json object
            return JsonResponse(
                the_program_data, 
                safe = False, 
                content_type = 'application/json', 
                status = 201
                )
    elif request.method == 'PATCH':
        if not request.user.is_authenticated:
             return HttpResponse(AuthorizationError, status = 401)
        current_user = request.user

        posted_data = jsonHandling(request)
        if posted_data == JSONDecodeFailMessage:
            return HttpResponse(JSONDecodeFailMessage, status = 400)
        else:
            try:
                the_program = Programs.objects.filter(id = program_id).get()
                if current_user.id != the_program.author.id:
                    return HttpResponse(AuthorizationError, status = 403)
                changed_data = {}
                # checks what types of data the user wants to modify for the 
                # program
                if 'name' in posted_data:
                    the_program.name = posted_data['name']
                    changed_data['name'] = posted_data['name']
                if 'description' in posted_data:
                    the_program.description = posted_data['description']
                    changed_data['description'] = posted_data['description']
                if 'fitness_goal' in posted_data:
                    the_program.fitness_goal = posted_data['fitness_goal']
                    changed_data['fitness_goal'] = posted_data['fitness_goal']
                the_program.save()
            except KeyError:
                return HttpResponse(KeyErrorMessage, status = 400)
            except DatabaseError:
                return HttpResponse(DatabaseError, status = 400)
            except Exception:
                return HttpResponse(ExceptionMessage, status = 400)
            else:
                # return the modified data as a json object
                return JsonResponse(
                    changed_data, 
                    safe = False, 
                    content_type = 'application/json', 
                    status = 201
                    )
    # delete the specified program
    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
             return HttpResponse(AuthorizationError, status = 401)
        try:
            the_program = Programs.objects.get(id= program_id)
            if request.user.id != the_program.author.id:
                return HttpResponse(AuthorizationError, status = 403)
            the_program.delete()
        except DatabaseError:
            return HttpResponse(DatabaseError, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            # return a plain text message if the theater is program
            # successfully
            return HttpResponse('Deleted', status = 200)
    else:
        return HttpResponse(BadRequestMessage, status = 405)