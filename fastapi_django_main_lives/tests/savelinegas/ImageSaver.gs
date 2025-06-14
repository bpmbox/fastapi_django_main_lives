class ImageSaver {
  /**
   * Saves an image to Google Drive.
   * @param {String} imageData The URL of the image data.
   */
  saveImage(imageData) {
    var response = UrlFetchApp.fetch(imageData);
    var blob = response.getBlob();
    var folder = DriveApp.getFolderById('YOUR_FOLDER_ID'); // Replace with your folder ID
    var file = folder.createFile(blob);
    Logger.log('Image saved to Google Drive: %s', file.getUrl());
  }
}