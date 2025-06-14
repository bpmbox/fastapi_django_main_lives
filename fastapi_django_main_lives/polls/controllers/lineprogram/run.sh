#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run the codebase
google-apps-script --authorization `oauth2.gs` --callback `authCallback` --channelId YOUR_CHANNEL_ID --channelSecret YOUR_CHANNEL_SECRET
node index.gs
