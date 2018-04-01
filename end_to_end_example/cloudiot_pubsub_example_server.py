#coding:utf-8
# Copyright 2017 Google Inc. All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
r"""Sample server that pushes configuration to Google Cloud IoT devices.

This example represents a server that consumes telemetry data from multiple
Cloud IoT devices. The devices report telemetry data, which the server consumes
from a Cloud Pub/Sub topic. The server then decides whether to turn on or off
individual devices fans.

This example requires the Google Cloud Pub/Sub client library. Install it with

  $ pip install --upgrade google-cloud-pubsub

If you are running this example from a Compute Engine VM, you will have to
enable the Cloud Pub/Sub API for your project, which you can do from the Cloud
Console. Create a pubsub topic, for example
projects/my-project-id/topics/my-topic-name, and a subscription, for example
projects/my-project-id/subscriptions/my-topic-subscription.

You can then run the example with

  $ python cloudiot_pubsub_example_server.py \
    --project_id=my-project-id \
    --pubsub_subscription=my-topic-subscription \
"""

import argparse
import base64
import json
import os
import sys
from threading import Lock
import time

from google.cloud import pubsub
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials


import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="service_account.json"


import socket
from time import ctime
import RPi.GPIO as GPIO
import time
from smbus import SMBus

print '....WIFIROBOTS START!!!...'


#######################################
#############信号引脚定义##############
#######################################
GPIO.setmode(GPIO.BCM)


########电机驱动接口定义#################
ENA = 13	#//L298使能A
ENB = 20	#//L298使能B
IN1 = 19	#//电机接口1
IN2 = 16	#//电机接口2
IN3 = 21	#//电机接口3
IN4 = 26	#//电机接口4

########舵机接口定义#################


#######################################
#########管脚类型设置及初始化##########
#######################################
GPIO.setwarnings(False)
#########电机初始化为LOW##########
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
ENA_pwm=GPIO.PWM(ENA,1000) 
ENA_pwm.start(0) 
ENA_pwm.ChangeDutyCycle(70)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
ENB_pwm=GPIO.PWM(ENB,1000) 
ENB_pwm.start(0) 
ENB_pwm.ChangeDutyCycle(70)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)

def Motor_Forward():
	print 'motor forward'
	GPIO.output(ENA,GPIO.HIGH)
	GPIO.output(ENB,GPIO.HIGH)
	GPIO.output(IN1,GPIO.HIGH)
	GPIO.output(IN2,GPIO.LOW)
	GPIO.output(IN3,GPIO.HIGH)
	GPIO.output(IN4,GPIO.LOW)
	
def Motor_Backward():
	print 'motor_backward'
	GPIO.output(ENA,GPIO.HIGH)
	GPIO.output(ENB,GPIO.HIGH)
	GPIO.output(IN1,GPIO.LOW)
	GPIO.output(IN2,GPIO.HIGH)
	GPIO.output(IN3,GPIO.LOW)
	GPIO.output(IN4,GPIO.HIGH)
	
def Motor_TurnLeft():
	print 'motor_turnleft'
	GPIO.output(ENA,GPIO.HIGH)
	GPIO.output(ENB,GPIO.HIGH)
	GPIO.output(IN1,GPIO.HIGH)
	GPIO.output(IN2,GPIO.LOW)
	GPIO.output(IN3,GPIO.LOW)
	GPIO.output(IN4,GPIO.HIGH)
def Motor_TurnRight():
	print 'motor_turnright'
	GPIO.output(ENA,GPIO.HIGH)
	GPIO.output(ENB,GPIO.HIGH)
	GPIO.output(IN1,GPIO.LOW)
	GPIO.output(IN2,GPIO.HIGH)
	GPIO.output(IN3,GPIO.HIGH)
	GPIO.output(IN4,GPIO.LOW)
def Motor_Stop():
	print 'motor_stop'
	GPIO.output(ENA,GPIO.LOW)
	GPIO.output(ENB,GPIO.LOW)
	GPIO.output(IN1,GPIO.LOW)
	GPIO.output(IN2,GPIO.LOW)
	GPIO.output(IN3,GPIO.LOW)
	GPIO.output(IN4,GPIO.LOW)
	
# HOST = 'daring.cwi.nl'    # The remote host
# PORT = 2001              # The same port as used by the server
# # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
# #     s.connect((HOST, PORT))
# #     s.sendall(b'Hello, world')
# #     data = s.recv(1024)
# # print('Received', repr(data)

API_SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
API_VERSION = 'v1'
DISCOVERY_API = 'https://cloudiot.googleapis.com/$discovery/rest'
SERVICE_NAME = 'cloudiot'


