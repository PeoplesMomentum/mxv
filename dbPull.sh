APP=mxv

export ENVPATH=./mxv/.env

HEROKU=heroku 
TODAY=`date "+%m-%d"`
DATE_READABLE=`date +%Y-%m-%dT%H:%M:%S%z`
DB="${APP}_backup_${TODAY}"

dropdb $DB

$HEROKU pg:pull DATABASE_URL $DB --app $APP
echo >> $ENVPATH
echo "# Written by dbpull on" $DATE_READABLE >> $ENVPATH
echo "MXV_DATABASE_NAME=${DB}" >> $ENVPATH
