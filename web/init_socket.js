function isImageElement(element) {
  return element.tagName === 'IMG';
}

function removeFirstChildElement(element) {
  element.removeChild(element.firstChild);
}

function createPictureElement(element) {
  let pictureElement = document.createElement('picture');
  let imageElement = document.createElement('img');
  pictureElement.appendChild(imageElement);
  element.appendChild(pictureElement);
}

function updateImageSrc(element, src) {
  let imageElement = element.getElementsByTagName('img')[0];
  imageElement.src = src;
}

function convertImageBytesToStringArray(image) {
  let bytes = new Uint8Array(image);
  bytes = Array.from(bytes);
  bytes = bytes.map(byte => String.fromCharCode(byte));
  return bytes.join('');
}

function alertContainer(container) {
  let imageElement = container.getElementsByTagName('img')[0];
  imageElement.className = 'alert';

  setTimeout(() => {
    imageElement.className = '';
  }, 1000);
}

const urlParams = new URLSearchParams(window.location.search);
const sectionId = urlParams.get('section') || '1';

const socket = io('http://localhost:5000');
socket.on('connect', function () {
  socket.on(`broadcast-image-${sectionId}`, data => {
    const { image, camera_id: cameraId, is_alert: isAlert } = data;
    const imageBytesString = convertImageBytesToStringArray(image);

    let imageContainer = document.querySelector(`#image-${cameraId}`);

    if (!isImageElement(imageContainer.firstChild)) {
      removeFirstChildElement(imageContainer);
      createPictureElement(imageContainer);
    }

    updateImageSrc(imageContainer, `data:image/png;base64,${imageBytesString}`);
    
    if (isAlert) {
      alertContainer(imageContainer);
    }
  })
});
