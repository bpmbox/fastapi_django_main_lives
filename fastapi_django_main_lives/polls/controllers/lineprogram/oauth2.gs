/**
 * OAuth2 service
 */
class OAuth2 {
  /**
   * Constructor
   * @param {string} clientId
   * @param {string} clientSecret
   */
  constructor(clientId, clientSecret) {
    this.clientId = clientId;
    this.clientSecret = clientSecret;
  }

  /**
   * Get access token
   * @return {string}
   */
  getAccessToken() {
    var service = OAuth2.createService('line-bot')
      .setAuthorizationBaseUrl('https://api.line.me/oauth2/v2.1')
      .setTokenUrl('https://api.line.me/oauth2/v2.1/token')
      .setClientId(this.clientId)
      .setClientSecret(this.clientSecret)
      .setCallbackFunction('authCallback')
      .setPropertyStore(PropertiesService.getUserProperties());
    return service.getAccessToken();
  }

  /**
   * Auth callback
   * @param {object} callback
   */
  authCallback(callback) {
    var authorized = callback.authorized;
    if (authorized) {
      return callback.accessToken;
    } else {
      var authorizationUrl = callback.authorizationUrl;
      Logger.log('Authorization URL: %s', authorizationUrl);
    }
  }
}