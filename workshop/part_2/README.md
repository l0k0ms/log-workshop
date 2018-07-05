# Workshop part 2

## Installation

1. If the agent from part 1 is still running, stop it with the [following command][4]: `sudo service datadog-agent stop`

2. Go in `/vagrant/workshop/part_2/`

3. Export your [Datadog API Key][14] `export DD_API_KEY=<DD_API_KEY>`

## Step 1: Simple flask app 

1. Go in `workshop/part_2`

2. Launch the first flask application: `docker-compose build && docker-compose up`

3. Try it out with one of the following command:

* `curl -X GET http://localhost:8080/think/?subject=technology`
* `curl -X GET http://localhost:8080/think/?subject=religion`
* `curl -X GET http://localhost:8080/think/?subject=war`
* `curl -X GET http://localhost:8080/think/?subject=work`
* `curl -X GET http://localhost:8080/think/?subject=music`
* `curl -X GET http://localhost:8080/think/?subject=humankind`

3. Stop the application when you are over: `docker-compose stop && docker-compose rm`

## Step 2 : Implement metric monitoring 
### Setup

1. Stop and remove all running containers: `docker-compose stop & docker-compose rm`

2. Add the following lines to the `docker-compose.yaml` file to run the agent along side our application ([learn more on docker Datadog Agent setup in the documentation][15]):

```yaml
datadog:
    container_name: datadog_agent
    image: datadog/agent:latest
    environment:
      - DD_HOSTNAME=datadog
      - DD_API_KEY=${DD_API_KEY}
    volumes:
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup/:/host/sys/fs/cgroup:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

In order to avoid any launch issue, make sure that the Datadog Agent is the last container to start by adding:

```
datadog:
  (...)
  depends_on:
        - nginx
        - api
```


In order to start metrics collection we are going to use labels on our containers ([learn more about auto-discovery in our documentation][5]):

For NGINX, according to [the Datadog-NGINX documentation][6] use the following labels:

```
nginx:
    (...)
    label:
        com.datadoghq.ad.check_names: '["nginx"]'
        com.datadoghq.ad.init_configs: '[{}]'
        com.datadoghq.ad.instances: '[{"nginx_status_url": "http://%%host%%:%%port%%/nginx_status"}]'
```

For Redis, according to [the Datadog-Redis documentation][7] use the following labels:

```
redis:
    (...)
    label:
        com.datadoghq.ad.check_names: '["redis"]'
        com.datadoghq.ad.init_configs: '[{}]'
        com.datadoghq.ad.instances: '[{"host": "%%host%%", "port": "6379"}]'
```


Once done, re-spawn your containers (`docker-compose up`) and go back to your [Datadog application][].

### Explore in Datadog:

Because of the check name that was just set up, Integration dashboard are created in your Datadog application:

* [Nginx Overview][1]
* [Nginx Metrics][2]
* [Redis Overview][3]

They give you a clear state of the running system  but don't show its behavior nor why it's behaving this way/

## Step 3: Implement Trace monitoring 

The flask application is already instrumented with traces. To configure the Datadog agent to gather traces in addition of metrics already collected and send everything to Datadog:

1. Add the following environment variable to our `datadog` container:

```
datadog:
  environment:
    (...)
    - DD_APM_ENABLED=true
```

2. Start the application:

```
docker-compose up
```

3. Go back to the [Datadog application][10] to see some traces flowing in it for the `redis`, `thinker-api`, `thinker-microservice` service.

## Step 4: Implement log monitoring
### Basic log collection

Metrics and traces are neow collected but let's collect the last medium.

The application is already emitting some logs let's catch them with our datadog container:

Add the following configuration in your `docker-compose.yml` for the Datadog Agent in-order to gather logs from your application:

```
datadog:
  environment:
    (...)
    - DD_LOGS_ENABLED=true
    - DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL=true
  volume:
    (...)
    - /opt/datadog-agent/run:/opt/datadog-agent/run:rw
    - /proc/mounts:/host/proc/mounts:ro
```

[Refer to the Datadog Agent log collection documentation to learn more][16]. 

Let's restart everything and start see our logs in our DD app:

```
docker-compose stop && docker-compose rm && docker-compose up
```

As you can see we can see our logs flowing in but they are not parsed yet
Check the info bubble on your logs to see which one are not parsed yet.

Datadog have a range of supported integration, and those are enabled according to the service-attributes value.

### Integration log collection 

In order to enable integrations pipeline, pass the source name as a label:

Enhance your docker compose with the following labels

```
redis:
  (...)
  labels:
    (...)
    com.datadoghq.ad.logs: '[{"source": "redis", "service": "docker-redis"}]'
nginx:
  (...)
  label:
    (...)
    com.datadoghq.ad.logs: '[{"source": "nginx", "service": "docker-nginx"}]'
```

restart everything and watch what is happening:

```
docker-compose stop && docker-compose rm && docker-compose up
```

Check if [the integration pipelines][9] are created and are parsing the logs.

### Binding logs traces and metrics

Tags are what is allowing us to bind metrics / traces / logs.

Let's add log tag to the containers `thinker-api` and `thinker-microservice` in order to be able to bind the traces and the log together

Enhance the `docker-compose.yml` file with the following labels:

```
api:
  (...)
  labels:
    (...)
    com.datadoghq.ad.logs: '[{"source": "webapp", "service": "thinker-api"}]'

thinker:
  (...)
  labels:
    (...)
    com.datadoghq.ad.logs: '[{"source": "webapp", "service": "thinker-microservice"}]'
```

Restart everything and watch what is happening:

```
docker-compose stop && docker-compose rm && docker-compose up
```

## (Bonus) Adding new logs

The log collection and binding to the APM is now over, let's update the application with a new log and see what is happening

in `thinker.py` in the `think()` function add a dummy log: 

```
    redis_client.incr('hits')
    aiohttp_logger.info('Number of hits is {}' .format(redis_client.get('hits').decode('utf-8')))
```

It just count the amount of hits and store the number in Redis itself

Restart everything and watch what is happening:

```
docker-compose stop && docker-compose rm && docker-compose up
```

logs flowing have automatically the right tags now, configuration is over.

Final question parse this new log, add the `hits_number` as a facet, create a monitor on its derivative and then launch `stress_test.sh` 

[1]: https://app.datadoghq.com/screen/integration/21/nginx---overview
[2]: https://app.datadoghq.com/dash/integration/20/nginx---metrics
[3]: https://app.datadoghq.com/screen/integration/15/redis---overview
[4]: https://docs.datadoghq.com/agent/basic_agent_usage/amazonlinux/#commands
[5]: https://docs.datadoghq.com/agent/autodiscovery/
[6]: https://docs.datadoghq.com/integrations/nginx/
[7]: https://docs.datadoghq.com/integrations/redisdb/
[8]: https://app.datadoghq.com/
[9]: https://app.datadoghq.com/logs/pipelines
[10]: https://app.datadoghq.com/apm/home?env=none
[14]: https://app.datadoghq.com/account/settings#api
[15]: https://docs.datadoghq.com/agent/basic_agent_usage/docker/
[16]: https://docs.datadoghq.com/logs/log_collection/docker/