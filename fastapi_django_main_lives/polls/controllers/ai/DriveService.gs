function getDriveService() {
  var service = OAuth2.createService('drive')
    .setAuthorizationBaseUrl('https://accounts.google.com')
    .setTokenUrl('https://accounts.google.com/o/oauth2/token')
    .setClientId('YOUR_CLIENT_ID')
    .setClientSecret('YOUR_CLIENT_SECRET')
    .setCallbackFunction('authCallback')
    .setPropertyStore(PropertiesService.getUserProperties());
  return service;
}

function getFolderById(folderId) {
  var driveService = getDriveService();
  var folder = driveService.getFolderById(folderId);
  return folder;
}

function createFile(imageData, folder) {
  var driveService = getDriveService();
  var file = driveService.createFile(imageData, folder);
  return file;
}