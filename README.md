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


## Routes with corrusponding Methods and sample input/output JSONs


