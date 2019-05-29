from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Programs, Users, Progress
from django.db import DatabaseError
import json
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import date
from django.forms.models import model_to_dict

# Create your views here.

JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."
KeyErrorMessage = "Erros when accessing the object"
ExceptionMessage = "Some Exceptions Happened"
AuthorizationError = "Not Authorized"

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

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
            # TODO: need to add functionality in order to get the aggregates for the data
            # filter the specified program
            the_program = Programs.objects.filter(id = program_id).get()
            the_program_data = {
                "name": the_program.name, 
                'description': the_program.description, 
                'fitness_goal': the_program.fitness_goal, 
                'author': the_program.author.username, 
                'date': the_program.date
                }
            the_program_data['usage'] = len(list(Progress.objects.filter(
                program = program_id
                ).values('user').distinct()))
            
            w1 = 0
            w2 = 0
            w3 = 0
            w4 = 0
            if(the_program.fitness_goal == "CA"):
                cov = ['mile_time_sec']
            elif(the_program.fitness_goal == "BB"):
                cov = ['weight']
            elif(the_program.fitness_goal == "ST"):
                cov = ['bench_press', 'deadlift', 'squat']
            else:
                cov = ['weight']

            p_val = [w1, w2, w3, w4]
            the_program_data['progress'] = p_val
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

