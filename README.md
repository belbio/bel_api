# BEL API

The BEL API provides a REST API for the BEL Language and platform services
for using the BEL Language and BEL Content.

Functionality provided:

* BEL language parsing and validation
* BEL Nanopub management and validation
* BEL Edge creation from BEL Nanopubs
* BEL EdgeStore services

## Installation for Development

The following bash command will do the following:

* check for the docker, docker-compose commands
* git clone or git pull depending on if 'bel_api' directory exists
* download the needed datasets from datasets.openbel.org
* provide commands to start the docker containers

    bash <(curl -s https://raw.githubusercontent.com/belbio/bel_api/master/bin/install.sh)


###  Post install script

Add hostnames to /etc/hosts (unix'ish machines) or /windows/system32/drivers/etc/hosts (Windows)

    127.0.0.1 belapi.test
    127.0.0.1 kibana.belapi.test
    127.0.0.1 swagger_ui.belapi.test
    127.0.0.1 swagger_edit.belapi.test
    127.0.0.1 arangodb.belapi.test
    127.0.0.1 docs.belapi.test

Run following commands to start development:

    cd bel_api
    cp api/Config.yml.sample api/Config.yml
    # Edit Config.yml
    docker-compose start
    docker-compose logs -f


You should now be able to access the following services via your browser:

* API test endpoint:  http://belapi.test/simple-status
* Elasticsearch: http://localhost:9210/
* Kibana: http://kibana.belapi.test/
* Arangodb: http://arangodb.belapi.test/
* Swagger Editor: http://swagger_edit.belapi.test/#/?import=http://docs.belapi.test/docs/openapi.yaml
* Swagger UI: http://swagger_ui.belapi.test/?url=http://docs.belapi.test/docs/openapi.yaml
* Traefik:  http://localhost:8088/
* API docs: http://docs.belapi.test  (e.g. http://docs.belapi.test/docs/openapi.yaml)

You can enter this url for the Swagger/OpenAPI spec in Swagger UI

    http://docs.belapi.test/docs/openapi.yaml


## Notes for Windows users

Install Bash: https://msdn.microsoft.com/en-us/commandline/wsl/about

After installing Bash and setting up your user:

    apt-get install make

These instructions may help you get docker working with Bash for Windows:

    https://blog.jayway.com/2017/04/19/running-docker-on-bash-on-windows/
	

## Further instructions for Windows users (updated July 5, 2017)
Note: These instructions were tested for `Docker version 17.06.0-ce, build 02c1d87`.

1. Install Bash for Windows using the instructions above
2. Install Docker CE for Windows and run it:
 [https://store.docker.com/editions/community/docker-ce-desktop-windows](https://store.docker.com/editions/community/docker-ce-desktop-windows)

3. Right-click on Docker in your system tray, and click on **Settings**.
4. In the **General** tab, check **Expose daemon on tcp://localhost:2375 without TLS**.
5. In the **Shared Drives** tab, check on the local drive (usually drive C) and click **Apply**. **If this step fails to save the check for the drive letter, see below. Once resolved, continue these instructions**.
	* If your drive simply refuses to be checked, it may have to do with the sharing permissions allowed on your account (this seems to be the problem for Microsoft Azure AD accounts).
	* A workaround: 
		1. **Windows Menu > Administrative Tools > Computer Management > System Tools > Local Users and Groups > Users**
		2. On the top menu, click **Actions > New User...**. Set both username and password to "docker" (or whatever you'd like)
		3. Uncheck **User must change password at next logon** and check **Password never expires**
		4. Switch to this new account and try to access your main files in **C:/Users/your-username**, which will prompt you to authenticate with your username and password
		5. Once authenticated, switch back to your main account and try the step above once more.
		6. If issue persists, check the Docker logs by clicking on the **Diagnose and Feedback** tab and selecting **log file**, or open an issue here on Github.
6. Open a Windows command line and run `bash`. You should now be in a Bash shell
7. TODO: intermediate step to install docker inside this environment, unless installed already
8. Run `docker --version` to check your version is `>= 17.06.0`
9. If not already in the Desktop directory, `cd /mnt/{$DRIVE-LETTER}/Users/{$USERNAME}/Desktop/` where `{$DRIVE-LETTER}` is your harddrive letter and `{$USERNAME}` is your user directory. For example, mine was `/mnt/c/Users/DavidChen/Desktop/`.
10. `git clone git@github.com:belbio/bel_api.git`
11. `cd bel_api/`
12. `docker-compose start`
13. The services should now be up and ready.
14. Run `docker-compose logs -f` to view logs. Run `docker-compose stop` to stop all services.
