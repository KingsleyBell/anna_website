var quill, aboutHeading, aboutText;

function htmlDecode(input){
  if (input.length == 0) {
    return input;
  }
  var e = document.createElement('div');
  e.innerHTML = input;
  return e.childNodes[0].nodeValue;
}

$(document).ready(function () {
    quill = new Quill('#snow-container-heading', {
        placeholder: "About heading",
        theme: "snow"
    });
    quill.clipboard.dangerouslyPasteHTML(htmlDecode(aboutHeading));

    quill = new Quill('#snow-container-text', {
        placeholder: "About text",
        theme: "snow"
    });
    quill.clipboard.dangerouslyPasteHTML(htmlDecode(aboutText));

    $("#about-form").on("submit", function () {
        var myHeadingEditor = document.querySelector("#snow-container-heading");
        var myTextEditor = document.querySelector("#snow-container-text");
        var headingHtml = myHeadingEditor.children[0].innerHTML;
        var textHtml = myTextEditor.children[0].innerHTML;
        $("#heading").val(headingHtml);
        $("#text").val(textHtml);
    });
});
