function getImageData(imageUrl) {
  var options = {
    'method': 'GET',
    'headers': {
      'Authorization': 'Bearer YOUR_IMAGE_API_TOKEN'
    }
  };
  var response = UrlFetchApp.fetch(imageUrl, options);
  var imageData = response.getBlob();
  return imageData;
}