var images, submitCurationUrl, successUrl;

$(document).ready(function () {
    //  Jquery UI stuff
    $(".edit-section-image").draggable();
    $(".edit-section-image img").resizable({
      aspectRatio: true
    });

    $("#submitCuration").click(function() {
      submitCuration();
    });
});

function submitCuration() {
  $.each(images, function(index, image) {
    let imgDiv = $("#image-" + image.id),
      top = imgDiv.position().top,
      left = imgDiv.position().left,
      width = imgDiv.width(),
      topPercent = top / document.documentElement.clientHeight * 100,
      leftPercent = left / document.documentElement.clientWidth * 100,
      widthPercent = width / document.documentElement.clientWidth * 100;

    images[index].top = topPercent;
    images[index].left = leftPercent;
    images[index].width = widthPercent;
  });

  $.ajax({
    type: "POST",
    url: submitCurationUrl,
    data: {"images": JSON.stringify(images)},
    success: function(response) {
      if (response.success === true) {
        window.location.replace(successUrl);
      }
    }
  });
}
