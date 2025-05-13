# mqtt_presence



## Start / Install

### As binary
Download and run executable created by Installer

    mqtt-presence
    mqtt-presence.exe


### As module in python:
Install:

    pip install mqtt-presence

Start
Run:

    mqtt-presence

Or use python module:

    python -m mqtt_presence.main



### Start Container

Image not yet published.

        docker-compose up -d

        docker run -d -p 5000:5000 --name mqtt_presence mqtt_presence
        
        If  GPIO is required  (only  Raspberry Pi):
        docker run --privileged -d -p 5000:5000 --name mqtt_presence mqtt_presence


## Virtuell environment

### create environment
    python -m venv venv

### Activate
    .\venv\Scripts\activate      # Windows
    source venv/bin/activate     # Linux

### Deactivate
    source venv/bin/deactivate
    deactivate     ??



# Create deployments


## Installer

    pyinstaller --onefile --name mqtt-presence mqtt_presence/main.py
    python -m PyInstaller --onefile --name mqtt-presence mqtt_presence/main.py



## Packet
    python -m build
    twine upload dist/*


## Container

### Build container:
    docker compose build
    docker compose up --build


### Delete image/existing container
    docker container rm mqtt-presence
    docker image rm mqtt-presence


### Save/load image:
    docker save -o mqtt-presence.tar mqtt-presence
    docker load -i ./mqtt-presence.tar

