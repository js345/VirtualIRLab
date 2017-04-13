var uploader_index = 0;


$("#upload-btn").click(function(){
	$(".curr-uploader input").click();
});


function new_file(){
	var filename = $(".curr-uploader input").val();
	$(".curr-uploader").append("<p>" + filename + "</p>");
	$(".curr-uploader").show();

	$(".curr-uploader").removeClass("curr-uploader");

	
	$(".files-container").append(
		"<div class='row'> \
			<div class='curr-uploader'> \
				<input type='file' name='file' onchange='new_file()'> \
			</div> \
		</div>"
	);

	console.log("hello");
}

$("#files-form").submit(function(){
	var formData = new FormData(this);
	console.log(formData);
});

$("#submit-btn").click(function(){
	$("#hidden-submit-btn").click();
});