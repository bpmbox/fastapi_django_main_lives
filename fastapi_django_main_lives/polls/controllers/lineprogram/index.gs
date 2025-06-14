/**
 * Entry point
 */
function doGet() {
  var channelId = 'YOUR_CHANNEL_ID';
  var channelSecret = 'YOUR_CHANNEL_SECRET';
  var oauth2 = new OAuth2(channelId, channelSecret);
  var accessToken = oauth2.getAccessToken();
  var lineBot = new LineBot(channelId, channelSecret, accessToken);

  var event = {
    'message': {
      'text': 'Hello, World!'
    },
    'replyToken': 'YOUR_REPLY_TOKEN',
    'source': {
      'userId': 'YOUR_USER_ID'
    }
  };
  lineBot.handleMessage(event);
}