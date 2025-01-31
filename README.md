# SapMachine Build Infrastructure

[![REUSE status](https://api.reuse.software/badge/github.com/SAP/SapMachine-infrastructure)](https://api.reuse.software/info/github.com/SAP/SapMachine-infrastructure)

## Description

This repository contains tools, scripts and infrastructure required to build, test and maintain the [SapMachine project](https://github.com/SAP/SapMachine).

The jobs run on our [Jenkins](https://ci.sapmachine.io/) installation.

Mercurial repos are imported to branches **jdk/jdk** and **jdk/jdk10**.
Every few hours, we poll the upstream mercurial repositories and add new changes and tags ([*update-pipeline* on jenkins]( https://ci.sapmachine.io/view/repository-update/job/update-pipeline/)).

The [SapMachine Github Repository](https://github.com/SAP/SapMachine) is organized into the following branches:

*  **jdk/jdk** and **jdk/jdk10** are mirrors of the corresponding mercurial repos.
* **sapmachine10**: **jdk/jdk10** + our changes.
* **sapmachine**: **jdk/jdk** + our changes.
* **sapmachine10-alpine**: **sapmachine10** + alpine changes.
* **sapmachine-alpine**: **sapmachine** + alpine changes.

We cherry-pick our changes between sapmachine and sapmachine10.
We merge **jdk/jdk10** and **jdk/jdk** with new build tags.
The job *check-tag-pipeline*, polls these branches for new tags, opens pull requests and starts validation jobs.
Merge is triggered manually, after reviewing test and build results and resolving conflicts if needed.

Build-jobs run in docker containers to have a reproducible build environment.
Different build-jobs use the same Pipeline with different parameters.
Build jobs start test jobs. However, we don't use the result of the tests as indicator of a failure of the build job, as some failures have to be considered a *normal*. Some tests are shaky, other failure address open issues that will be fixed with the next build. However, we should compare our results to the results reported here: http://download.java.net/openjdk/testresults/10/testresults.html

## Requirements

### Jenkins Installation
We run the jobs on a jenkins installation with one server and two clients.
As most of the jobs run in docker containers, docker must be installed on the client machines.

### Access to SapMachine Repository
Some of the jobs need push access to the [SapMachine repository](https://github.com/SAP/SapMachine). It is possible to work with a fork of this repository. The credentials have to be configured in Jenkins.

## Installation
After installing jenkins, one pipeline job has to be configured that runs the Pipeline [jenkins-restore-pipeline](jenkins-restore-pipeline/Jenkinsfile). This jobs imports the whole jenkins configuration. After running this job, the configuration has to be reloaded.
To get all the jobs to function, missing credentials have to be added. Depending on the jenkins installation, some missing plugins have to be installed.
If working with a forked SapMachine repository, the repository URL in most of the Jenkinsfiles has to be changed accordingly.

## Known Issues

There are no known issues.

## How to Obtain Support

This project is provided as is.

## License

Copyright 2017-2021 SAP SE or an SAP affiliate company and SapMachine-infrastructure contributors. Please see our [LICENSE](LICENSE) for copyright and license information. Detailed information including third-party components and their licensing/copyright information is available [via the REUSE tool](https://api.reuse.software/info/github.com/SAP/SapMachine-infrastructure).
