# MxV - Momentum's new digital democracy platform

## What's this?
This new digital platform will be used initially to help in the generation of ideas for Momentum's submissions to the Labour Party Democracy Review.  It will probably broaden into a "Member's hub" after that.

The intention is for this platform to generate a transparent debate between Momentum members about the changes we would like to see in the Labour Party by broadening discussions about party reform to as wide a pool of activists as possible, in order to fully harness the ideas, creativity and experiences of our membership and ensure that Momentum’s submissions to the Democracy Review are as representative as possible of the views of our members.

See [this](https://github.com/PeoplesMomentum/mxv/blob/master/Docs/Requirements/MxV%20Summary%20Doc.pdf) document for more details of the platform requirements.

## Get involved!

Do you have development skills (see below for the technologies we've used)?  Then get involved!  This is your chance to put your skills to use in the political arena in order to further Momentum's and the Labour Party's aims.  This is *not* a theoretical exercise, your contributions *will* be used!

## Developer setup

### Prerequisites

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [GitHub account](https://github.com/join)
- Python 3.6 ([Os X](http://docs.python-guide.org/en/latest/starting/install3/osx/), [Windows](http://docs.python-guide.org/en/latest/starting/install3/win/) or [Linux](http://docs.python-guide.org/en/latest/starting/install3/linux/))
- [Pipenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
- [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup)
- [Django](https://docs.djangoproject.com/en/1.11/topics/install/)

### Setup

1. `git clone https://github.com/PeoplesMomentum/mxv.git` to get the code.
2. `cd mxv`, `pipenv --three` and `pipenv install` to configure a virtual environment.
2a. If you have an error with -lssl, see https://stackoverflow.com/questions/11538249/python-pip-install-psycopg2-install-error
3. `pipenv shell` to start the virtual environment (you'll want to do this whenever working on the app).
4. Copy the example environment file in in `configs/example.env` to `mxv/.env`
5. `python manage.py collectstatic` to complete local Django setup.
6a. Run `docker-compose up` to create the database if you have docker installed. OR:
6b. Create a Postgres database called 'mxv' and a Postgres user called 'mxv' with a password of 'mxv' and grant all permissions to that user in the new database (these settings are only for the local database so don't worry about the obvious password!).  Here are the commands to use in `psql`:
	- `create database mxv;`
	- `create user mxv with password 'mxv';`
	- `grant all privileges on database mxv to mxv;`
	- `alter user mxv createdb;`
7. `python manage.py migrate` to populate the database with tables by running the migrations.
8. `python manage.py createsuperuser` to add yourself as an admin.
9. `python manage.py runserver` to run the application locally.
	- Site accessible at [http://localhost:8000](http://localhost:8000).
	- Admin site accessible at [http://localhost:8000/admin](http://localhost:8000/admin).

### Useful tools

- [LiClipse](http://www.liclipse.com/download.html) (Python/Django version of Eclipse)
	- Set up a python interpreter for the virtual environment so that the external packages are found
		- LiClipse, Preferences, PyDev, Interpreters, Python Interpreter, New...
		- Use this interpreter in the project PyDev settings.

### Workflow
This is based on the WaffleBot [workflow](https://help.waffle.io/wafflebot-basics/getting-started-with-the-wafflebot/how-to-use-wafflebot).

1. Choose a task from the 'To Do' column on the Waffle board and create a branch with a name that starts with the task number, then push the branch to origin; the task will be assigned to you and moved into the 'In Progress' column on the Waffle board.
	- `git branch 12-AddUserView`
	- `git checkout 12-AddUserView`
	- `git commit --allow-empty -m "Started work on 12-AddUserView."`
	- `git push origin 12-AddUserView`
2. Discuss the task in the #digitaldemocracy Slack channel if it's not absolutely clear what needs to be done.
3. Make changes in the branch and test locally.
4. Commit the changes on the branch, push the branch to origin and create a pull request on GitHub that uses a [GitHub closing keyword](https://help.github.com/articles/closing-issues-via-commit-messages/) in the description referencing the task number (e.g. `closes #12`), this will move the task into the 'Needs Review' column.
5. Momentum will review the pull request, merge the changes back into master (which marks the task as 'Done' on Waffle) and push the changes to the live application on Heroku.

### Bookmarks

- [GitHub repository](https://github.com/PeoplesMomentum/mxv)
- [Waffle board](https://waffle.io/PeoplesMomentum/mxv)
