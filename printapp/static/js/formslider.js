$(document).ready(function(){
  /*$("form").submit(function(e) {
    e.preventDefault();
  });*/
  
  var clogin = $("#content-login");
  var cregister = $("#content-register");
  
  /* display the register page */
  $("#showregister").on("click", function(e){
    e.preventDefault();
    //var newheight = cregister.height();
    console.log($("#tags").val().toLowerCase().split(' ').join('-'));
    var tag_name = $("#tags").val().toLowerCase().split(' ').join('-');
    console.log("tagg name is " + tag_name);
    var content_id ="#content-" + tag_name;
    console.log("content id is " + content_id);
    $(content_id).css("display", "block");
    console.log("content id is " + content_id);
    var ccontent_id = $(content_id);
    var newheight = ccontent_id.height();
    //$("#content-visiting-card").css("display", "block");
    
    $(clogin).stop().animate({
      "left": "-880px"
    }, 800, function(){ /* callback */ });

    $(content_id).stop().animate({
    //$("#content-visiting-card").stop().animate({
      "left": "0px"
    }, 800, function(){ $(clogin).css("display", "none"); });
    
    $("#page").stop().animate({
      "height": newheight+"px"
    }, 550, function(){ /* callback */ });
  });
  
  /* display the login page */
  $("#showlogin").on("click", function(e){
    e.preventDefault();
    var newheight = clogin.height();
    $(clogin).css("display", "block");
    
    $(clogin).stop().animate({
      "left": "0px"
    }, 800, function() { /* callback */ });
    $(cregister).stop().animate({
      "left": "880px"
    }, 800, function() { $(cregister).css("display", "none"); });
    
    $("#page").stop().animate({
      "height": newheight+"px"
    }, 550, function(){ /* callback */ });
  });

  /*$("#visiting-card-submit").click(function(){
    console.log("inside submit");
    $("#visiting-card").submit();
  });*/
});