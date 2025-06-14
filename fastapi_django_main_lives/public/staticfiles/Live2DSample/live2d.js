//appをindex.jsで使いたいのでスコープを外しています。
var app;

// PixiJS
var {
  Application, live2d: { Live2DModel }
} = PIXI;

// Kalidokit
var {
  Face, Vector: { lerp }, Utils: { clamp }
} = Kalidokit;


// 1, Live2Dモデルへのパスを指定する
var modelUrl = "./Hiyori/Hiyori.model3.json";
var currentModel;
	
// メインの処理開始
(async function main() {
  // 2, PixiJSを準備する
  app = new PIXI.Application({
    view: document.getElementById("my-live2d"),
    autoStart: true,
    backgroundAlpha: 0,
    backgroundColor: 0x0000ff,
    resizeTo: window
  });

  // 3, Live2Dモデルをロードする
  currentModel = await Live2DModel.from(modelUrl, { autoInteract: false });
  currentModel.scale.set(0.5);//モデルの大きさ★
  currentModel.interactive = true;
  currentModel.anchor.set(0.5, 0.5);//モデルのアンカー★
  currentModel.position.set(window.innerWidth/2, window.innerHeight);//モデルの位置★

  // 4, Live2Dモデルをドラッグ可能にする
  currentModel.on("pointerdown", e => {
    currentModel.offsetX = e.data.global.x - currentModel.position.x;
    currentModel.offsetY = e.data.global.y - currentModel.position.y;
    currentModel.dragging = true;
  });
  currentModel.on("pointerup", e => {
    currentModel.dragging = false;
    var updateFn = currentModel.internalModel.motionManager.update;
    var coreModel = currentModel.internalModel.coreModel;
    //モーション周りのパスcurrentModel.internalModel.motionManager.startMotion('TapBody', 0,2);

  });
  currentModel.on("pointermove", e => {
    if (currentModel.dragging) {
      currentModel.position.set(
        e.data.global.x - currentModel.offsetX,
        e.data.global.y - currentModel.offsetY
      );
    }
  });

  // 5, Live2Dモデルを拡大/縮小可能に(マウスホイール) #my-live2dはcanvasのidにして下さい
  document.querySelector("#my-live2d").addEventListener("wheel", e => {
    e.preventDefault();
    currentModel.scale.set(
      clamp(currentModel.scale.x + event.deltaY * -0.001, -0.5, 10)
    );
  });
  //背景を設定./background.jpgを画像のパスに書きかえて下さい
  let background = PIXI.Sprite.fromImage('./background.jpg');
  background.anchor.set(0.5);
  background.x = app.screen.width / 2;
  background.y = app.screen.height / 2;
  background.height = app.screen.height;
  background.width = app.screen.width;
  app.stage.addChild(background);
  
  // 6, Live2Dモデルを配置する
  app.stage.addChild(currentModel);

})();



