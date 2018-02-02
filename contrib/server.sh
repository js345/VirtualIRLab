#! /bin/bash

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

APPDIR=/home/xyu37/metapy-demos
PIDFILE=tmp/pids/server.pid
CONFIGFILE=contrib/server.cfg

restart() {
	pushd $APPDIR > /dev/null
	pyenv activate vir-pyenv
	if [ -e $PIDFILE ] && kill -0 $(cat $PIDFILE)
	then
		echo "Gunicorn is running, reloading..."
		kill -HUP $(cat $PIDFILE)
	else
		echo "Starting new gunicorn process..."
		gunicorn -c $CONFIGFILE server:app
	fi
	echo "Done!"
	popd > /dev/null
}

stop() {
	pushd $APPDIR > /dev/null
	if [ -e $PIDFILE ] && kill -0 $(cat $PIDFILE)
	then
		echo "Stopping gunicorn..."
		kill -QUIT $(cat $PIDFILE)
	fi
	echo "Done!"
	popd > /dev/null
}

case "$1" in
	start)
		restart
		;;
	restart)
		restart
		;;
	stop)
		stop
		;;
	*)
		echo "Usage: {start|stop|restart}"
		exit 1
		;;
	esac