class Server(object):
    """Represents the state of the server."""

    def __init__(self, service_account_json):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            service_account_json, API_SCOPES)
        if not credentials:
            sys.exit('Could not load service account credential '
                     'from {}'.format(service_account_json))

        discovery_url = '{}?version={}'.format(DISCOVERY_API, API_VERSION)

        self._service = discovery.build(
            SERVICE_NAME,
            API_VERSION,
            discoveryServiceUrl=discovery_url,
            credentials=credentials,
            cache_discovery=False)

        # Used to serialize the calls to the
        # modifyCloudToDeviceConfig REST method. This is needed
        # because the google-api-python-client library is built on top
        # of the httplib2 library, which is not thread-safe. For more
        # details, see: https://developers.google.com/
        #     api-client-library/python/guide/thread_safety
        self._update_config_mutex = Lock()

    def _update_device_config(self, project_id, region, registry_id, device_id,
                              data):
        """Push the data to the given device as configuration."""
        # config_data = None
        print('The device ({}) receive a command '
              'of: {}'.format(device_id, data['command']))
        '''
        if data['command']:
            data['command'] = '00'
        if data['command'] == '00':
            Motor_Stop()
            # config_data = {'command': 'stop'}
        elif data['command'] == '01':
            Motor_Forward()
        elif data['command'] == '02':
            Motor_Backward()
        elif data['command'] == '03':
            Motor_TurnLeft()
        elif data['command'] == '04':
            Motor_TurnRight()
        '''
        # with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #     s.connect((HOST, PORT))
        #     s.sendall(data['command'])
            # data = s.recv(1024)
        # print('Received', repr(data)
        # print('The device ({}) has a temperature '
        #       'of: {}'.format(device_id, data['temperature']))
        # if data['temperature'] < 0:
        #     # Turn off the fan.
        #     config_data = {'fan_on': False}
        #     print('Setting fan state for device', device_id, 'to off.')
        # elif data['temperature'] > 10:
        #     # Turn on the fan
        #     config_data = {'fan_on': True}
        #     print('Setting fan state for device', device_id, 'to on.')
        # else:
        #     # Temperature is OK, don't need to push a new config.
        #     return

        '''
        config_data_json = json.dumps(config_data)
        body = {
            # The device configuration specifies a version to update, which
            # can be used to avoid having configuration updates race. In this
            # case, you use the special value of 0, which tells Cloud IoT to
            # always update the config.
            'version_to_update': 0,
            # The data is passed as raw bytes, so you encode it as base64.
            # Note that the device will receive the decoded string, so you
            # do not need to base64 decode the string on the device.
            'binary_data': base64.b64encode(
                    config_data_json.encode('utf-8')).decode('ascii')
        }

        device_name = ('projects/{}/locations/{}/registries/{}/'
                       'devices/{}'.format(
                           project_id,
                           region,
                           registry_id,
                           device_id))

        request = self._service.projects().locations().registries().devices(
        ).modifyCloudToDeviceConfig(name=device_name, body=body)

        # The http call for the device config change is thread-locked so
        # that there aren't competing threads simultaneously using the
        # httplib2 library, which is not thread-safe.
        '''
        # self._update_config_mutex.acquire()
        '''
        try:
            request.execute()
        except HttpError as e:
            # If the server responds with a HtppError, log it here, but
            # continue so that the message does not stay NACK'ed on the
            # pubsub channel.
            print('Error executing ModifyCloudToDeviceConfig: {}'.format(e))
        finally:
            self._update_config_mutex.release()
        '''
        # self._update_config_mutex.release()

    def run(self, project_id, pubsub_subscription):
        """The main loop. Consumes messages from the
        Pub/Sub subscription.
        """

        subscriber = pubsub.SubscriberClient()
        subscription_path = subscriber.subscription_path(
                              project_id,
                              pubsub_subscription)

        def callback(message):
            """Logic executed when a message is received from
            subscribed topic.
            """
            print message
            try:
                data = json.loads(message.data)
            except ValueError as e:
                print('Loading Payload ({}) threw an Exception: {}.'.format(
                    message.data, e))
                message.ack()
                return

            # Get the registry id and device id from the attributes. These are
            # automatically supplied by IoT, and allow the server to determine
            # which device sent the event.
            device_project_id = message.attributes['projectId']
            device_registry_id = message.attributes['deviceRegistryId']
            device_id = message.attributes['deviceId']
            device_region = message.attributes['deviceRegistryLocation']

            # Send the config to the device.
            self._update_device_config(
              device_project_id,
              device_region,
              device_registry_id,
              device_id,
              data)

            # Acknowledge the consumed message. This will ensure that they
            # are not redelivered to this subscription.
            message.ack()

        print('Listening for messages on {}'.format(subscription_path))
        subscriber.subscribe(subscription_path, callback=callback)

        # The subscriber is non-blocking, so keep the main thread from
        # exiting to allow it to process messages in the background.
        
        while True:
            time.sleep(10)
        


def parse_command_line_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Example of Google Cloud IoT registry and '
                    'device management.')
    # Required arguments
    parser.add_argument(
        '--project_id',
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        required=True,
        help='GCP cloud project name.')
    parser.add_argument(
        '--pubsub_subscription',
        required=True,
        help='Google Cloud Pub/Sub subscription name.')

    # Optional arguments
    parser.add_argument(
        '--service_account_json',
        default=os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"),
        help='Path to service account json file.')
    print os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    return parser.parse_args()


def main():
    args = parse_command_line_args()

    server = Server(args.service_account_json)
    server.run(args.project_id, args.pubsub_subscription)


if __name__ == '__main__':
    main()
