# MxV - Momentum's new digital democracy platform

## Developer setup

### Prerequisites

- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [GitHub account](https://github.com/join)
- [Heroku](https://devcenter.heroku.com/articles/heroku-cli)
- [Heroku account](https://signup.heroku.com/signup/dc) (it's easiest to use the same credentials as your GitHub account)
- Python 3.6 ([Os X](http://docs.python-guide.org/en/latest/starting/install3/osx/), [Windows](http://docs.python-guide.org/en/latest/starting/install3/win/) or [Linux](http://docs.python-guide.org/en/latest/starting/install3/linux/))
- [Pipenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
- [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup)
- [Django](https://docs.djangoproject.com/en/1.11/topics/install/)

### Setup
1. `heroku login` using the email and password for your Heroku/GitHub accounts.
2. `git clone https://github.com/PeoplesMomentum/mxv.git` to get the code.
3. `cd mxv`, `pipenv --three` and `pipenv install` to configure a virtual environment.
4. `pipenv shell` to start the virtual environment (you'll want to do this whenever working on the app).
5. `python manage.py collectstatic` to complete local Django setup.
6. `heroku local` to run the application locally (accessible at [http://localhost:5000](http://localhost:5000)).

### Useful tools

- [LiClipse](http://www.liclipse.com/download.html) (Python/Django version of Eclipse)

### Workflow
This is based on the WaffleBot [workflow](https://help.waffle.io/wafflebot-basics/getting-started-with-the-wafflebot/how-to-use-wafflebot).

- Choose a task from the 'To Do' column on the Waffle board and create a branch with a name that starts with the task number (e.g. `git branch 12-AddUserView`), this will assign the task to you and move the task into the 'In Progress' column.
- Make changes in the branch and test locally.
- Commit the changes and create a pull request on GitHub that uses a [GitHub closing keyword](https://help.github.com/articles/closing-issues-via-commit-messages/) in the description referencing the task number (e.g. `closes #12`).
- Momentum will review the pull request, merge the changes back into master and push the changes to the live application on Heroku.

### Bookmarks

- [GitHub repository](https://github.com/PeoplesMomentum/mxv)
- [Waffle board](https://waffle.io/PeoplesMomentum/mxv)
