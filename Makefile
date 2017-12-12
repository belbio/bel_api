# Run make help or make list to find out what the commands are


# ensures list is not mis-identified with a file of the same name
.PHONY: deploy-major deploy-minor deploy-path update_ebnf update_parsers
.PHONY: docs test list help lint run


define deploy_commands
	@echo "Update CHANGELOG"
	@echo "Create Github release and attach the gem file"

	git push
	git push --tags
endef


run:
	cd api; gunicorn --config ./gunicorn.conf --log-config ./gunicorn_log.conf -b 0.0.0.0:8181 app:api

deploy-major: make_html
	@echo Deploying major update
	bumpversion major
	@${deploy_commands}

deploy-minor: make_html
	@echo Deploying minor update
	bumpversion minor
	@${deploy_commands}

deploy-patch: make_html
	@echo Deploying patch update
	bumpversion --allow-dirty patch
	${deploy_commands}


update_ebnf:
	./bin/yaml_to_ebnf.py


update_parsers: update_ebnf
	./bin/ebnf_to_parsers.py


make_html:
	cd make_docs/sphinx; make html

docs: make_html
	cp -r make_docs/sphinx/build/html/* docs
	cp -r make_docs/openapi docs
	cp -r make_docs/images docs
	cp make_docs/CNAME docs
	cp make_docs/belbio_api.yaml docs


livehtml:
	cd make_docs/sphinx; sphinx-autobuild -q -p 0 --open-browser --delay 5 source build/html

test:
	bin/runtests.sh


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
