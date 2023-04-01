document.addEventListener('DOMContentLoaded', function () {
    const hero = new HeroSlider('.swiper');
    hero.start();
    new MobileMenu;
});

// 使ってない
function searchOnEnter(event) {
  if (event.keyCode === 13) { // Enterキーが押された場合
    var searchText = event.target.value; // inputタグの値を取得
    // ここで検索処理を実行する
    return false; // フォームの送信をキャンセルする
  }
  return true;
}

// ウィンドウサイズに応じて表示する文字数を制限する
const windowWidth = window.innerWidth;
let limit;

if (window.location.href.indexOf("post/") > -1) {
  
  async function limitTextByBytes(text, maxBytes) {
    const encoder = new TextEncoder();
    const encoded = encoder.encode(text);
    
    if (encoded.byteLength > maxBytes) {
      const truncated = encoded.slice(0, maxBytes);
      const decoder = new TextDecoder();
      return decoder.decode(truncated);
    } else {
      return text;
    }
  }

  async function onResize(){
    $.ajax({
      url: '/post/json',
      type: 'GET',
      dataType: "json",
      success:async function(data){
        const content = document.querySelectorAll(".pickpost__content");
        let cachedDate = data;
        let reversedcachedDate = [];
        for (let i = cachedDate.length -1; i >= 0; i--){
          reversedcachedDate.push(cachedDate[i]);
        }
        
        for (var i = 0; i < data.length; i++) {
          let regularContent = ""
          console.log(reversedcachedDate[i].content);
          console.log(content[i].innerText);
          console.log("A");

          // もともと表示してあるcontent[i]でできるのか、djangoから直接
          // 貰ったデータでできるのかわからない
          regularContent = await limitTextByBytes(content[i].innerHTML,maxLength);

          content[i].innerText = regularContent;
        }
      }
    });
  }
  
  window.addEventListener('resize',onResize);
  onResize();
}
// // JavaScriptの記述例

// // 文字列をバイト数で制限する
// async function limitTextByBytes(text, maxBytes) {
//   const encoder = new TextEncoder();
//   const encoded = encoder.encode(text);
  
//   if (encoded.byteLength > maxBytes) {
//     const truncated = encoded.slice(0, maxBytes);
//     const decoder = new TextDecoder();
//     return decoder.decode(truncated);
//   } else {
//     return text;
//   }
// }

// // 表示するテキストを取得する
// function getText() {
//   return 'This is a long text to be displayed on a web page. '
//       + 'It should be truncated when the window size is too small.';
// }

// // ウィンドウサイズが変更されたときに呼ばれる
// async function onResize() {
//   const container = document.getElementById('text-container');
//   const text = getText();
  
//   // ウィンドウの幅に応じて、表示する文字列の長さを変更する
//   let maxLength;
//   if (window.innerWidth < 600) {
//     maxLength = 20;
//   } else if (window.innerWidth < 800) {
//     maxLength = 30;
//   } else {
//     maxLength = 50;
//   }
  
//   // 文字列をバイト数で制限する
//   const limitedText = await limitTextByBytes(text, maxLength);
  
//   // 制限された文字列を表示する
//   container.innerText = limitedText;
// }

// // ウィンドウサイズが変更されたときにonResize関数を呼ぶ
// window.addEventListener('resize', onResize);

// // 初期化時にonResize関数を呼ぶ
// onResize();


/* ポストに対するイイね */
document.getElementById('ajax-like-for-post').addEventListener('click', e => {
  e.preventDefault();
  const url = '{% url "MyApp:post_like" %}';
  fetch(url, {
    method: 'POST',
    body: `post_pk={{post.pk}}`,
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
      'X-CSRFToken': '{{ csrf_token }}',
    },
  }).then(response => {
      return response.json();
  }).then(response => {
  // イイね数を書き換える
  const counter = document.getElementById('postlike_count')
  counter.textContent = response.postlike_count
  const icon = document.getElementById('like-for-post-icon')
  // 作成した場合はハートを塗る
  if (response.method == 'create') {
      icon.classList.remove('far')
      icon.classList.add('fas')
      icon.id = 'like-for-post-icon'
  } else {
      icon.classList.remove('fas')
      icon.classList.add('far')
      icon.id = 'like-for-post-icon'
  }
  }).catch(error => {
  console.log(error);
  });
});