# MuscleUpDjango

**DO NOT PUSH env to the Github**

**Please create your own branch and push to your branch, if you have made changes. Create a pull request on this github repo, and notify me so that I can review the changes, and accept the pull request to merge**


## Initial Set Up of Application


**DO NOT PUSH env to the Github**

- Make sure you have python 3, and install pip if you do not have pip
  - **When installing python, make sure to check the box in installation process which adds it to PATH system variables**
  - Installing pip on Linux: sudo apt-get install python3-pip
- clone repo
- cd into repo
- you should be in a directory with only one other folder called "MuscleUpDjango" and this README
- install virtualenv 
  - Linux: sudo pip3 install virtualenv 
  - Windows: pip install virtualenv
- create new virtualenv
  - Command to run: virtualenv env

**DO NOT PUSH env to the Github**

- activate virtualenv
  - Linux: source env/bin/activate
  - Windows: env/Scripts/activate    (copy and paste and run as is, and make sure to be using Powershell)
  - **In order to deactivate virtualenv its as simple as running "deactivate" in the directory**
- install django
  - Linux: pip install django (try pip3 install django if normal pip does not work, but it should since you are in virtualenv now)
  - Windows: pip install django

**DO NOT PUSH env to the Github**

- cd into MuscleUpDjango/
- you should see a manage.py file (you are in the wrong directory if you dont see this file)
- run the application
  - Linux: python manage.py runserver (try python3 manage.py runserver if first command does not work but it should work, hopefully)
  - Windows: python manage.py runserver

- Ctrl + C if you want to terminate the server


## Routes with corresponding Methods and sample input/output JSONs

**An admin account is already made so we can use it for testing**

**Username: admin**

**Password: admin**

### /auth/register

- POST : This creates a brand new user (ALL JSON PARAMETERS MUST BE INCLUDED)

   - Sample input:<br />
   {<br />
     "username": "kimboslice123",<br />
     "password": "password123", <br />
     "passwordconf": "password123", <br />
     "email": "kimbo@email.com", <br />
     "first_name": "Kimbo",<br />
     "last_name": "Slice",<br />
     "gender": "male", (Can be only 'male' or 'female')<br />
     "dob": "1996-01-01", (YYYY-MM-DD)<br />
     "height": 90 (make sure to not pass in string)<br />
   }<br />


### /auth/signin

- POST: Signs in user (ALL JSON PARAMETERS MUST BE INCLUDED)

   - Sample input:<br />
   {<br />
     "username": "kimboslice123",<br />
     "password": "password123" <br />
   }<br />

### /auth/signout

- GET: Signs out user (User must be signed in, in order to be able to sign out)

### /auth/update

- PATCH: Update user information (Only parameters for information that is being updated should be included in JSON)

   - Sample input:<br />
   {<br />
     "username": "kimboslice123",<br />
     "password": "password123", <br />
     "passwordconf": "password123", <br />
     "email": "kimbo@email.com" <br />
   }<br />


### /auth/delete

- DELETE: Deletes the user that is currently signed in

### /programs

- GET: Gets a list of all the programs' information as JSON

   - Sample output:<br />
   [<br />
     {<br />
       "id": "1",<br />
       "name": "Sample Program", <br />
       "description": "Sample Program for Testing", <br />
       "fitness_goal": "CA", <br />
       "author": "1",<br />
       "date": "2019-04-18T18:53:12Z"<br />
     },<br />
     {<br />
       "id": "2",<br />
       "name": "Sample Program 2", <br />
       "description": "Sample Program 2 for Testing", <br />
       "fitness_goal": "WL", <br />
       "author": "1",<br />
       "date": "2019-04-18T18:53:12Z"<br />
     }<br />
   ]<br />


- POST: Create new program and adds to database (Musted be logged in to do so)

   - Sample input:<br />
   {<br />
     "name": "Sample Program", <br />
     "description": "Sample Program for Testing", <br />
     "fitness_goal": "WL" (Must be BB, ST, CA, or WL)<br />
   }<br />

### /programs/(id)

- GET: Gets the specific program based off of the id provided in the route of the url

   - Sample output:<br />
   {<br />
     "id": "1",<br />
     "name": "Sample Program", <br />
     "description": "Sample Program for Testing", <br />
     "fitness_goal": "CA", <br />
     "author": "kimboslice123",<br />
     "date": "2019-04-18T18:53:12Z",<br />
     "usage": "300", <br />
     "progress": ["23", "26", "45", "60"] <br />
   }<br />

