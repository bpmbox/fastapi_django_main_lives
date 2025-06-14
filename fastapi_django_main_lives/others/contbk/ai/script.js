function main() {
  var lineData = getLineData();
  var imageData = getBlogImageData(lineData);
  saveImageToDrive(imageData);
}

function getLineData() {
  // Replace with your line API credentials and implementation
  var lineApiUrl = 'https://api.line.me/v2/messages';
  var options = {
    'method': 'GET',
    'headers': {
      'Authorization': 'Bearer YOUR_LINE_API_TOKEN'
    }
  };
  var response = UrlFetchApp.fetch(lineApiUrl, options);
  var lineData = JSON.parse(response.getContentText());
  return lineData;
}

function getBlogImageData(lineData) {
  // Replace with your blog API credentials and implementation
  var blogApiUrl = 'https://example.com/blog/api/images';
  var options = {
    'method': 'GET',
    'headers': {
      'Authorization': 'Bearer YOUR_BLOG_API_TOKEN'
    }
  };
  var response = UrlFetchApp.fetch(blogApiUrl, options);
  var imageData = JSON.parse(response.getContentText());
  return imageData;
}

function saveImageToDrive(imageData) {
  var driveService = DriveService.getDriveService();
  var folder = driveService.getFolderById('YOUR_DRIVE_FOLDER_ID');
  var file = driveService.createFile(imageData, folder);
  Logger.log('Image saved to Drive: %s', file.getUrl());
}