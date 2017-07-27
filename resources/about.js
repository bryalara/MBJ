function hover(e) {
  $(e.currentTarget).css({
    image: "opacity"
  });
}

function hoverOff(e) {
  $(e.currentTarget).css({
    image: "transparent"
  });
}

function AddEvents(){
  $(".image").on("mouseenter", hover);
  $(".image").on("mouseleave",hoverOff);
}

$(document).ready(AddEvents);
