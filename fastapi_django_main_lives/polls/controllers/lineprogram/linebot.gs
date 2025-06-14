/**
 * LINE bot main class
 */
class LineBot {
  /**
   * Constructor
   * @param {string} channelId
   * @param {string} channelSecret
   * @param {string} accessToken
   */
  constructor(channelId, channelSecret, accessToken) {
    this.channelId = channelId;
    this.channelSecret = channelSecret;
    this.accessToken = accessToken;
    this.lineApi = 'https://api.line.me/v2/';
  }

  /**
   * Handle incoming message
   * @param {object} event
   */
  handleMessage(event) {
    var message = event.message;
    var replyToken = event.replyToken;
    var userId = event.source.userId;
    var messageText = message.text;

    // Handle message
    var response = this.handleMessageText(messageText, userId);
    this.replyMessage(replyToken, response);
  }

  /**
   * Handle message text
   * @param {string} messageText
   * @param {string} userId
   * @return {string}
   */
  handleMessageText(messageText, userId) {
    // Simple echo bot
    return messageText;
  }

  /**
   * Reply message
   * @param {string} replyToken
   * @param {string} message
   */
  replyMessage(replyToken, message) {
    var options = {
      'method': 'POST',
      'headers': {
        'Authorization': 'Bearer ' + this.accessToken,
        'Content-Type': 'application/json'
      },
      'payload': JSON.stringify({
        'replyToken': replyToken,
        'messages': [{
          'type': 'text',
          'text': message
        }]
      })
    };
    UrlFetch.fetch(this.lineApi + 'messages/reply', options);
  }
}