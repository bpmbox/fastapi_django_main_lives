/**
 * Retrieves image data from LINE and returns it as a blob.
 * @return {Blob} Image data as a blob.
 */
function getLineImageData() {
  var options = {
    "method": "GET",
    "headers": {
      "Authorization": "Bearer YOUR_LINE_API_TOKEN"
    }
  };
  
  var response = UrlFetch.fetch("https://api.line.me/v2/profile/picture", options);
  var imageData = response.getContentText();
  var blob = Utilities.newBlob(imageData, "image/jpeg");
  return blob;
}