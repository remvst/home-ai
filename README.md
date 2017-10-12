# Dependencies

```sh
sudo apt-get install arp-scan
```

Make `arp-scan` accessible to your user (potentially unsafe but whatever):
```sh
sudo chmod u+s $(which arp-scan)
```

Install ngrok:
```sh
# For arm systems
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.tgz
tar -zxvf ngrok-stable-linux-arm.tgz
rm ngrok-stable-linux-arm.tgz
```

PyGame dependencies:
```sh
sudo apt-get install libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev
sudo apt-get install libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev
```

OpenCV dependencies (not sure if necessary):
```sh
sudo apt-get install libopencv-dev python-opencv
```

Install Python Dependencies:
```sh
pip install -r requirements.txt
```
