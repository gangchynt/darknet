#!/usr/bin/env python2
#
# Copyright 2015-2016 Carnegie Mellon University
# Edited 2018 Obodroid Corporation by Lertlove
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import ptvsd

# Allow other computers to attach to ptvsd at this IP address and port, using the secret
# ptvsd.enable_attach("my_secret", address=('0.0.0.0', 3000))
# Pause the program until a remote debugger is attached
# ptvsd.wait_for_attach()

import os
import sys
fileDir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(fileDir, ".."))
import traceback
import pprint
import txaio
txaio.use_twisted()

from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from twisted.internet import task, reactor, threads
from twisted.internet.defer import Deferred, inlineCallbacks
from twisted.internet.ssl import DefaultOpenSSLContextFactory
from twisted.python import log

import urllib
import argparse
import cv2
import imagehash
import json
from PIL import Image
import numpy as np
import StringIO
import base64
import time
from datetime import datetime
import ssl

# For TLS connections
tls_crt = os.path.join(fileDir, 'tls', 'server.crt')
tls_key = os.path.join(fileDir, 'tls', 'server.key')

parser = argparse.ArgumentParser()
parser.add_argument('--shapePredictor', type=str, help="Path to dlib's shape predictor.",
                    default="")
parser.add_argument('--port', type=int, default=9000,
                    help='WebSocket Port')
args = parser.parse_args()

class RorServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super(RorServerProtocol, self).__init__()

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        msg = 'Your id : {0}'.format(request.peer)
        msg = msg.encode('utf8')

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        raw = payload.decode('utf8')
        print("server raw msg - {}".format(raw))
        self.sendMessage('server send')
        # msg = json.loads(raw)

        # if msg['type'] == "ALL_STATE":
        #     self.loadState(msg['images'], msg['training'], msg['people'])
        # elif msg['type'] == "NULL":
        #     self.sendMessage('{"type": "NULL"}')
        # elif msg['type'] == "FRAME":
        #     print("\n on message: FRAME \n")
        #     from datetime import datetime
        #     from time import sleep

        #     def mockStartThread():  # used for increasing thread pool size
        #         sleep(5)
        #     if len(reactor.getThreadPool().threads) < 10:
        #         reactor.callLater(
        #             0, lambda: reactor.callInThread(mockStartThread))

        #     now = datetime.now()
        #     time_diff = now - \
        #         datetime.strptime(msg['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
        #     print("frame latency: {}".format(time_diff))
        #     if time_diff.seconds < 1:
        #         reactor.callLater(
        #             0, lambda: reactor.callInThread(self.processFrame, msg))
        #         self.sendMessage('{"type": "PROCESSED"}')
        #     else:
        #         print("drop delayed frame")
        # elif msg['type'] == "PROCESS_RECENT_FACE":
        #     self.processRecentFace = msg['val']
        # elif msg['type'] == "ENABLE_CLASSIFIER":
        #     self.enableClassifier = msg['val']
        # elif msg['type'] == "TRAINING":
        #     self.training = msg['val']
        #     if not self.training:
        #         self.trainClassifier()
        # elif msg['type'] == 'SET_MAX_FACE_ID':
        #     self.faceId = int(msg['val']) + 1
        # elif msg['type'] == "REQ_SYNC_IDENTITY":
        #     def getPeople(peopleId, label): return {
        #         'peopleId': peopleId,
        #         'label': label
        #     }
        #     newMsg = {
        #         "type": "SYNC_IDENTITY",
        #         "people": map(getPeople, self.people.keys(), self.people.values())
        #     }
        #     self.sendMessage(json.dumps(newMsg))
        # elif msg['type'] == "UPDATE_IDENTITY":
        #     h = msg['hash'].encode('ascii', 'ignore')
        #     if h in self.images:
        #         self.images[h].identity = msg['idx']
        #         if not self.training:
        #             self.trainClassifier()
        #     else:
        #         print("Image not found.")
        # elif msg['type'] == "REMOVE_IMAGE":
        #     h = msg['hash'].encode('ascii', 'ignore')
        #     if h in self.images:
        #         del self.images[h]
        #         if not self.training:
        #             self.trainClassifier()
        #     else:
        #         print("Image not found.")
        # elif msg['type'] == 'REQ_TSNE':
        #     self.sendTSNE(msg['people'] if 'people' in msg else self.people)
        # elif msg['type'] == 'CLASSIFY':
        #     self.classifyFace(np.array(msg['rep']))
        # else:
        #     print("Warning: Unknown message type: {}".format(msg['type']))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def processFrame(self, msg):
        print("processFrame")

def main(reactor):
    log.startLogging(sys.stdout)
    factory = WebSocketServerFactory()
    factory.protocol = RorServerProtocol
    ctx_factory = DefaultOpenSSLContextFactory(tls_key, tls_crt)
    reactor.listenSSL(args.port, factory, ctx_factory)
    return Deferred()


if __name__ == '__main__':
    task.react(main)
