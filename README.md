# viscosity-calculator

TODO: Description

## Set up development environment

### Install dependencies

```
pip install -r requirements.txt
```

### How to run locally for testing

Start a local Dash server on `localhost:8050` by submitting

```
python app.py
```

The app can be accessed in the browser at `http://localhost:8050/viscosity-calculator/`.

### Install Docker

Go to [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/) and install
the Docker desktop.


## Preparation for deployment

Before deployment to the server, make sure that the application is runnable
in a Docker container. In order to check that, perform the following steps
on your machine.

1. Build Docker container

    ```
    docker build -t viscosity-calculator .
    ```

2. Run the container

    ```
    docker run -p 8050:8050 viscosity-calculator
    ```

3. Open a browser and load the following address. This should start the app.

    ```
    http://localhost:8050/viscosity-calculator/
    ```
    

4. Stop the container. First look up the ID of the running container:
    
    ```
    >> docker ps
    CONTAINER ID        IMAGE                  COMMAND             CREATED             STATUS              PORTS                    NAMES
    bd8bb0decd02        viscosity-calculator   "python3 app.py"    11 minutes ago      Up 11 minutes       0.0.0.0:8050->8050/tcp   gallant_poitras
    ```
    
    The container ID and name will be different in your case. 
    
    Then stop the container:
    
    ```
    docker stop bd8bb0decd02
    ```

