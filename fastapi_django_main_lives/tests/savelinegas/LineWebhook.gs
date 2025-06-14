class LineWebhook {
  /**
   * Handles a LINE Webhook request.
   * @param {Object} e The event object from the LINE Webhook request.
   */
  handleRequest(e) {
    var events = e.events;
    for (var i = 0; i < events.length; i++) {
      var event = events[i];
      if (event.type == 'message' && event.message.type == 'image') {
        var imageData = event.message.contentProvider.previewImageUrl;
        var imageSaver = new ImageSaver();
        imageSaver.saveImage(imageData);
      }
    }
  }
}