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

Install Python Dependencies:
```sh
pip install -r requirements.txt
```
