# set up virtual environment
sudo apt-get update
sudo apt-get -y install python3-venv
sudo python3 -m venv venv
source venv/bin/activate
pip install requirements.txt

# install non-python requirements
sudo apt-get install jpegoptim

# give mendel user correct permissions
sudo useradd mendel dialout

# install service
sudo cp /home/mendel/sapling-software/coral/services/command_handler.service /lib/systemd/system/sapling_cc.service
sudo systemctl daemon-reload
sudo systemctl enable sapling_cc
sudo systemctl start sapling_cc
