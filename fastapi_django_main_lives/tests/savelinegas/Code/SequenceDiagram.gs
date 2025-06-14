/**
 * Generates a sequence diagram using PlantUML.
 */
function generateSequenceDiagram() {
  var plantUmlCode = "@startuml\n" +
                     "participant Line as L\n" +
                     "participant Google Apps Script as G\n" +
                     "L->>G: Get image data\n" +
                     "G->>L: Return image data\n" +
                     "G->>Drive: Save image to Drive\n" +
                     "@enduml";
  
  var plantUmlService = getPlantUmlService();
  var diagram = plantUmlService.generateDiagram(plantUmlCode);
  var blob = Utilities.newBlob(diagram, "image/png");
  DriveApp.getFolderById("YOUR_GOOGLE_DRIVE_FOLDER_ID").createFile(blob).setName("sequence_diagram.png");
}

/**
 * Returns a PlantUML service instance.
 * @return {PlantUmlService} PlantUML service instance.
 */
function getPlantUmlService() {
  var service = OAuth2.createService("plantuml")
    .setAuthorizationBaseUrl("https://plantuml.com/")
    .setTokenUrl("https://plantuml.com/api/token")
    .setClientId("YOUR_PLANTUML_API_KEY")
    .setClientSecret("YOUR_PLANTUML_API_SECRET")
    .setCallbackFunction("authCallback")
    .setPropertyStore(PropertiesService.getUserProperties());
  return service;
}

/**
 * OAuth2 callback function.
 * @param {Object} request OAuth2 request object.
 */
function authCallback(request) {
  var service = getPlantUmlService();
  var authorized = service.handleCallback(request);
  if (authorized) {
    return HtmlService.createHtmlOutput("Authorized!");
  } else {
    return HtmlService.createHtmlOutput("Access denied.");
  }
}