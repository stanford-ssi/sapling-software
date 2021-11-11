# Setup Google Corral and connect to Stanford Wifi

The next handful of steps can be found: [https://coral.ai/docs/dev-board/get-started/#flash-the-board](https://coral.ai/docs/dev-board/get-started/#flash-the-board)

![Untitled](Setup%20Google%20Corral%20and%20connect%20to%20Stanford%20Wifi%20140eb8b097bc4af79d6f38599b76b8e3/Untitled.png)

![Untitled](Setup%20Google%20Corral%20and%20connect%20to%20Stanford%20Wifi%20140eb8b097bc4af79d6f38599b76b8e3/Untitled%201.png)

![Untitled](Setup%20Google%20Corral%20and%20connect%20to%20Stanford%20Wifi%20140eb8b097bc4af79d6f38599b76b8e3/Untitled%202.png)

![Untitled](Setup%20Google%20Corral%20and%20connect%20to%20Stanford%20Wifi%20140eb8b097bc4af79d6f38599b76b8e3/Untitled%203.png)

[https://coral.ai/docs/dev-board/reflash/#flash-a-new-board](https://coral.ai/docs/dev-board/reflash/#flash-a-new-board)

### At this point you should be able to serial into the board. On linux that takes the form of:

```jsx
screen /dev/ttyUSB0 115200
```

The username and password are both "mendel"

## Register on Stanford network

1. Find your hardware address by typing ip address. The hardware address is listed below wlan0. 

![Untitled](Setup%20Google%20Corral%20and%20connect%20to%20Stanford%20Wifi%20140eb8b097bc4af79d6f38599b76b8e3/Untitled%204.png)

1. [https://iprequest.stanford.edu/iprequest/](https://iprequest.stanford.edu/iprequest/)
2. Follow the on-screen instructions to add another device:
    - **First page:** Device Type: Other, Operating System: Linux, Hardware Address: put Pi's MAC address
    - **Second page:** Make and model: Other PC, Hardware Addresses Wired: delete what's there, Hardware Addresses Wireless: put Pi's MAC address
3. call sudo reboot on mendel

![Untitled](Setup%20Google%20Corral%20and%20connect%20to%20Stanford%20Wifi%20140eb8b097bc4af79d6f38599b76b8e3/Untitled%205.png)

1. try ping [www.google](http://www.google).com on reboot

In order to run an example model you should be able to follow this tutorial

[https://coral.ai/docs/accelerator/get-started/#3-run-a-model-on-the-edge-tpu](https://coral.ai/docs/accelerator/get-started/#3-run-a-model-on-the-edge-tpu)