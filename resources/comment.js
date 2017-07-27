function hover(e) {
  $(e.currentTarget).css({
    backgroundColor: "white"
  });
}

function hoverOff(e) {
  $(e.currentTarget).css({
    backgroundColor: "transparent"
  });
}

function AddEvents(){
  $(".headerColor").on("mouseenter", hover);
  $(".headerColor").on("mouseleave",hoverOff);
}

$(document).ready(AddEvents);
