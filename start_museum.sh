#!/bin/bash

# Pad naar de website directory
WEBSITE_DIR="/home/pi/museum-site"

# Start de webserver
cd $WEBSITE_DIR
python3 -m http.server 8000 &

# Start de knop-server
python3 $WEBSITE_DIR/arcade_buttons_server.py &

# Wacht op beide processen
wait 