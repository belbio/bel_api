


# From https://github.com/autoferrit/docker-gunicorn-examples/blob/master/falcon/Makefile
NAMESPACE=skiftcreative
APP=falcon

build:
	docker build -t ${NAMESPACE}/${APP} .
run:
	docker run --name=${APP} --detach=true -p 5000:5000 ${NAMESPACE}/${APP}
clean:
	docker stop ${APP} && docker rm ${APP}
reset: clean
	docker rmi ${NAMESPACE}/${APP}
interactive:
	docker run --rm --interactive --tty --name=${APP} ${NAMESPACE}/${APP} bash
push:
	docker push ${NAMESPACE}/${APP}

test:
	bin/runtests.sh
