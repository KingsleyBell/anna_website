var quill, contactText;

function htmlDecode(input){
  if (input.length == 0) {
    return input;
  }
  var e = document.createElement('div');
  e.innerHTML = input;
  return e.childNodes[0].nodeValue;
}

$(document).ready(function () {
    quill = new Quill('#snow-container-text', {
        placeholder: "Contact text",
        theme: "snow"
    });
    quill.clipboard.dangerouslyPasteHTML(htmlDecode(contactText));

    $("#contact-form").on("submit", function () {
        var myTextEditor = document.querySelector("#snow-container-text");
        var textHtml = myTextEditor.children[0].innerHTML;
        $("#text").val(textHtml);
    });
});
