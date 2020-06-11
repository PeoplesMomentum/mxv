# MxV - Momentum's digital democracy platform

## What's this?
This  digital platform was used initially to help in the generation of ideas for Momentum's submissions to the Labour Party Democracy Review.  It will probably broaden into a "Member's hub" after that.

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
3. `yarn shell` (alias for `pipenv shell`) to start the virtual environment (you'll want to do this whenever working on the app).
4. Copy the example environment file in in `configs/example.env` to `mxv/.env`
5. `python manage.py collectstatic` to complete local Django setup.
6a. (not recommended) Run `docker-compose up` to create the database if you have docker installed. OR:
6b. Create a Postgres database called 'mxv' and a Postgres user called 'mxv' with a password of 'mxv' and grant all permissions to that user in the new database (these settings are only for the local database so don't worry about the obvious password!).  Here are the commands to use in `psql`:
	- `create database mxv;`
	- `create user mxv with password 'mxv';`
	- `grant all privileges on database mxv to mxv;`
	- `alter user mxv createdb;`
  - `\c mxv`
  - `create extension citext`
7. `yarn python manage.py migrate` to populate the database with tables by running the migrations.
8. `yarn python manage.py createsuperuser` to add yourself as an admin.
9. `yarn develop` to run the application locally.
	- Site accessible at [http://localhost:8000](http://localhost:8000).
	- Admin site accessible at [http://localhost:8000/admin](http://localhost:8000/admin).
10. `yarn test` to run unit tests, of which there are only a few. You'll need to create extension citext as outlined below.

### Bookmarks

- [GitHub repository](https://github.com/PeoplesMomentum/mxv)

### To pull data from prod

`yarn dbpull` will create a new database in your local server with prod data.

For this to work you'll need to have run 

```
yarn psql
\c template1
create extension citext
```

at least once first.
