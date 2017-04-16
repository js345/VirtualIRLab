$(document).ready(function(){
	$(".collapse-able").click(function(){
		var id = $(this).attr("id");
		var child_id = id + "-children";
		if($(this).hasClass("collapsed")){
			$(this).removeClass("collapsed");
			$("#"+child_id).hide();
		}
		else{
			$(this).addClass("collapsed");
			$("#"+child_id).show();
		}
	});
});