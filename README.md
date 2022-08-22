# 0022-Dissertation

This is the dissertation project for CASA Connected Environment. 

<img src='https://github.com/xxxcrttt/0022-Dissertation/blob/main/figure/9641660913096_.pic.jpg' height=300 center=/align>

## Overview
This project uses a low-cost infrared imaging camera **FLIR Lepton**. It deploys the lightweight neural network, **MobileNet** to a tiny single-board computer **Raspberry Pi**. The dataset and model was trained on Edge Inpulse, ([Edge Impulse](https://studio.edgeimpulse.com/public/112844/latest)). By evaluating different model experiments, this project achieved an accuracy of 96.2%, and can successfully distinguish up to 7 people. 

FLIR Lepton: 

<img src='https://github.com/xxxcrttt/0022-Dissertation/blob/main/figure/dev%20kiy.jpeg' height=300 center=/align>

process: can be found [here](https://github.com/xxxcrttt/0022-Dissertation/blob/main/figure/process4%20(1).png)


circuit diagram:

<img src='https://github.com/xxxcrttt/0022-Dissertation/blob/main/figure/circuit.jpg' height=500 centre=/align>

## Setup

### Connect Edge Impulse with Raspberry Pi
Follow the installation guidance of  [Linux Python SDK](https://docs.edgeimpulse.com/docs/edge-impulse-for-linux/linux-python-sdk), and connect the Raspberry Pi with Edge Impulse: [Raspberry Pi](https://docs.edgeimpulse.com/docs/development-platforms/officially-supported-cpu-gpu-targets/raspberry-pi-4).


### Required to download the following libraries

1. ```opencv``` and ```numpy``` modules: 

```$ sudo apt-get install python-opencv python-numpy```

2. ```pylepton``` to control the Lepton camera to capture images: [pylepton](https://github.com/groupgets/pylepton)

```from pylepton import Lepton``` 

3. download LCD libraries: [Waveshare](https://www.waveshare.net/wiki/1.28inch_LCD_Module) 

```from lib import LCD_1inch28```

4. Python Image Library:

```from PIL import Image, ImageDraw, ImageFont ```

5. from Edge Impulse import training model file

```from edge_impulse_linux.image import ImageImpulseRunner```    
```modelfile = os.path.join(dir_path, model)```

6. Using paho.mqtt to transmitt and publish data 

```pip install paho-mqtt```

### Hardware 
|  Hardware  |
|   ----  |
| [Rasperry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) |
| [FLIR Lepton](https://www.sparkfun.com/products/16465)  |
| [1.28-inch LCD Screen](https://www.waveshare.com/wiki/1.28inch_LCD_Module)|

### Software 
|Libraries | Version|
|---- | ----|
|OpenCV | 4.5.0|
|NumPy | 1.2.0|
|Edge-impulse-linux | 1.0.7|
|pylepton | 0.1.2 |
|spidev | 3.5 |
|Pillow | 9.2.0 |
|RPi.GPIO | 0.7.1 |
|paho-mqtt | 1.6.1|

### Enclosure
The orginal design can be found here. 
|Enclosure|
|----|
|Prusa 3D printer| 


### Code Design
1. define the MQTT client, subscribe and publish data:

```def connect_mqtt()``` ```client.connect(broker, port)``` ``` client.publish(topic, label)```
 
 2. control the Lepton to capture image: 

```with Lepton("/dev/spidev0.1") as l:``` ```cv2.imwrite("image111.jpg", np.uint8(a))```

3. Pass the image into model to predict the label: 

```if "classification" in res["result"].keys():``` ```score = res['result']['classification'][label]```

4. Setup LCD screen and display the result 

```draw.text((100, 120), label, fill = (250, 240, 230),font=Font1)```
 


### Output

<img src='https://github.com/xxxcrttt/0022-Dissertation/blob/main/figure/9661660914689_.pic_hd.jpg' height=300 center=/align>

<img src='https://github.com/xxxcrttt/0022-Dissertation/blob/main/figure/9671660914690_.pic_hd.jpg' height=300 center=/align>



