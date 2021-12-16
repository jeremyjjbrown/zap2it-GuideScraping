#!/bin/bash

docker run -d --name zap2it -p 5000:5000 -v /home/jeremybr/.cache/tvguide:/guides zap2it
