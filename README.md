# MxV - Momentum's new digital democracy platform

## Developer setup

### Prerequisites

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [GitHub account](https://github.com/join)
- [Heroku](https://devcenter.heroku.com/articles/heroku-cli)
- [Heroku account](https://signup.heroku.com/signup/dc)
- Python 3.6 ([Os X](http://docs.python-guide.org/en/latest/starting/install3/osx/), [Windows](http://docs.python-guide.org/en/latest/starting/install3/win/) or [Linux](http://docs.python-guide.org/en/latest/starting/install3/linux/))
- [Pipenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
- [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup)
- [Django](https://docs.djangoproject.com/en/1.11/topics/install/)

### Setup
1. `heroku login` using the email and password for your Heroku account.
2. `git clone https://github.com/PeoplesMomentum/mxv.git` to get the code.
3. `cd mxv`, `pipenv --three` and `pipenv install` to configure a virtual environment.
4. `pipenv shell` to start the virtual environment (you'll want to do this whenever working on the app).
5. `python manage.py collectstatic` to complete local Django setup.
6. Create a Prostgres database called 'mxv' and a Postgres user called 'mxv' with a password of 'mxv' and grant all permissions to that user in the new database (these settings are only for the local database so don't worry about the obvious password!).  Here are the commands to use in `psql`:
	- `create database mxv;`
	- `create user mxv with password 'mxv';`
	- `grant all privileges on database mxv to mxv;`
	- `alter user mxv createdb;`
7. `python manage.py migrate` to populate the database with tables by running the migrations.
8. `python manage.py createsuperuser` to add yourself as an admin.
9. `heroku local` to run the application locally.
	- Site accessible at [http://localhost:8000](http://localhost:8000).
	- Admin site accessible at [http://localhost:8000/admin](http://localhost:8000/admin).

### Useful tools

- [LiClipse](http://www.liclipse.com/download.html) (Python/Django version of Eclipse)

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
5. Momentum will review the pull request, merge the changes back into master and push the changes to the live application on Heroku and mark the task as 'Done' on Waffle.

### Bookmarks

- [GitHub repository](https://github.com/PeoplesMomentum/mxv)
- [Waffle board](https://waffle.io/PeoplesMomentum/mxv)
