/**
 * Creates a folder tree in Google Drive.
 */
function createFolderTree() {
  var rootFolder = DriveApp.getRootFolder();
  var folderTree = [
    { name: "LineImageGetter", folders: [
      { name: "images" },
      { name: "sequence_diagrams" }
    ]}
  ];
  
  createFolders(rootFolder, folderTree);
}

/**
 * Recursively creates folders in Google Drive.
 * @param {Folder} parentFolder Parent folder.
 * @param {Array} folderTree Folder tree structure.
 */
function createFolders(parentFolder, folderTree) {
  folderTree.forEach(function(folder) {
    var subFolder = parentFolder.createFolder(folder.name);
    if (folder.folders) {
      createFolders(subFolder, folder.folders);
    }
  });
}