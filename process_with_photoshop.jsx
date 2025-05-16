var inputFolder = new Folder(Folder.current + "/downloads");
var outputFolder = new Folder(Folder.current + "/saved");

if (!outputFolder.exists) {
    outputFolder.create();
}

var files = inputFolder.getFiles("*.png");

for (var i = 0; i < files.length; i++) {
    var file = files[i];
    var doc = open(file);
    var filename = file.name.toLowerCase();

    // Eğer isimde bambu veya puffy geçiyorsa renk ayarı yap
    if (filename.includes("puffy") || filename.includes("bambu")) {
        var idLvls = charIDToTypeID("Lvls");
        var desc = new ActionDescriptor();
        var idAdjs = charIDToTypeID("Adjs");
        var list = new ActionList();
        var desc2 = new ActionDescriptor();
        var idChnl = charIDToTypeID("Chnl");
        var ref = new ActionReference();
        ref.putEnumerated(charIDToTypeID("Chnl"), charIDToTypeID("Chnl"), charIDToTypeID("Cmps"));
        desc2.putReference(idChnl, ref);
        desc2.putDouble(charIDToTypeID("Gmm "), 1.2); // orta ton
        list.putObject(idLvls, desc2);
        desc.putList(idAdjs, list);
        executeAction(idLvls, desc, DialogModes.NO);
    }

    // TIF olarak kaydet
    var saveFile = new File(outputFolder + "/" + file.name.replace(".png", ".tif"));
    var tifOptions = new TiffSaveOptions();
    tifOptions.imageCompression = TIFFEncoding.NONE;
    doc.saveAs(saveFile, tifOptions, true);
    doc.close(SaveOptions.DONOTSAVECHANGES);
}
