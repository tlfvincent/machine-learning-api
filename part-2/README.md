
## Information
What is HAProxy?
HAProxy is a free, open source high availability solution, providing load balancing and proxying for TCP and HTTP-based applications by spreading requests across multiple servers.


## Usage

1. 

```
docker-compose up -d
```

2. Check that both containers are running

```
docker-compose ps
```

and yes they are!

```
         Name                   Command                   State                    Ports
-------------------------------------------------------------------------------------------------
part2_api_1              python3 api.py           Up                       5000/tcp
part2_loadbalancer_1     /sbin/tini --            Up                       1936/tcp, 443/tcp,
                         dockercloud- ...                                  0.0.0.0:80->80/tcp
```

At this point, this is not much different to spinning an API from a container, as only a single instance of the API exists. Nevertheless, let's test how long our API takes to process 100 requests.

3. Check that the endpoint of your API is working, first find the IP address of your machine with the command `hostname -I` nd st the API endpoint with a `curl` command and example JSON payload

```
curl http://your_machine_ip:5000/predict -d '{"sepal_length": 1, "sepal_width":0.2, "petal_length":3, "petal_width":2}' -H 'Content-Type: application/json'
```

You should get an output similar to the following:

```
{
  "prediction": {
    "Iris-setosa": 0.36363636363636365,
    "Iris-versicolor": 0.5454545454545454,
    "Iris-virginica": 0.09090909090909091
  },
  "status_code": 200
}


## Scaling your applications

```
docker-compose up -d --scale api=7
```

which gives

```
Creating part2_api_1 ...
Creating part2_api_2 ...
Creating part2_api_3 ...
Creating part2_api_4 ...
Creating part2_api_5 ...
Creating part2_api_6 ...
Creating part2_api_7 ...
Creating part2_api_1 ... done
Creating part2_api_2 ... done
Creating part2_api_3 ... done
Creating part2_api_4 ... done
Creating part2_api_5 ... done
Creating part2_api_6 ... done
Creating part2_api_7 ... done
Creating part2_loadbalancer_1 ...
Creating part2_loadbalancer_1 ... done
```

and `docker-compose ps` show now look like:

```
        Name                      Command               State                   Ports
-----------------------------------------------------------------------------------------------------
part2_api_1            python3 api.py                   Up      0.0.0.0:32768->5000/tcp
part2_api_2            python3 api.py                   Up      0.0.0.0:32769->5000/tcp
part2_api_3            python3 api.py                   Up      0.0.0.0:32772->5000/tcp
part2_api_4            python3 api.py                   Up      0.0.0.0:32770->5000/tcp
part2_api_5            python3 api.py                   Up      0.0.0.0:32771->5000/tcp
part2_api_6            python3 api.py                   Up      0.0.0.0:32774->5000/tcp
part2_api_7            python3 api.py                   Up      0.0.0.0:32773->5000/tcp
part2_loadbalancer_1   /sbin/tini -- dockercloud- ...   Up      1936/tcp, 443/tcp, 0.0.0.0:80->80/tcp
```



##

Using the command `curl http://159.203.105.158`, you we can hit our API endpoint and see how the container id changes for each request:

```
for request in `seq 1 10`; do curl http://159.203.105.158; done
```

```
Hello World! My Hostname is: 49b962f57208
Hello World! My Hostname is: 5735a77067fd
Hello World! My Hostname is: a981f1027579
Hello World! My Hostname is: 3b7819972924
Hello World! My Hostname is: b3c51f7d843b
Hello World! My Hostname is: 8b40b442cfa1
Hello World! My Hostname is: f5603a0c7d2b
Hello World! My Hostname is: 49b962f57208
Hello World! My Hostname is: 5735a77067fd
Hello World! My Hostname is: a981f1027579
```

docker-compose logs