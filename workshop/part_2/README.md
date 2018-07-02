# Workshop part 2

## Installation

1. If the agent from part 1 is still running, stop it with the [following command][4]: `sudo service datadog-agent stop`

2. Go in `/vagrant/workshop/part_2/`

3. Build the flask container: `docker-compose build`

## Step 1 : Simple flask app 

1. Go in `workshop/part_2`
2. Launch the first flask app: `docker-compose build && docker-compose up`

3. Try it out with one of the following command:

* `curl -X GET http://localhost:8080/think/?subject=technology`
* `curl -X GET http://localhost:8080/think/?subject=religion`
* `curl -X GET http://localhost:8080/think/?subject=war`
* `curl -X GET http://localhost:8080/think/?subject=work`
* `curl -X GET http://localhost:8080/think/?subject=music`
* `curl -X GET http://localhost:8080/think/?subject=humankind`

3. Stop the application when you are over: `docker-compose stop && docker-compose rm`

4. Switch to the branch `part_2/step_2` to start next step:

`git checkout part_2/step_2`

[1]: https://app.datadoghq.com/screen/integration/21/nginx---overview
[2]: https://app.datadoghq.com/dash/integration/20/nginx---metrics
[3]: https://app.datadoghq.com/screen/integration/15/redis---overview
[4]: https://docs.datadoghq.com/agent/basic_agent_usage/amazonlinux/#commands
[5]: https://docs.datadoghq.com/agent/autodiscovery/
[6]: https://docs.datadoghq.com/integrations/nginx/
[7]: https://docs.datadoghq.com/integrations/redisdb/
[8]: https://app.datadoghq.com/
[9]: https://app.datadoghq.com/logs/pipelines