# Run make help or make list to find out what the commands are

# TODO -- break out local make commands into a Makefile-local and
#   include into this one: https://www.gnu.org/software/make/manual/html_node/Include.html


VERSION_FILE=VERSION
VERSION=`cat $(VERSION_FILE)`

# ensures list is not mis-identified with a file of the same name
.PHONY: deploy_major deploy_minor deploy_patch livedocs
.PHONY: test list help lint run docker_push docker_quickpush docker_quickpush_plm docker_quickpush_demo

define deploy_commands
	@echo "Update CHANGELOG"
	@echo "Create Github release and attach the gem file"

	git push
	git push --tags
endef

dev_install:
	python3.6 -m venv .venv --prompt bel_api
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install --upgrade setuptools

	.venv/bin/pip install -r requirements.txt

run:
	cd app; gunicorn --config ./gunicorn_conf.py --log-config ./gunicorn_log.conf -b 0.0.0.0:8181 main:app

# deploy_major:
# 	@echo Deploying major update
# 	bumpversion major
# 	@${deploy_commands}

# deploy_minor:
# 	@echo Deploying minor update
# 	bumpversion --allow-dirty minor
# 	@${deploy_commands}

# deploy_patch:
# 	@echo Deploying patch update
# 	bumpversion --allow-dirty patch
# 	${deploy_commands}

bumpmajor:
	@echo Deploying major update
	bump2version  --allow-dirty --no-commit major

bumpminor:
	@echo Deploying minor update
	bump2version  --allow-dirty --no-commit minor

bumppatch:
	@echo Deploying patch update
	bump2version --allow-dirty --no-commit patch

bumpbuild:
	@echo Bumping build number
	bump2version --allow-dirty --no-commit build

bumprelease:
	@echo Bumping release and tagging
	bump2version --tag release
	git push
	git push --tags

docker_pushdev:
	@echo Deploying docker DEV image to dockerhub $(VERSION)
	# git checkout develop

	docker build -t belbio/belapi:dev -t belbio/belapi:$(VERSION) -f ./docker/Dockerfile.dev .
	docker push belbio/belapi:dev
	docker push belbio/belapi:$(VERSION)

	ssh thor "cd docker && docker-compose pull belapi"
	ssh thor "cd docker && docker-compose stop belapi"
	ssh thor "cd docker && docker-compose rm -f belapi"
	ssh thor "cd docker && docker-compose up -d belapi"
	@say -v Karen "Finished the BEL A P I docker deployment"

# 	ssh dev "cd docker; bash -ic dp userstore"

docker_pushprod:
	@echo Deploying docker PROD image to dockerhub $(VERSION)

# 	@if [[ $(BRANCH) != "master" ]]; then \
# 		echo 'Aborting script - please switch to master branch'; \
# 		exit 1; \
# 	fi

	@echo $(VERSION)
	@if [[ $(VERSION) = *dev* ]]; then \
		echo "Run 'make bumprelease' first to remove dev<buildnum>"; \
		exit 1; \
	fi

	docker build -t belbio/belapi:latest -t belbio/belapi:$(VERSION) -f ./docker/Dockerfile.prod .
	docker push belbio/belapi:latest
	docker push belbio/belapi:$(VERSION)


# docker_push:
# 	@echo Deploying docker image to dockerhub $(VERSION)
# 	docker build -t belbio/bel_api -t belbio/bel_api:$(VERSION) -f docker/Dockerfile-bel_api-image .
# 	docker push belbio/bel_api


# docker_quickpush:
# 	@echo Updating belbio/bel_api docker image directly to belbio server
# 	rsync -a --exclude=".*" ../bel docker
# 	docker build -t belbio/bel_api -f docker/Dockerfile-bel_api-quickpush .
# 	docker save belbio/bel_api | bzip2 | pv | ssh belbio 'bunzip2 | docker load'
# 	ssh belbio cd services; docker-compose stop belbio_api; docker-compose rm -f belbio_api; docker-compose up -d belbio_api; docker image prune -f


# docker_quickpush_demo:
# 	@echo Updating belbio/bel_api docker image directly to Demo2 BELbio server
# 	rsync -a --exclude=".*" ../bel docker
# 	docker build -t belbio/bel_api -f docker/Dockerfile-bel_api-quickpush .
# 	docker save belbio/bel_api | bzip2 | pv | ssh demo 'bunzip2 | docker load'
# #	ssh belbio cd services; docker-compose stop belbio_api; docker-compose rm -f belbio_api; docker-compose up -d belbio_api; docker image prune -f


# docker_quickpush_plm:
# 	@echo Updating belbio/bel_api docker image directly to PLM server
# 	rsync -a --exclude=".*" ../bel docker
# 	docker build -t belbio/bel_api -f docker/Dockerfile-bel_api-quickpush .
# 	docker save belbio/bel_api | bzip2 | pv | ssh plm 'bunzip2 | docker load'
# 	# ssh plm cd docker/belbio  && docker-compose stop bel_api && docker-compose rm -f bel_api && docker-compose up -d bel_api && docker image prune -f


livedocs:
	cd sphinx; sphinx-autobuild -q -p 0 --open-browser --delay 5 source build/html


tests: clean_pyc
	py.test -rs --cov=./app --cov-report html --cov-config .coveragerc -c tests/pytest.ini --color=yes --durations=10 --flakes --pep8 tests


clean_pyc:
	find . -name '*.pyc' -exec rm -r -- {} +
	find . -name '*.pyo' -exec rm -r -- {} +
	find . -name '__pycache__' -exec rm -r -- {} +


lint:
	flake8 --exclude=.tox

list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

help:
	@echo "List of commands"
	@echo "   deploy-{major|minor|patch} -- bump version and tag"
	@echo "   help -- This listing "
	@echo "   list -- Automated listing of all targets"


# # From https://github.com/autoferrit/docker-gunicorn-examples/blob/master/falcon/Makefile
# NAMESPACE=skiftcreative
# APP=falcon

# build:
# 	docker build -t ${NAMESPACE}/${APP} .
# run:
# 	docker run --name=${APP} --detach=true -p 5000:5000 ${NAMESPACE}/${APP}
# clean:
# 	docker stop ${APP} && docker rm ${APP}
# reset: clean
# 	docker rmi ${NAMESPACE}/${APP}
# interactive:
# 	docker run --rm --interactive --tty --name=${APP} ${NAMESPACE}/${APP} bash
# push:
# 	docker push ${NAMESPACE}/${APP}
