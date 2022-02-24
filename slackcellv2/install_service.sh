# create slackcell service
sudo cp slackcell.service /lib/systemd/system/slackcell.service
sudo chmod 644 /lib/systemd/system/slackcell.service
sudo systemctl daemon-reload
sudo systemctl enable slackcell.service
sudo reboot