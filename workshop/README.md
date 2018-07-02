# log-workshop
## Overview 

A simple Flask app to demonstrate Datadog Log management solution
This is inspired from the [previous work of Vlad][4] on the APM distributed feature.

## Setup

You need the following tools for this workshop:

* [Vagrant][1]
* [A Datadog platform][2] and its [associated API key][3]

### Installation

1. Run `vagrant up`
2. Connect to your Workshop vagrant box: `vagrant ssh`
3. Export your [Datadog API Key][3] `export DD_API_KEY=<DD_API_KEY>`

## Part 1

Go in [/part_1](/part_1) and follow the `README.md` instructions.

## Part 2

Go in [/part_2](/part_2) and follow the `README.md` instructions.

[1]: https://www.vagrantup.com/downloads.html
[2]: https://app.datadoghq.com/
[3]: https://app.datadoghq.com/account/settings#api
[4]: https://github.com/vlad-mh/pyconuk-2017
[5]: https://docs.datadoghq.com/logs/log_collection/
[6]: https://app.datadoghq.com/logs
[7]: https://docs.datadoghq.com/logs/processing/