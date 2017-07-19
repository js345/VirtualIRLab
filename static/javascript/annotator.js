var assignments = {};
var curr_assignment;

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

	// show assignment detail
	$("#assignments-children li").click(function(){
		var name = $(this).html();
		var assignment = assignments[name];

		console.log(assignment);
		
		$("#assignment-name").html(assignment.name);
		$("#assignment-author").html("Author: " + assignment.author);
		$("#assignment-query").html("Query: " + assignment.query);
		$("#assignment-ranker").html("Ranker: " + assignment.ranker);
		$("#assignment-deadline").html("Deadline: " + assignment.deadline);

		$('#content-welcome').hide();
		$("#content-assignment").show();

		curr_assignment = assignment;

		// remind user if this assignment have been finished already
		if(curr_assignment.status == true){
			$("#nav-assignment-btn").html("Start Over");
		}
		else{
			$("#nav-assignment-btn").html("Start");
		}
	});

	// go to assignment
	$("#nav-assignment-btn").click(function(){
		if($(this).html() == "Start Over"){
			$("#alert-modal").modal('show');
			return;
		}

		window.location = "/assignment/" + curr_assignment.author + "/" + curr_assignment.name;
	});

	$("#nav-assignment-modal-btn").click(function(){
		window.location = "/assignment/" + curr_assignment.author + "/" + curr_assignment.name;
	});

	// play btn clicked
	$("#play-btn").click(function(){
		window.location = "/search/" + curr_assignment.author + "/" + curr_assignment.ds_name;
	});
});