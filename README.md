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
     "date": "2019-04-18T18:53:12Z"<br />
   }<br />

- PATCH: Update program specified in the route of url as id (Only parameters that are being updated need to be specified)


   - Sample input:<br />
   {<br />
     "name": "Sample Program for Pros", <br />
     "description": "Sample Program Updated", <br />
     "fitness_goal": "WL" <br />
   }<br />

- DELETE: deletes the specified program based off of the id provided in the route of the url


