var uploader_index = 0;


$("#upload-btn").click(function(){
	$("#files").click();
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
}


$("#files").change(function(){
	var files = $(this).prop("files");
	var html = "";
	for(var i = 0; i < files.length; i++){
		var file = files[i];
		html += "<p>" + file.name + "</p>";
	}
	$(".files-container").html(html);

});


$("#submit-btn").click(function(){	
	var formData = new FormData($("#files-form")[0]);

    $.ajax({
        url: "/upload",
        type: 'POST',
        data: formData,
        async: false,
        success: function (data) {
            $(".files-container").html("");
        },
        cache: false,
        contentType: false,
        processData: false
    });
});