@csrf_exempt
@sensitive_post_parameters()
def allProgress(request):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)
    
    if request.method == "GET":
        try:
            distinct_programs = list(Progress.objects.all().filter(user = current_user.id).values('program').distinct())

            program_obj_list = []
            for pro in distinct_programs:
                print(pro["program"])
                cur_program_obj = Programs.objects.get(id = int(pro["program"]))
                print(model_to_dict(cur_program_obj))
                program_obj_list.append(model_to_dict(cur_program_obj))

        except DatabaseError:
            return HttpResponse(DatabaseErrorMessage, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            # return all programs into the template
            return JsonResponse(program_obj_list, safe = False, content_type = 'application/json', status = 201)

    
    elif request.method == "POST":
        posted_data = jsonHandling(request)
        if posted_data == JSONDecodeFailMessage:
            return HttpResponse(JSONDecodeFailMessage, status = 400)
        try:
            prev_progress = Progress.objects.filter(user = current_user.id)
            if not prev_progress:
                last_progress = None
            else:
                last_progress = prev_progress.latest('date')

            the_user = Users.objects.get(id = current_user.id)
            the_program = Programs.objects.get(id = posted_data['program'])
            the_height = the_user.height
            the_age = calculate_age(the_user.dob)

            if the_user.gender == 'male':
                the_gender = 0
            else: 
                the_gender = 1
            
            if last_progress is None:
                new_progress = Progress.objects.create(
                    user = the_user, 
                    program = the_program, 
                    height = the_height, 
                    gender = the_gender, 
                    age = the_age
                    )
                new_progress.save()
                progress_info = Progress.objects.all().values().filter(
                    pk = new_progress.pk
                    )[0]
            else:

                the_barbell_row = last_progress.barbell_row
                the_bench_press = last_progress.bench_press
                the_dead_lift = last_progress.dead_lift
                the_overhead_press = last_progress.overhead_press
                the_squat = last_progress.squat
                the_dips_count = last_progress.dips_count
                the_pullups_count = last_progress.pullups_count
                the_pushups_count = last_progress.pushups_count
                the_mile_time_sec = last_progress.mile_time_sec
                the_heartrate_bpm = last_progress.heartrate_bpm
                the_steps = last_progress.steps
                the_weight = last_progress.weight
                the_bodyfat_perc = last_progress.bodyfat_perc

                new_progress = Progress.objects.create(
                    user = the_user, 
                    program = the_program, 
                    height = the_height, 
                    gender = the_gender, 
                    age = the_age,
                    barbell_row = the_barbell_row,
                    bench_press = the_bench_press,
                    dead_lift = the_dead_lift,
                    overhead_press = the_overhead_press,
                    squat = the_squat,
                    dips_count = the_dips_count,
                    pullups_count = the_pullups_count,
                    pushups_count = the_pushups_count,
                    mile_time_sec = the_mile_time_sec,
                    heartrate_bpm = the_heartrate_bpm,
                    steps = the_steps,
                    weight = the_weight,
                    bodyfat_perc = the_bodyfat_perc
                    )
                new_progress.save()
                progress_info = Progress.objects.all().values().filter(
                    pk = new_progress.pk
                    )[0]
        except DatabaseError:
            return HttpResponse(DatabaseError, status = 400)
        except KeyError:
            return HttpResponse(DatabaseError, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            # return the newly created transaction as a json object
            return JsonResponse(
                progress_info, 
                safe = False, 
                content_type = 'application/json', 
                status = 201
                )

    else:
        return HttpResponse(BadRequestMessage, status = 405)

@csrf_exempt
@sensitive_post_parameters()
def programProgress(request, program_id):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)

    if request.method == "GET":
        try:
            progress_list = list(Progress.objects.all().filter(
                user = current_user.id,
                program =  program_id
                ).values())

        except DatabaseError:
            return HttpResponse(DatabaseError, status = 400)
        except KeyError:
            return HttpResponse(DatabaseError, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            # return the newly created transaction as a json object
            return JsonResponse(
                progress_list, 
                safe = False, 
                content_type = 'application/json', 
                status = 201
                )

    elif request.method == "POST":
        posted_data = jsonHandling(request)
        if posted_data == JSONDecodeFailMessage:
            return HttpResponse(JSONDecodeFailMessage, status = 400)
        try:
            prev_progress = Progress.objects.filter(user = current_user.id)
            if not prev_progress:
                last_progress = None
            else:
                last_progress = prev_progress.latest('date')

            the_user = Users.objects.get(id = current_user.id)
            the_program = Programs.objects.get(id = program_id)
            the_height = the_user.height
            the_age = calculate_age(the_user.dob)

            if the_user.gender == 'male':
                the_gender = 0
            else: 
                the_gender = 1
            
            if last_progress is None:
                print("1")
                if 'barbell_row' in posted_data:
                    the_barbell_row = posted_data['barbell_row']
                else:
                    the_barbell_row = None
                
                if 'bench_press' in posted_data:
                    the_bench_press = posted_data['bench_press']
                else:
                    the_bench_press = None
                
                if 'dead_lift' in posted_data:
                    the_dead_lift = posted_data['dead_lift']
                else:
                    the_dead_lift = None
                
                if 'overhead_press' in posted_data:
                    the_overhead_press = posted_data['overhead_press']
                else:
                    the_overhead_press = None

                if 'squat' in posted_data:
                    the_squat = posted_data['squat']
                else:
                    the_squat = None
                
                if 'dips_count' in posted_data:
                    the_dips_count = posted_data['dips_count']
                else:
                    the_dips_count = None
                
                if 'pullups_count' in posted_data:
                    the_pullups_count = posted_data['pullups_count']
                else:
                    the_pullups_count = None

                if 'pushups_count' in posted_data:
                    the_pushups_count = posted_data['pushups_count']
                else:
                    the_pushups_count = None
                
                if 'mile_time_sec' in posted_data:
                    the_mile_time_sec = posted_data['mile_time_sec']
                else:
                    the_mile_time_sec = None
                
                if 'heartrate_bpm' in posted_data:
                    the_heartrate_bpm = posted_data['heartrate_bpm']
                else:
                    the_heartrate_bpm = None

                if 'steps' in posted_data:
                    the_steps = posted_data['steps']
                else:
                    the_steps = None
                
                if 'weight' in posted_data:
                    the_weight = posted_data['weight']
                else:
                    the_weight = None
                
                if 'bodyfat_perc' in posted_data:
                    the_bodyfat_perc = posted_data['bodyfat_perc']
                else:
                    the_bodyfat_perc = None

            else:
                the_barbell_row = last_progress.barbell_row
                the_bench_press = last_progress.bench_press
                the_dead_lift = last_progress.dead_lift
                the_overhead_press = last_progress.overhead_press
                the_squat = last_progress.squat
                the_dips_count = last_progress.dips_count
                the_pullups_count = last_progress.pullups_count
                the_pushups_count = last_progress.pushups_count
                the_mile_time_sec = last_progress.mile_time_sec
                the_heartrate_bpm = last_progress.heartrate_bpm
                the_steps = last_progress.steps
                the_weight = last_progress.weight
                the_bodyfat_perc = last_progress.bodyfat_perc

                if 'barbell_row' in posted_data:
                    the_barbell_row = posted_data['barbell_row']
                
                if 'bench_press' in posted_data:
                    the_bench_press = posted_data['bench_press']
                
                if 'dead_lift' in posted_data:
                    the_dead_lift = posted_data['dead_lift']
                
                if 'overhead_press' in posted_data:
                    the_overhead_press = posted_data['overhead_press']

                if 'squat' in posted_data:
                    the_squat = posted_data['squat']
                
                if 'dips_count' in posted_data:
                    the_dips_count = posted_data['dips_count']
                
                if 'pullups_count' in posted_data:
                    the_pullups_count = posted_data['pullups_count']

                if 'pushups_count' in posted_data:
                    the_pushups_count = posted_data['pushups_count']
                
                if 'mile_time_sec' in posted_data:
                    the_mile_time_sec = posted_data['mile_time_sec']
                
                if 'heartrate_bpm' in posted_data:
                    the_heartrate_bpm = posted_data['heartrate_bpm']

                if 'steps' in posted_data:
                    the_steps = posted_data['steps']
                
                if 'weight' in posted_data:
                    the_weight = posted_data['weight']
                
                if 'bodyfat_perc' in posted_data:
                    the_bodyfat_perc = posted_data['bodyfat_perc']             

            new_progress = Progress.objects.create(
                user = the_user, 
                program = the_program, 
                height = the_height, 
                gender = the_gender, 
                age = the_age,
                barbell_row = the_barbell_row,
                bench_press = the_bench_press,
                dead_lift = the_dead_lift,
                overhead_press = the_overhead_press,
                squat = the_squat,
                dips_count = the_dips_count,
                pullups_count = the_pullups_count,
                pushups_count = the_pushups_count,
                mile_time_sec = the_mile_time_sec,
                heartrate_bpm = the_heartrate_bpm,
                steps = the_steps,
                weight = the_weight,
                bodyfat_perc = the_bodyfat_perc
                )
            new_progress.save()
            progress_info = Progress.objects.all().values().filter(
                pk = new_progress.pk
                )[0]
        except DatabaseError:
            return HttpResponse(DatabaseError, status = 400)
        except KeyError:
            return HttpResponse(DatabaseError, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            # return the newly created transaction as a json object
            return JsonResponse(
                progress_info, 
                safe = False, 
                content_type = 'application/json', 
                status = 201
                )


    elif request.method == "DELETE":
        try:
            Progress.objects.filter(
                user = current_user.id, 
                program = program_id
                ).delete()
        except DatabaseError:
            return HttpResponse(DatabaseError, status = 400)
        except KeyError:
            return HttpResponse(DatabaseError, status = 400)
        except Exception:
            return HttpResponse(ExceptionMessage, status = 400)
        else:
            return HttpResponse('Deleted', status = 200)
    else:
        return HttpResponse(BadRequestMessage, status = 405)


def recommendedPrograms(request, fitness_goal):
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponse(AuthorizationError, status = 401)

    if request.method == "GET":
        return HttpResponse(AuthorizationError, status = 401)
    
    else:
        return HttpResponse(BadRequestMessage, status = 405)


