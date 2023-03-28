let signupButton = document.querySelector(".picktop__btn2");

// モーダルウィンドウ要素を取得
const modalWrapper = document.querySelector('.modal-wrapper');

// 閉じるボタン要素を取得
const closeButton = document.querySelector('.close-button');

// ボタンをクリックしたときにモーダルウィンドウを表示する
signupButton.addEventListener('click', function() {
  modalWrapper.style.display = 'flex';
});

// 閉じるボタンをクリックしたときにモーダルウィンドウを非表示にする
closeButton.addEventListener('click', function() {
  modalWrapper.style.display = 'none';
});

// モーダルウィンドウの外側をクリックしたときにモーダルウィンドウを非表示にする
modalWrapper.addEventListener('click', function(event) {
  if (event.target === modalWrapper) {
    modalWrapper.style.display = 'none';
  }
});