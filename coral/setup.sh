# set up virtual environment
sudo apt-get update
sudo apt-get -y install python3-venv
sudo python3 -m venv venv
source venv/bin/activate
pip install requirements.txt

# install non-python requirements
sudo apt-get install jpegoptim

# install service
sudo cp /home/mendel/sapling-software/coral/services/command_handler.service /lib/systemd/system/sapling_coral_command_handler.service
sudo systemctl daemon-reload
sudo systemctl start sapling_coral_command_handler


