/*
HTMLのボタンで以下function Motionを実行します。そして
live2d.jsの最初のappから階層をたどりstartMotionを起動=>該当アニメーションが再生します。

第１引数
'TapBody'はHiyori/Hiyori.model3.jsonのMotionsのTapBodyです。
上記MotionsにはIdle,TapBodyがありそれぞれでHiyori/motionsフォルダ内の
アニメーションファイルmotion3.jsonを定義しています。
デフォルトではIdleの方で定義されたアニメーションからランダムで再生されます。
第２引数
numberにてTapBody内から起動するアニメーション種類をインデックスで指定しています。
*/
function Motion(number){
  app.stage.children[1].internalModel.motionManager.startMotion('TapBody',number,2);
}