(function () {
  const cameraPerSection = 12;
  const urlParams = new URLSearchParams(window.location.search);
  const sectionId = urlParams.get('section') || '1';
  let imageContainers = document.querySelectorAll('.image-container');

  imageContainers.forEach((container, index) => {
    let noSignalElement = document.createElement('h3');

    let cameraNo = index + ((Number(sectionId) - 1) * cameraPerSection) + 1;
    let text = document.createTextNode(`No Signal From Camera #${cameraNo}`);
    noSignalElement.appendChild(text);
    container.appendChild(noSignalElement);
  })
})();
