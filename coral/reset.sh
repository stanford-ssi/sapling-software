sudo systemctl stop sapling_coral_command_handler
sudo cp /home/mendel/sapling-software/coral/services/command_handler.service /etc/systemd/system/sapling_coral_command_handler.service
sudo systemctl daemon-reload
sudo systemctl enable sapling_coral_command_handler
sudo systemctl start sapling_coral_command_handler

