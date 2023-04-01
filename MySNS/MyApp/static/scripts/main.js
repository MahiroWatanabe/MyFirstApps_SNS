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
      let lastByte = truncated[truncated.length - 1];
      let charsToRemove = 0;
      while ((lastByte & 0xC0) === 0x80) {
        charsToRemove++;
        lastByte = truncated[truncated.length - 1 - charsToRemove];
      }
      const finalBytes = truncated.slice(0, truncated.length - charsToRemove);
      let ans = decoder.decode(finalBytes);
      ans = ans.slice(0,ans.length-1);
      ans += "..."
      return ans;
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
          let maxLength;
          let windowSize = window.innerWidth;

          if (windowSize >= 1475){
            maxLength = 300;
          }else if (windowSize >= 1329){
            maxLength = 150;
          }else if(windowSize >= 960){
            maxLength = 85;
          }
          regularContent = await limitTextByBytes(reversedcachedDate[i].content,maxLength);
          content[i].innerText = regularContent;
        }
      }
    });
  }
  
  window.addEventListener('resize',onResize);
  onResize();
}

/* ポストに対するイイね */
// document.getElementById('ajax-like-for-post').addEventListener('click', e => {
//   e.preventDefault();
//   const url = '{% url "MyApp:post_like" %}';
//   fetch(url, {
//     method: 'POST',
//     body: `post_pk={{post.pk}}`,
//     headers: {
//       'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
//       'X-CSRFToken': '{{ csrf_token }}',
//     },
//   }).then(response => {
//       return response.json();
//   }).then(response => {
//   // イイね数を書き換える
//   const counter = document.getElementById('postlike_count')
//   counter.textContent = response.postlike_count
//   const icon = document.getElementById('like-for-post-icon')
//   // 作成した場合はハートを塗る
//   if (response.method == 'create') {
//       icon.classList.remove('far')
//       icon.classList.add('fas')
//       icon.id = 'like-for-post-icon'
//   } else {
//       icon.classList.remove('fas')
//       icon.classList.add('far')
//       icon.id = 'like-for-post-icon'
//   }
//   }).catch(error => {
//   console.log(error);
//   });
// });