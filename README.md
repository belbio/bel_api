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

## Related projects

* OpenBEL, http://openbel.org
* PyBEL, http://pybel.readthedocs.io/en/latest/

## Contributors

William Hayes, whayes@adsworks.com, Organization Maintainer
David Chen, dchen@adsworks.com


## Further instructions for Windows users (updated July 5, 2017)
Note: These instructions were tested for `Docker version 17.05.0-ce, build 89658be` and `docker-compose version 1.14.0, build c7bdf9e`.

0. Install Bash for Windows using the instructions above
0. Install Docker CE for Windows and run it:
 [https://store.docker.com/editions/community/docker-ce-desktop-windows](https://store.docker.com/editions/community/docker-ce-desktop-windows)

0. Right-click on Docker in your system tray, and click on **Settings**.
0. In the **General** tab, check **Expose daemon on tcp://localhost:2375 without TLS**.
0. In the **Shared Drives** tab, check on the local drive (usually drive C) and click **Apply**. If the settings are not saved after clicking apply, see below. Else, continue.
	* If your drive simply refuses to be checked, it may have to do with the sharing permissions allowed on your account (this seems to be the problem for Microsoft Azure AD accounts).
	* A workaround: 
		* **Windows Menu > Administrative Tools > Computer Management > System Tools > Local Users and Groups > Users**
		* On the top menu, click **Actions > New User...**. Set both username and password to "docker" (or whatever you'd like)
		* Uncheck **User must change password at next logon** and check **Password never expires**
		* Switch to this new account and try to access your main files in **C:/Users/your-username**, which will prompt you to authenticate with your username and password
		* Once authenticated, switch back to your main account (do not log out of the docker account) and try the step above **but using the credentials of the new account** (see image below):
		
		<br>
		<img src="\misc\imgs\docker-share.jpg" style="width:100%;" />
		<br>
		
		* If issue persists, check the Docker logs by clicking on the **Diagnose and Feedback** tab and selecting **log file**, or open an issue here on Github
0. Open a Windows command line and run `bash` - you should now be in a Bash shell
0. Elevate permission to install the newest version of Docker by running `sudo chown -R {$USERNAME} /usr/local/bin` and replace `{$USERNAME}` with your username
0. Install Docker 17.05.0 using `curl -fsSLO https://get.docker.com/builds/Linux/x86_64/docker-17.05.0-ce.tgz && tar --strip-components=1 -xvzf docker-17.05.0-ce.tgz -C /usr/local/bin`
0. Run `docker --version` to check your version is `>= 17.05.0` after the above installation
0. If not already in the Desktop directory, `cd /mnt/{$DRIVE-LETTER}/Users/{$USERNAME}/Desktop/`. For example, mine was `/mnt/c/Users/DavidChen/Desktop/`
0. `git clone git@github.com:belbio/bel_api.git`
0. `cd bel_api/`
0. `cp api/Config.yml.sample api/Config.yml` and edit Config.yml if necessary.
0. `docker-compose start`
0. The services should now be up and ready.
0. Run `docker-compose logs -f` to view logs. Run `docker-compose stop` to stop all services.

