/**
 * The main Google Apps Script file
 */

// Get data from Line
function getLineData() {
  var lineApiUrl = 'https://api.line.me/v2/oauth/accessToken';
  var options = {
    'method': 'POST',
    'headers': {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    'payload': 'grant_type=client_credentials&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET'
  };
  var response = UrlFetchApp.fetch(lineApiUrl, options);
  var accessToken = JSON.parse(response.getContentText()).access_token;
  
  // Use the access token to get data from Line
  var lineDataUrl = 'https://api.line.me/v2/messages';
  options = {
    'method': 'GET',
    'headers': {
      'Authorization': 'Bearer ' + accessToken
    }
  };
  response = UrlFetchApp.fetch(lineDataUrl, options);
  var lineData = JSON.parse(response.getContentText());
  
  return lineData;
}

// Get image data from Blog
function getBlogImageData() {
  var blogUrl = 'https://example.com/blog';
  var response = UrlFetchApp.fetch(blogUrl);
  var html = response.getContentText();
  var imageUrls = [];
  var regex = /<img.*?src=[\'"](.*?)[\'"].*?>/g;
  var match;
  while ((match = regex.exec(html)) !== null) {
    imageUrls.push(match[1]);
  }
  
  return imageUrls;
}

// Save image data to Google Drive
function saveImageDataToDrive(imageUrls) {
  var driveFolder = DriveApp.getFolderById('YOUR_DRIVE_FOLDER_ID');
  for (var i = 0; i < imageUrls.length; i++) {
    var imageUrl = imageUrls[i];
    var response = UrlFetchApp.fetch(imageUrl);
    var blob = response.getBlob();
    driveFolder.createFile(blob);
  }
}

// Main function
function main() {
  var lineData = getLineData();
  var imageUrls = getBlogImageData();
  saveImageDataToDrive(imageUrls);
}