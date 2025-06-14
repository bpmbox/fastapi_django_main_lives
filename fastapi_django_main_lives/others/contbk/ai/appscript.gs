function onEdit(e) {
  var sheet = e.source.getActiveSheet();
  var range = e.range;
  
  // Call Python script to process OCR result
  var pythonScript = "python manage.py ocr_view";
  var ocrResult = UrlFetchApp.fetch(pythonScript);
  
  // Insert OCR result into Google Chat
  var chatService = getService();
  var spaceName = 'spaces/AAAA';
  var message = {'text': ocrResult.getContentText()};
  chatService.spaces.messages.create({
    'parent': spaceName,
    'resource': message
  });
}

function getService() {
  var service = OAuth2.createService('chat')
    .setAuthorizationBaseUrl('https://accounts.google.com')
    .setTokenUrl('https://accounts.google.com/o/oauth2/token')
    .setClientId('your_client_id')
    .setClientSecret('your_client_secret')
    .setCallbackFunction('authCallback')
    .setPropertyStore(PropertiesService.getUserProperties());
  return service;
}

function authCallback(request) {
  var service = getService();
  var authorized = service.handleCallback(request);
  if (authorized) {
    return HtmlService.createHtmlOutput('Authorized');
  } else {
    return HtmlService.createHtmlOutput('Not authorized');
  }
}