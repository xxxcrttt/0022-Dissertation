from distutils.command.clean import clean
import cv2
import os
import sys, getopt
import numpy as np
from edge_impulse_linux.image import ImageImpulseRunner
from pylepton import Lepton
from time import sleep


# mqtt
from paho.mqtt import client as mqtt_client
import random
runner = None 

def help(): 
    print('python classify_image.py <path_to_model.eim> <path_to_image.jpg>')

# MQTT 
broker = 'mqtt.cetools.org'
port = 1884
topic = "student/CASA0022/ucfnrc0/poeple"
client_id = f'python-mqtt-{random.randint(0,1000)}'
username = 'student'
password = 'ce2021-mqtt-forget-whale'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT!")
        else:
            print("Failed to connect, try again", rc)
    
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client 
    print('successfully connect!')


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h", ["--help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            help()
            sys.exit()

    if len(args) != 2:
        help()
        sys.exit(2)
    

    model = args[0]


    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)

    print("MODEL:" + modelfile)

    # mqtt client 
    # 
    client = connect_mqtt()



    with ImageImpulseRunner(modelfile) as runner:
        while True:
            model_info = runner.init()
            print('Loaded runner for "' + model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')
            labels = model_info['model_parameters']['labels']
            #if len(args) >= 2:
            #    DeviceId = int(args[1])

            with Lepton("/dev/spidev0.1") as l:
                a,_ = l.capture()
                
                cv2.normalize(a, a, 0, 65535, cv2.NORM_MINMAX) # extend contrast
                np.right_shift(a, 8, a) # fit data into 8 bits
                cv2.imwrite("image111.jpg", np.uint8(a)) # write it!
                

            
            img = cv2.imread("image111.jpg")
            if img is None:
                print('Failed to load images', "image111.jpg")
                exit(1)
            
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            features, cropped = runner.get_features_from_image(img)

            res = runner.classify(features)

            if "classification" in res["result"].keys():
                print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                for label in labels:
                    score = res['result']['classification'][label]
                    if score > 0.5:
                        print('%s: %.2f\t' % (label, score), end='')
                        client.publish(topic, label)

                print('', flush=True)

            elif "bounding_boxes" in res["result"].keys():
                print('Found %d bounding boxes (%d ms.)' % (len(res["result"]["bounding_boxes"]), res['timing']['dsp'] + res['timing']['classification']))
                for bb in res["result"]["bounding_boxes"]:
                    print('\t%s (%.2f): x=%d y=%d w=%d h=%d' % (bb['label'], bb['value'], bb['x'], bb['y'], bb['width'], bb['height']))
                    cropped = cv2.rectangle(cropped, (bb['x'], bb['y']), (bb['x'] + bb['width'], bb['y'] + bb['height']), (255, 0, 0), 1)

            # the image will be resized and cropped, save a copy of the picture here
            # so you can see what's being passed into the classifier
            cv2.imwrite('debug.jpg', cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR))

            # sleep(5)
            sleep(2)
            

        #finally:
        #    if (runner):
        #        runner.stop()
                

if __name__ == '__main__':
   main(sys.argv[1:])



