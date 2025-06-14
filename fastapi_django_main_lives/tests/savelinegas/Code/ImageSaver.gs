/**
 * Saves the image data to Google Drive.
 * @param {Blob} imageData Image data as a blob.
 */
function saveImageToDrive(imageData) {
  var folder = DriveApp.getFolderById("YOUR_GOOGLE_DRIVE_FOLDER_ID");
  var file = folder.createFile(imageData);
  Logger.log("Image saved to Google Drive: " + file.getUrl());
}