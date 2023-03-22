const input = document.querySelector('.input-file');

input.style.opacity = 0;
input.addEventListener('change', updateImageDisplay);

function updateImageDisplay() {

  const curFiles = input.files;
  if (curFiles.length === 0) {
  	alert("you didn't choose ")
  } else {

    for (const file of curFiles) {
		if (validFileType(file)) {
			alert("successful")
			url = URL.createObjectURL(file);
			inp_file = document.querySelector('.inp-file')
			set_image(url, inp_file)
		} else {
		alert('invalid type')
		}
    }
  }
}
const fileTypes = [
  "image/jpeg",
  "image/jpg",
  "image/png"
];

function validFileType(file) {
  return fileTypes.includes(file.type);
}

function returnFileSize(number) {
  if (number < 1024) {
    return `${number} bytes`;
  } else if (number >= 1024 && number < 1048576) {
    return `${(number / 1024).toFixed(1)} KB`;
  } else if (number >= 1048576) {
    return `${(number / 1048576).toFixed(1)} MB`;
  }
}

function set_image(url, obj) {
	obj.replaceChildren()
    obj.style.background = 'url("'+url+'")'
    obj.style.border = "none";
    obj.style.borderRadius = "0"
    obj.style.backgroundSize = "100% 100%"
}