- PATCH: Update program specified in the route of url as id (Only parameters that are being updated need to be specified)


   - Sample input:<br />
   {<br />
     "name": "Sample Program for Pros", <br />
     "description": "Sample Program Updated", <br />
     "fitness_goal": "WL" <br />
   }<br />

- DELETE: deletes the specified program based off of the id provided in the route of the url


### /progress

- GET: Returns a list of all the programs what the user has progress recorded for, both currently active programs and previous programs tha the user has used.

- POST:
   - Sample output:<br />
   [<br />
     {<br />
       "id": "1",<br />
       "name": "Sample Program", <br />
       "description": "Sample Program for Testing", <br />
       "fitness_goal": "CA", <br />
       "author": "1",<br />
       "date": "2019-04-18T18:53:12Z"<br />
     },<br />
     {<br />
       "id": "2",<br />
       "name": "Sample Program 2", <br />
       "description": "Sample Program 2 for Testing", <br />
       "fitness_goal": "WL", <br />
       "author": "1",<br />
       "date": "2019-04-18T18:53:12Z"<br />
     }<br />
     ... <br />
   ]<br />


### /progress/(program_id)

- GET: Gets all the user non null data previously added as progress of the specific program according to the parameter in the URL.
     
     - Sample output:<br />
     [<br />
       {<br />
         "id": "1",<br />
         "user": "2", <br />
         "program": "3", <br />
         "date": "2019-04-18T18:53:12Z", <br />
         "height": "70",<br />
         "gender": "1", (0 means male, 1 means female) <br />
         "age": "20",<br />
         "barbell_row": "120",<br />
         "bench_press": "100",<br />
         "dead_lift": "200",<br />
         "overhead_press": "100",<br />
         "squat": "200",<br />
         "dips_count": "20",<br />
         "pullups_count": "20",<br />
         "pushups_count": "30",<br />
         "mile_time_sec": "600",<br />
         "heartrate_bpm": "70",<br />
         "steps": "1000",<br />
         "weight": "200",<br />
         "bodyfat_perc": "0.16" <br />
       }, <br />
       {<br />
         "id": "2",<br />
         "user": "2", <br />
         "program": "3", <br />
         "date": "2019-04-18T18:53:12Z", <br />
         "height": "70",<br />
         "gender": "1", (0 means male, 1 means female) <br />
         "age": "20",<br />
         "barbell_row": "120",<br />
         "bench_press": "100",<br />
         "dead_lift": "200",<br />
         "overhead_press": "100",<br />
         "squat": "200",<br />
         "dips_count": "20",<br />
         "pullups_count": "20",<br />
         "pushups_count": "30",<br />
         "mile_time_sec": "600",<br />
         "heartrate_bpm": "70",<br />
         "steps": "1000",<br />
         "weight": "200",<br />
         "bodyfat_perc": "0.16" <br />
       } <br />
     ]<br />

- POST: sample input is similar to sample output, except that user, program, date, height, gender, or age, should not be passed in, any of the other keys can be posted as an entry, any field not passed in will be held as a null value.

- DELETE: Deletes all the progress of a specific program, for the specified logged in user.



### /recommended/(fitness_goal)

fitness_goal passed in through the parameter should be a number between 1-4 (1 means bodybuilding, 2 means strength, 3 means cardio, 4 means weightloss)

- GET: Gets the 5 best programs for the logged in user according to the specified fitness goal.

   - Sample output:<br />
   [<br />
     {<br />
       "id": "1",<br />
       "name": "Sample Program", <br />
       "description": "Sample Program for Testing", <br />
       "fitness_goal": "CA", <br />
       "author": "1",<br />
       "date": "2019-04-18T18:53:12Z"<br />
     },<br />
     {<br />
       "id": "2",<br />
       "name": "Sample Program 2", <br />
       "description": "Sample Program 2 for Testing", <br />
       "fitness_goal": "WL", <br />
       "author": "1",<br />
       "date": "2019-04-18T18:53:12Z"<br />
     }<br />
     ... <br />
   ]<br />




