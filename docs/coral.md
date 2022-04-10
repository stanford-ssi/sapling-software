## Coral Side

- Ingestion loop that waits for commands from UART and queues the tasks up
- Dispatch loop that runs jobs from the queue
- Linux Service that keeps the python script running after reboot. Reference: <https://www.digitalocean.com/community/tutorials/how-to-configure-a-linux-service-to-start-automatically-after-a-crash-or-reboot-part-1-practical-examples>