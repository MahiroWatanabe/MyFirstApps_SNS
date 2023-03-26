document.addEventListener('DOMContentLoaded', function () {
  let body = document.querySelector('body');
  console.log(body);
  if(body.classList.contains('pace-runnning')){
    body.classList.add("#particles-js");
  }
    const hero = new HeroSlider('.swiper');
    hero.start();

    new MobileMenu;

});

function searchOnEnter(event) {
  if (event.keyCode === 13) { // Enterキーが押された場合
    var searchText = event.target.value; // inputタグの値を取得
    // ここで検索処理を実行する
    return false; // フォームの送信をキャンセルする
  }
  return true;
}