# PART 1: A standalone ML Flask API

## Usage

1. Build Docker image and tag as ml-api

```
docker build . -t ml-api  
```

2. Run Docker container and map container port of 5000 to local host port of 5000 

```
docker run -p 5000:5000 -d ml-api 
```


## Testing

1. Find the IP address of your machine

```
hostname -I
```

2. Test the API endpoint with a `curl` command and example JSON payload

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
```

3. Similary, you can try and pass an invalid payload (for example using strings rather numbers), which will return a `400` bad request message

```
curl http://your_machine_ip:5000/predict -d '{"sepal_length": 'thirty', "sepal_width":0.2, "petal_length":3, "petal_width":2}' -H 'Content-Type: application/json'
```

```
{
  "error": "400 Bad Request: Failed to decode JSON object: Expecting value: line 1 column 18 (char 17)
}
```
