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
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
rm ngrok-stable-linux-amd64.zip
```

Install Python Dependencies:
```sh
pip install -r requirements.txt
```
