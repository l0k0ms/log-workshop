# Workshop Exercise 1: Reaching 100% visibility with metrics traces and logs

This first exercise is a simple Flask application composed with NGINX, an API, a micro-service and Redis. The Flask application is a fork from the [Vlad's previous workshop](https://github.com/vlad-mh/pyconuk-2017) on the APM distributed feature, allowing us to work with an already APM instrumented application in order to focus on the log collection and usage part.

## Installation

In order to perform this exercise, we must spawn a vagrant VM. This allows us to work in a controlled environment, abstracting all potential OS related issues and making this work flow repeatable.

The OS distribution and version used for this exercise is `bento/ubuntu-16.04`. 

0. Go inside the `log-workshop/` folder that you [downloaded from Github](https://github.com/l0k0ms/log-workshop).

1. Start your vagrant VM:
  
    `vagrant up`

2. Connect to your Workshop vagrant box:
  
    `vagrant ssh`

3. Export your [Datadog API Key](https://app.datadoghq.com/account/settings#api):

    `export DD_API_KEY=<DD_API_KEY>`

     We export the Datadog API key in our current shell in order to be able to call it at any time with `$DD_API_KEY`. 

4. Go in the `/vagrant/workshop/exercise_1/` folder to start the exercise:

    `cd /vagrant/workshop/exercise_1/`

## Trying the application

Let's start this exercise by launching the application and testing it.
The whole application is managed with `docker-compose` in order to simplify its usage.

1. Launch the first Flask application: 

    `docker-compose up --build -d`

2. Try it out with one of the following command:

  * `curl -X GET http://localhost:8080/think/?subject=technology`
  * `curl -X GET http://localhost:8080/think/?subject=religion`
  * `curl -X GET http://localhost:8080/think/?subject=war`
  * `curl -X GET http://localhost:8080/think/?subject=work`
  * `curl -X GET http://localhost:8080/think/?subject=music`
  * `curl -X GET http://localhost:8080/think/?subject=humankind`
  
  Either test this in your vagrant box or on your computer directly. The `8080` port is bound between the vagrant host and guest. 
  
  If curl is not available on your machine, try to access `http://localhost:8080/think/?subject=technology` in your favorite browser.

## Step 1: Gathering logs.
### Installation 

If not done already, go in your Datadog application and [enable the Log-management feature](https://app.datadoghq.com/logs/).

### Setup

Start by stopping and removing all current running containers: 

    docker-compose stop && docker-compose rm -f

Since we are working in a containerized environment, the Datadog Agent should run as a container alongside the other containers. All configuration should then happen only through environment variables, volumes, and docker labels. [Learn more about docker Datadog Agent setup in the documentation](https://docs.datadoghq.com/agent/basic_agent_usage/docker/).

To start gathering the application logs, add the following lines to the `docker-compose.yaml` file in this folder to run the Agent as a container and start gathering some logs:

```
datadog:
  environment:
    (...)
    - DD_LOGS_ENABLED=true
    - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
  volume:
    (...)
    - /opt/datadog-agent/run:/opt/datadog-agent/run:rw
```

| Configuration                                      | type         | Explanations                                    |
| :----                                              | :-----       | :-----                                          |
| `DD_LOGS_ENABLED=true`                             | env variable | Enable log collection                           |
| `DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true`        | env variable | Enable log collection for all containers        |
| `/opt/datadog-agent/run:/opt/datadog-agent/run:rw` | volume       | Used to store pointers on container current log |

[Refer to the Datadog Agent log collection documentation to learn more](https://docs.datadoghq.com/logs/log_collection/docker/). 

Go in your Datadog application in [`Log -> Explorer`](https://app.datadoghq.com/logs/) and check your logs flowing.

![Log Flow](/workshop/exercise_1/images/log_flow.png)

## Step 2: Exploring data in Datadog

Install the Redis and NGINX integrations on the [Datadog integration page](https://app.datadoghq.com/account/settings).

### Metrics

Thanks to the [Datadog auto-discovery feature](https://docs.datadoghq.com/agent/autodiscovery/), metrics are collected automatically from the Redis and NGINX containers. OOTB Integrations dashboards have been created in your Datadog application:

* [Nginx Overview](https://app.datadoghq.com/screen/integration/21/nginx---overview)
* [Nginx Metrics](https://app.datadoghq.com/dash/integration/20/nginx---metrics)
* [Redis Overview](https://app.datadoghq.com/screen/integration/15/redis---overview)

**Those dashboards give you a clear state of the running system but don't show its overall state or why it's behaving this way.**

### Traces

Traces are collected for the following services:

* [`redis`](https://app.datadoghq.com/apm/service/redis/redis.command)
* [`thinker-api`](https://app.datadoghq.com/apm/service/thinker-api/flask.request)
* [`thinker-microservice`](https://app.datadoghq.com/apm/service/thinker-microservice/aiohttp.request)

The application was already instrumented to emit those traces. [Refer to the Datadog documentation if you want to learn more on APM instrumentation](https://docs.datadoghq.com/tracing/)

**Those traces describe your system behavior but don't show its overall state or why it's behaving this way.**

### Logs 

[Logs are collected](https://app.datadoghq.com/logs) from all your containers but there are some issues: 

* Logs are not parsed.
* Logs are not bound to the other data types that are metrics and traces.

**Those Logs give more context on your system but don't show its overall state or why it's behaving this way.**

![log_not_parsed](/workshop/exercise_1/images/log_not_parsed.png)

## Step 2: Gathering better logs.

Logs are flowing in your Datadog application but they are not parsed, nor are they linked to the other data type.

In order to solve this issue, we are going to use two reserved attributes:

* `source`
* `service`

### Integration pipelines 

**The `source` attribute is key to enable the integration pipeline**

Datadog has a range of [Log supported integration](https://docs.datadoghq.com/integrations/#log-collection). In order to enable the Log integrations pipeline in Datadog, pass the source name as a value for the `source` attribute with a docker label.

Enhance your `docker-compose.yml` with the following labels:

For Redis, according to [the Datadog Redis documentation](https://docs.datadoghq.com/integrations/redisdb/) use the following labels:

```
redis:
  (...)
  labels:
    com.datadoghq.ad.logs: '[{"source": "redis", "service": "redis"}]'
```

For NGINX, according to [the Datadog NGINX documentation](https://docs.datadoghq.com/integrations/nginx/) use the following labels:

```
nginx:
  (...)
  labels:
    (...)
    com.datadoghq.ad.logs: '[{"source": "nginx", "service": "nginx"}]'
```

### Binding Application logs to the corresponding metrics and traces

**The `service` attribute is key for binding metrics traces and logs**.

Our application is already instrumented for APM. Let's add log tags to the containers `thinker-api` and `thinker-microservice` in order to be able to bind the traces and the log together.

Enhance the `docker-compose.yml` file with the following labels:

```
api:
  (...)
  labels:
    com.datadoghq.ad.logs: '[{"source": "webapp", "service": "thinker-api"}]'

thinker:
  (...)
  labels:
    com.datadoghq.ad.logs: '[{"source": "webapp", "service": "thinker-microservice"}]'
```

The `service` attribute values are defined upon what has been set up in our applications code:

* [For the `api` service](https://github.com/l0k0ms/log-workshop/blob/master/workshop/exercise_1/app/api.py#L16)
* [For the `thinker` service](https://github.com/l0k0ms/log-workshop/blob/master/workshop/exercise_1/app/thinker.py#L73) 

### Testing the new configuration

Restart everything:

```
docker-compose stop && docker-compose rm -f && docker-compose up -d
```

Thanks to the `source` attribute, [Integration pipelines](https://app.datadoghq.com/logs/pipelines) have been created within your Datadog application and are parsing your application logs from Redis and NGINX.
If you want to learn more about log parsing and what's the story behind pipelines, feel free to refer to the [second exercise of this workshop][/workshop/exercise_2].

![integration_pipelines](/workshop/exercise_1/images/integration_pipelines.png)

Thanks to the `service` attribute we are now able to switch from metrics to traces to logs.

## Bonus - Enhancing our logs
This section should be done after completing the [second exercise](/workshop/exercise_2) of this workshop.

## Adding new application logs
Update the application with a new log and see what is happening

In `thinker.py`, in the `think()`, function add a dummy log: 

```
redis_client.incr('hits')
aiohttp_logger.info('Number of hits is {}' .format(redis_client.get('hits').decode('utf-8')))
```

It just counts the number of hits and stores the number in Redis itself.
Restart everything and watch what is happening:

```
docker-compose stop && docker-compose rm -f && docker-compose up -d
```

Logs flowing automatically have the right tags now. Configuration is over.

After completing Exercise 2, parse this new log, add the `hits_number` as a facet, create a monitor on its derivative, and then launch `stress_test.sh` 