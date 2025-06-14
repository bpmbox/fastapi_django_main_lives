function getBlogService() {
  var service = OAuth2.createService('blog')
    .setAuthorizationBaseUrl('https://example.com/blog/api')
    .setTokenUrl('https://example.com/blog/api/token')
    .setClientId('YOUR_BLOG_CLIENT_ID')
    .setClientSecret('YOUR_BLOG_CLIENT_SECRET')
    .setCallbackFunction('authCallback')
    .setPropertyStore(PropertiesService.getUserProperties());
  return service;
}

function getImageData(lineData) {
  var blogService = getBlogService();
  var options = {
    'method': 'GET',
    'headers': {
      'Authorization': 'Bearer ' + blogService.getAccessToken()
    }
  };
  var response = UrlFetchApp.fetch('https://example.com/blog/api/images', options);
  var imageData = JSON.parse(response.getContentText());
  return imageData;
}