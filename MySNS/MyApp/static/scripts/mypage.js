let detailButtons = document.querySelectorAll(".mypost__btn");

detailButtons.forEach(function(detailButton) {

  const modalWrapper = detailButton.closest(".mypost__usercontainer").querySelector('.modal-wrapper');

  const closeButton = modalWrapper.querySelector('.close-button');

  detailButton.addEventListener('click', function() {
    modalWrapper.style.display = 'flex';
  });

  closeButton.addEventListener('click', function() {
    modalWrapper.style.display = 'none';
  });

  modalWrapper.addEventListener('click', function(event) {
    if (event.target === modalWrapper) {
      modalWrapper.style.display = 'none';
    }
  });
});
