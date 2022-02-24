# Hardware
- [Raspberry Pi with WiFi (only tested with PiZero)](https://de.aliexpress.com/item/1005001993063894.html?spm=a2g0o.productlist.0.0.241718cau3Jmoo&algo_pvid=ab124c88-2c89-49b1-b4b1-63a48af97898&algo_expid=ab124c88-2c89-49b1-b4b1-63a48af97898-11&btsid=2100bdf016176111740133968e8c95&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_
)
- [Load cell](https://www.aliexpress.com/item/32812001888.html?spm=a2g0s.9042311.0.0.27424c4dgwwxjk
)
- [HX711 board](https://de.aliexpress.com/item/32878181081.html?spm=a2g0s.9042311.0.0.27424c4dayNX7O
)
- [MicroSD card](https://www.ebay.de/itm/372359679358?chn=ps&mkevt=1&mkcid=28&var=641177897326
)
- [2 eye bolts](https://www.edelstahl-niro.de/ring-schraube-16mm-edelstahl-p-83.html
)
- 5V Power supply
- Cables

__Total cost: ~ 70 €__

- Optional: Connectors, LED Strip ([WS2812](https://de.aliexpress.com/item/32682015405.html?spm=a2g0s.9042311.0.0.50c14c4d5FxgiO),
 [WS2813](https://www.aliexpress.com/item/4001322411818.html?spm=a2g0o.productlist.0.0.6f8e1dd5cPWhci&algo_pvid=dc35f561-fb6a-47c2-bd78-e85539a01e37&algo_expid=dc35f561-fb6a-47c2-bd78-e85539a01e37-2&btsid=2100bdd816176233368473349e79dd&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_
))

# Tools
- Soldering iron or crimping tool if you use connectors
- Unix-Shell (Windows: [PuTTY](https://www.putty.org/) or Linux subsystem) or monitor and keyboard if you don't use a headless pi
(see next step)

# Installation
- [Prepare the headless Pi](https://desertbot.io/blog/headless-pi-zero-w-wifi-setup-windows) with [Raspian lite](https://www.raspberrypi.org/software/operating-systems/)
- Connect to pi with `ssh pi@<IP_OF_YOUR_PI>` password is `raspberry`
- Update pi and install packages. Grab a coffee, this will take a while
```
# update Raspian
sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt-get install git
sudo apt-get install python3
sudo apt-get install python3-pip
sudo apt-get install libatlas-base-dev
```
- Clone Repo `git clone git@gitlab.com:Grommi/slackcellv2.git`
- Install Python Modules
```
cd slackcellv2
sudo  python3 -m pip install -r requirements.txt
```
- Create config and save as `slackcell.cfg`. You can copy `example.cfg` for a start.

# Connection
 
[Pi Pinout](https://www.raspberrypi.org/documentation/usage/gpio/)

## HX711

| Loadcell cable | HX711 pin |
|---|---|
| Red | E+ |
| Black | E- |
| White | A- |
| Green | A+ |

| HX711 pin | Pi pin |
| --- | --- |
| VCC | 5V |
| SCK | GPIO23 |
| DT | GPIO22 |
| GND | GND |

SCK and DT can be connected to any GPIO pin but you need to change the pins in `slackcell.cfg` accordingly.

## LEDs

| LED pin | Pi pin |
| --- | --- |
| VCC | 5V power supply |
| DIN | GPIO18 |
| GND | GND pi and power supply|



# Calibration
The load cell can be calibrated with help of the slack cell web interface

# Start SlackCellv2
- Start loadcell and server with `sudo python3 run.py`.
- Open `http://<IP_OF_YOUR_PI>:8800` in your browser
- One time calibration with a known weight via browser

# Installing Comitup
> The comitup service, which automatically connects to any previously established Wifi Access Points, if possible. Otherwise, it will create a stand-alone Access Point with the name (SSID) 'comitup-<nnn>', where '<nnn>' is a unique, persistent number.

[Installation guide](https://github.com/davesteele/comitup/wiki/Installing-Comitup)

# Development
In case your developing without a Raspberry Pi install the rpi-ws281x-mock module
