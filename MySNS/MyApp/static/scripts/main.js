document.addEventListener('DOMContentLoaded', function () {
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