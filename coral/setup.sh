# set up virtual environment
sudo apt-get -y install python3-venv
sudo python3 -m venv $HOME/venv
source $HOME/venv/bin/activate
sudo pip install --user -r requirements.txt

# move code to the root folder
mv ./src/* $HOME/

# install service
sudo cp /home/mendel/sapling-software/coral/services/command_handler.service /lib/systemd/system/sapling_coral_command_handler.service
sudo systemctl daemon-reload
sudo systemctl start sapling_coral_command_handler

