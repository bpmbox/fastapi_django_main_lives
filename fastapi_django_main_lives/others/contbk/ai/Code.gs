// This script handles the image search system

// Configuration
var SECRET_KEY = 'YOUR_SECRET_KEY';
var S3_BUCKET = 'YOUR_S3_BUCKET';
var DRIVE_FOLDER = 'YOUR_DRIVE_FOLDER';

// Function to handle doPost requests
function doPost(e) {
  var type = e.parameter.type;
  var data = e.parameter.data;
  
  if (type == 'image') {
    // Save the image to Google Drive
    var driveFolder = DriveApp.getFolderById(DRIVE_FOLDER);
    var file = driveFolder.createFile(data);
    
    // Upload the file to S3
    var s3 = getS3Client();
    s3.putObject({
      Bucket: S3_BUCKET,
      Key: file.getName(),
      Body: file.getBlob()
    });
  }
}

// Function to get an S3 client
function getS3Client() {
  var awsAccessKeyId = PropertiesService.getUserProperties().getProperty('awsAccessKeyId');
  var awsSecretAccessKey = PropertiesService.getUserProperties().getProperty('awsSecretAccessKey');
  
  var s3 = Aws.S3({
    accessKeyId: awsAccessKeyId,
    secretAccessKey: awsSecretAccessKey
  });
  
  return s3;
}

// Function to generate a PlantUML diagram
function generatePlantUML() {
  var plantUML = ' @startuml\n';
  plantUML += '  participant "Line" as line\n';
  plantUML += '  participant "Google Apps Script" as gas\n';
  plantUML += '  participant "Google Drive" as drive\n';
  plantUML += '  participant "S3" as s3\n';
  plantUML += '  line ->> gas: doPost\n';
  plantUML += '  gas ->> drive: save image\n';
  plantUML += '  gas ->> s3: upload image\n';
  plantUML += ' @enduml\n';
  
  var diagram = UrlFetchApp.fetch('http://www.plantuml.com/plantuml/form', {
    method: 'POST',
    payload: plantUML,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  });
  
  var blob = diagram.getBlob();
  var file = DriveApp.createFile(blob);
  file.setName('system_diagram.png');
}

// Function to generate system documentation
function generateSystemDocumentation() {
  var doc = DocumentApp.createDocument('System Documentation');
  var body = doc.getBody();
  
  body.appendParagraph('System Overview');
  body.appendParagraph('This system handles image search requests from Line and saves the images to Google Drive and uploads them to S3.');
  
  body.appendParagraph('System Flow');
  body.appendParagraph('1. Line sends a doPost request to the Google Apps Script');
  body.appendParagraph('2. The script saves the image to Google Drive');
  body.appendParagraph('3. The script uploads the image to S3');
  
  doc.saveAndClose();
}

// Initialize the system
function init() {
  PropertiesService.getUserProperties().setProperty('awsAccessKeyId', SECRET_KEY);
  PropertiesService.getUserProperties().setProperty('awsSecretAccessKey', SECRET_KEY);
  
  generatePlantUML();
  generateSystemDocumentation();
}