#!/bin/bash

# Install dependencies
npm install google-apps-script

# Run the codebase
node -e "require('./Code/LineImageGetter.gs').getLineImageData()"
node -e "require('./Code/ImageSaver.gs').saveImageToDrive()"
node -e "require('./Code/SequenceDiagram.gs').generateSequenceDiagram()"
node -e "require('./Code/FolderTree.gs').createFolderTree()"
