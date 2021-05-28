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
        var myHeadingEditor = document.querySelector("#snow-container-heading");
        var myTextEditor = document.querySelector("#snow-container-text");
        var headingHtml = myHeadingEditor.children[0].innerHTML;
        var textHtml = myTextEditor.children[0].innerHTML;
        $("#heading").val(headingHtml);
        $("#text").val(textHtml);
    });
});
