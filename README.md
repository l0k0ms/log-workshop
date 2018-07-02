# log-workshop

This workshop aims to demonstrate the Datadog Log-management solution.
Part 1 is around how to collect different logs formats from different sources and how to unify them on the datadog side in order to leverage the most value out of it.
Part 2 is a simple Flask application to demonstrate how Datadog Log management solution include it-self in the 100% observability logic. The Flask app is a fork from the [previous workshop of Vlad][4] on the APM distributed feature.

## Setup

You need the following tools for this workshop:

* [Vagrant][1]
* [A Datadog platform][2] and its [associated API key][3]

### Installation

1. Run `vagrant up`
2. Connect to your Workshop vagrant box: `vagrant ssh`
3. Export your [Datadog API Key][3] `export DD_API_KEY=<DD_API_KEY>`

## Part 1

Go in [workshop/part_1](/workshop/part_1) and follow the `README.md` instructions.

## Part 2

Go in [workshop/part_2](/workshop/part_2) and follow the `README.md` instructions.

[1]: https://www.vagrantup.com/downloads.html
[2]: https://app.datadoghq.com/
[3]: https://app.datadoghq.com/account/settings#api
[4]: https://github.com/vlad-mh/pyconuk-2017
[5]: https://docs.datadoghq.com/logs/log_collection/
[6]: https://app.datadoghq.com/logs
[7]: https://docs.datadoghq.com/logs/processing/