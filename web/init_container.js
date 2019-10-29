(function () {
  const cameraPerSection = 12;
  let container = document.querySelector('.container');

  for (let i = 0; i < cameraPerSection; i++) {
    let imageContainer = document.createElement('div');
    imageContainer.className = 'image-container';
    imageContainer.id = `image-${i}`;
    container.appendChild(imageContainer);
  }
})();
