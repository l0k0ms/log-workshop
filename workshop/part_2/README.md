# Workshop part 2

## Installation

1. If the agent from part 1 is still running, stop it with the [following command][4]: `sudo service datadog-agent stop`

2. Go in `/vagrant/workshop/part_2/`

3. Build the flask container: `docker-compose build`

## Step 1 : Simple flask app 
### Spawn the flask app 

Launch the first flask app:

`docker-compose up`

Try it out with one of the following command:

* `curl -X GET http://localhost:8080/think/?subject=technology`
* `curl -X GET http://localhost:8080/think/?subject=religion`
* `curl -X GET http://localhost:8080/think/?subject=war`
* `curl -X GET http://localhost:8080/think/?subject=work`
* `curl -X GET http://localhost:8080/think/?subject=music`
* `curl -X GET http://localhost:8080/think/?subject=humankind`

## Step 2 : Implement metric monitoring 
### Setup

Stop and remove all containers:

`docker-compose rm & docker-compose stop`

Add the following line to the `docker-compose.yaml` file to run the agent along side our app:

```
datadog:
    container_name: datadog_agent
    image: datadog/agent:latest
    environment:
      - DD_HOSTNAME=workshop_part_2
      - DD_API_KEY=${DD_API_KEY}
    volumes:
      - /proc/:/host/proc/:ro
      - /sys/fs/cgroup/:/host/sys/fs/cgroup:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
```

In order to avoid any launch issue, make sure that the DD agent is the last container to start by adding:

```
datadog:
  (...)
  depends_on:
        - nginx
        - api
```


In order to start metrics collection we are going to use labels on our containers ([learn more about auto-discovery in our documentation][5]):

For NGINX, according to [the NGINX documentation][6]:

```
    label:
        com.datadoghq.ad.check_names: '["nginx"]'
        com.datadoghq.ad.init_configs: '[{}]'
        com.datadoghq.ad.instances: '[{"nginx_status_url": "http://%%host%%:%%port%%/nginx_status"}]'
```

For Redis, according to [the Redis documentation][7]:

```
    label:
        com.datadoghq.ad.check_names: '["redis"]'
        com.datadoghq.ad.init_configs: '[{}]'
        com.datadoghq.ad.instances: '[{"host": "%%host%%", "port": "6379"}]'
```


Once done, re-spawn your containers and go back to your [Datadog application][]. 

`docker-compose up`

### Explore in Datadog:

Because of the check name, we can see that there are dashboard already created in your datadog application:

* [Nginx Overview][1]
* [Nginx Metrics][2]
* [Redis Overview][3]

We now have a clear state of our system and we could check if there is an issue but let's try to have more insights 

[1]: https://app.datadoghq.com/screen/integration/21/nginx---overview
[2]: https://app.datadoghq.com/dash/integration/20/nginx---metrics
[3]: https://app.datadoghq.com/screen/integration/15/redis---overview
[4]: https://docs.datadoghq.com/agent/basic_agent_usage/amazonlinux/#commands
[5]: https://docs.datadoghq.com/agent/autodiscovery/
[6]: https://docs.datadoghq.com/integrations/nginx/
[7]: https://docs.datadoghq.com/integrations/redisdb/
[8]: https://app.datadoghq.com/
[9]: https://app.datadoghq.com/logs/pipelines