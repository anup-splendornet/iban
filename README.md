# iban
## Django application to manage (CRUD) users and their bank account data (IBAN).

- Require Python 3.x 

- Setup virtualenvwrapper Ref: [https://virtualenvwrapper.readthedocs.io/en/latest/](https://virtualenvwrapper.readthedocs.io/en/latest/)

- We can alias to Python in my case it is python3 to execute version 3

- `alias python3='/usr/bin/python3'`

- `sudo apt-get -y install python3-pip` One time only

- `pip install virtualenvwrapper` OR `pip3 install virtualenvwrapper` pip3 is soft link / alias.

- `export WORKON_HOME=~/Envs`

- `mkdir -p $WORKON_HOME`

- `source /usr/local/bin/virtualenvwrapper.sh` This can achieved using Ref: [https://stackoverflow.com/questions/21928555/virtualenv-workon-command-not-found](https://stackoverflow.com/questions/21928555/virtualenv-workon-command-not-found)

- `mkvirtualenv iban`

- `pip3 install django==1.11`

- Daily we need only to fire command like `workon iban` to enter specific python version to execute code.

- Ensure Django version by typing python `-m django --version`

- django-admin startproject ibanapp Ref: [https://docs.djangoproject.com/en/1.11/intro/tutorial01/](https://docs.djangoproject.com/en/1.11/intro/tutorial01/)

- `python manage.py runserver`
    OR
- `python manage.py runserver 0.0.0.0:8000`
    OR
- `python manage.py runserver 0.0.0.0:8000 --settings=iban.settings`

- Now you start development using branches at remote machine. Please refer Taiga for branch names for every one.

- Every time you add new packages / module please fire this command and commit `pip3 freeze > requirements.txt` the file.

