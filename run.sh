#/bin/bash
echo "Building the docker image"

docker build -t test .

echo "Docker image successfully build"
echo "Starting clients"

docker run -d -p 4000:80 --name client1 --hostname 4000 test
docker run -d -p 4001:80 --name client2 --hostname 4001 test
docker run -d -p 4002:80 --name client3 --hostname 4002 test
docker run -d -p 4003:80 --name client4 --hostname 4003 test
docker run -d -p 4004:80 --name client5 --hostname 4004 test

echo "Successfully started 5 clients"
echo "Terminating and removing clients"

docker stop client1
docker stop client2
docker stop client3
docker stop client4
docker stop client5

docker rm client1
docker rm client2
docker rm client3
docker rm client4
docker rm client5

echo "Clients successfully terminated and removed"

echo "Retrieving docker machine ip"
docker_machine_ip="$(docker-machine ip)"
echo "Docker machine ip is: ${docker_machine_ip}"