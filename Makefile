USER := baroolescientifique # my docker hub user
PROJECT := test
VERSION := 2.0.0
REMOTE := $(USER)/$(PROJECT):$(VERSION)

ISSTARTED := $(shell sudo docker ps -a -f name=my-rabbit --format='{{.Names}}' | wc -l )

# builds docker image
docker-build:
	sudo docker build -f Dockerfile -t $(REMOTE) .

## cleans docker image
clean:
	sudo docker image rm $(REMOTE) | true

## runs container in foreground, using default args
docker-test:
	sudo docker run -it --rm $(REMOTE)

## runs container in foreground, override entrypoint to use use shell
docker-test-cli:
	sudo docker run -it --rm --entrypoint "/bin/bash" $(REMOTE)
# Run Docker
docker-run:
	sudo docker run -it --rm $(REMOTE) $(CMD)

## pushes to docker hub
docker-push:
	sudo docker push $(REMOTE)


## convenience tasks for running produer/consumer against privateIP of rmq
docker-run-server: get-rabbitmq-ip
	sudo docker run -it --rm $(REMOTE) ./server.py --host=$(RMQ) $(CMD)
docker-run-client: get-rabbitmq-ip
	sudo docker run -it --rm $(REMOTE) ./client.py --host=$(RMQ) $(CMD)

# stops rabbitmq server
stop-rabbit:
	sudo docker stop my-rabbit