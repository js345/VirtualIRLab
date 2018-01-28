/**
	
**/
var user;
var classes;
var assignments = {};
var datasets = {};
var curr_assignment_id;
var documents = {};
var curr_dataset_id;

$(document).ready(function(){

	$('[data-toggle="tooltip"]').tooltip(); 

	$("#assignment-deadline").datepicker();

	$("#update-deadline").datepicker();

	$("#nav-upload-btn").click(function(){
		// set user_name
		window.localStorage.setItem("username", user.name);
		window.open("/upload", '_blank');
	});

	// new class
	$("#create-class-btn").click(function(){
		var class_name = $("#class-name").val();
		var password = $("#class-password").val();

		var data = {
			"instructor" : user.name,
			"name" : class_name,
			"password" : password
		};

		$.ajax({
			type: "POST",
			dataType: "json",
			url: "/class",
			data: JSON.stringify(data),
			contentType: 'application/json; charset=utf-8'
		})
		.success(function(data){
			$("#assignment-class").append("<option>" + class_name + "</option>");
		});
	});

	$("#assign-btn").click(function(){
		var ds_id = $('input[name="data_set"]:checked').val();
		if(ds_id == null){
			alert("Please select a dataset first.");
		}
		else{
			$("#assign-modal").modal("show");
		}
	});

	// new assignment
	$("#create-assignment-btn").click(function(){
		// form data
		var name = $("#assignment-name").val();
		var queries = [];
		// list of queries
		$(".query-container").find("input").each(function(){
			if($(this).val() != ""){
				queries.push($(this).val());
			}
		});

		var class_ = $("#assignment-class").val();
		var ds_id = $('input[name="data_set"]:checked').val();
		var ranker = $("#assignment-ranker").val();
		var deadline = $("#assignment-deadline").val();
		var num_results = $("#assignment-num-of-results").val();
		var params = {};

		for(var i = 0; i < search_algorithms[ranker].length; i++){
			var p_id = "#param-" + search_algorithms[ranker][i];
			params[search_algorithms[ranker][i]] = parseFloat($(p_id).val());
		}

		var ds_name = datasets[ds_id].ds_name;
		var ds_author = $('input[name="data_set"]:checked').parent().attr("id");

		// create assignment
		var assign_data = {
			"name" : name,
			"class" : class_,
			"dataset" : ds_id,
			"ranker" : ranker,
			"params" : params,
			"deadline" : deadline,
		};
		// send data to create new assignment
		$.ajax({
			type: "POST",
			dataType: "json",
			url: "/assign",
			data: JSON.stringify(assign_data),
			contentType: 'application/json; charset=utf-8'
		})
		.success(function(data){
			var assginment_id = data;
			var count = 0;
			// send each query to /search
			for(var i = 0; i < queries.length; i++){
				var query = queries[i];
				var search_data = {
					"query" : query,
					"ranker" : ranker,
					"num_results" : num_results,
					"params" : params
				};
				(function(query){
					$.ajax({
						type : "POST",
						url : "/search/" + ds_author + "/" + ds_name,
						data: JSON.stringify(search_data),
						contentType: 'application/json; charset=utf-8'
					})
					.success(function(data){
						doc_scores = {}
						for(var i = 0; i < data.results.length; i++){
							var doc_name = data.results[i].name;
							doc_name = doc_name.substring(0, doc_name.length - 4);
							var doc_score = data.results[i].score;
							doc_scores[doc_name] = doc_score;
						}

						var query_data = {
							"query" : query,
							"doc_scores" : doc_scores,
							"assignment_id" : assginment_id,
							"user_id" : user['_id']['$oid']
						};


						// send data to create new assignment
						$.ajax({
							type: "POST",
							dataType: "json",
							url: "/query",
							data: JSON.stringify(query_data),
							contentType: 'application/json; charset=utf-8'
						})
						.success(function(){
							count++;
							if(count == queries.length){
								$("#assign-notification-modal").modal("show");
							}
						})
					})
				})(query);

			}
		});
	});

	$("#create-assignment-complete-btn").click(function(){
		location.reload();
	});

	// add new query btn
	$("#add-query-btn").click(function(){
		var query_container = $("#query-container");
		if($(".query-container div:nth-last-child(2)").find("input").val() != ""){
			var new_query_html;
			if($(".query-container").children().length == 2){
				var new_query_html = "<div><div class='col-sm-8 col-sm-offset-3'><input id='assignment-query' class='form-control' type='text'></div></div>";
			}
			else{
				var new_query_html = "<div><div class='col-sm-8 col-sm-offset-3' style='margin-top:5px;'><input id='assignment-query' class='form-control' type='text'></div></div>";
			}
			$(this).parent().before(new_query_html);
		}
	});


	// select all clicked 
	$("#assign-select-all").click(function(){
		event.preventDefault();
		$(".ds-checkbox").prop("checked", true);
	});


	// parameter change
	$("#assignment-ranker").change(function(){

		var ranker = $("#assignment-ranker").val();
		var params = search_algorithms[ranker];

		var html = "";

		html += "<div class='row'> \
				    <label class='col-sm-2 control-label col-sm-offset-1'>Params</label> \
				    <div class='col-sm-8'> \
				      <input class='form-control' id='param-" + params[0] + "' type='text' placeholder='" + params[0] + "'> \
				    </div> \
				  </div>"

		for(var i = 1; i < params.length; i++){
			html += "<div class='row'> \
					    <label class='col-sm-2 control-label col-sm-offset-1' style='color:#fff;'>s</label> \
					    <div class='col-sm-8'> \
					      <input class='form-control' id='param-" + params[i] + "' type='text' placeholder='" + params[i] + "'> \
					    </div> \
					  </div>"
		}

		$("#assignment-params").html(html);
	});


	/*
		Update assginment
	*/
	$(".btn-edit").click(function(){
		curr_assignment_id = $(this).parent().parent().attr("id");
	})

	$("#update-assignment-btn").click(function(){
		var curr_assignment = assignments[curr_assignment_id];
		// construct data
		var name = $("#update-name").val();
		var query = $("#update-query").val();
		var ranker = $("#update-ranker").val();
		var deadline = $("#update-deadline").val();
		var num_results = $("#update-num-of-results").val();
		var params = {};
		var search_tag = false;

		for(var i = 0; i < search_algorithms[ranker].length; i++){
			var p_id = "#update-param-" + search_algorithms[ranker][i];
			if(parseFloat($(p_id).val()) != "")
				params[search_algorithms[ranker][i]] = parseFloat($(p_id).val());
		}

		if(name == ""){
			name = curr_assignment.name;
		}

		if(deadline == ""){
			deadline = curr_assignment.deadline;
		}

		if(query == ""){
			query = curr_assignment.query;
		}
		else{
			search_tag = true;
		}

		if(ranker == ""){
			ranker = curr_assignment.ranker;
		}
		else{
			search_tag = true;
		}

		if(Object.keys(params).length == 0){
			params = curr_assignment.params;
		}
		else{
			search_tag = true;
		}

		if(num_results == ""){
			num_results = Object.keys(curr_assignment.doc_scores).length;
		}
		else{
			search_tag = true;
		}



		// if search condition changed
		if(search_tag){
			var search_data = {
				"query" : query,
				"ranker" : ranker,
				"num_results" : num_results,
				"params" : params
			};

			$.ajax({
				type : "POST",
				url : "/search/" + curr_assignment.ds_author + "/" + curr_assignment.ds_name,
				data: JSON.stringify(search_data),
				contentType: 'application/json; charset=utf-8'
			})
			.success(function(data){
				doc_scores = {}
				for(var i = 0; i < data.results.length; i++){
					var doc_name = data.results[i].name;
					doc_name = doc_name.substring(0, doc_name.length - 4);
					var doc_score = data.results[i].score;
					doc_scores[doc_name] = doc_score
				}

				var assign_data = {
					"assignment_id" : curr_assignment_id,
					"name" : name,
					"query" : query,
					"ranker" : ranker,
					"params" : params,
					"deadline" : deadline,
					"doc_scores" : doc_scores
				};


				// send data to create new assignment
				$.ajax({
					type: "POST",
					dataType: "json",
					url: "/assignment_update",
					data: JSON.stringify(assign_data),
					contentType: 'application/json; charset=utf-8'
				})
				.success(function(data){
					$("#assign-notification-modal").modal("show");
					$("#assign-notification-modal").modal("show");
				});
			})
		}
		else{	// directly update data
			var update_data = {
				"assignment_id" : curr_assignment_id,
				"name" : name,
				"query" : query,
				"ranker" : ranker,
				"params" : params,
				"deadline" : deadline,
				"doc_scores" : {}
			};

			$.ajax({
				type: "POST",
				dataType: "json",
				url: "/assignment_update",
				data: JSON.stringify(update_data),
				contentType: 'application/json; charset=utf-8'
			})
			.success(function(data){
				$("#assign-notification-modal").modal("show");
			});
		}

	});

	// update parameter change
	$("#update-ranker").change(function(){
		var ranker = $("#update-ranker").val();
		var params = search_algorithms[ranker];

		var html = "";

		if(ranker == ""){
			$("#update-params").html("");
			return;
		}

		html += "<div class='row'> \
				    <label class='col-sm-2 control-label col-sm-offset-1'>Params</label> \
				    <div class='col-sm-8'> \
				      <input class='form-control' id='update-param-" + params[0] + "' type='text' placeholder='" + params[0] + "'> \
				    </div> \
				  </div>"

		for(var i = 1; i < params.length; i++){
			html += "<div class='row'> \
					    <label class='col-sm-2 control-label col-sm-offset-1' style='color:#fff;'>s</label> \
					    <div class='col-sm-8'> \
					      <input class='form-control' id='update-param-" + params[i] + "' type='text' placeholder='" + params[i] + "'> \
					    </div> \
					  </div>"
		}

		$("#update-params").html(html);
	});

	// show documents for assignments
	var annotated_documents = {}
	var prev_selected_btn = {};
	$(".show-hide-documents-btn").click(function(){
		var button = $(this);
		var id = button.attr("id");

		var assignment_id = id.split("-")[0];
		var query_content = id.split("-")[1];

		table_id = "#table-" + assignment_id;


		if(button.hasClass('btn-primary')){
			button.removeClass('btn-primary').addClass('btn-info');
			$(table_id).hide();
		}
		else{
			if(prev_selected_btn[assignment_id] != null){
				prev_selected_btn[assignment_id].removeClass('btn-primary').addClass('btn-info');
			}

			button.addClass('btn-primary').removeClass('btn-info');
			prev_selected_btn[assignment_id] = button;

			// get documents
			$.ajax({
				type: "GET",
				dataType: "json",
				url: "/documents",
				data: {'assignment_id': assignment_id, 'query_content':query_content}
			})
			.success(function(data){
				var html = "";

				// use the data to update modal
				for(var i = 0; i < data.length; i++){
					var doc = data[i];
					html += "<tr>";
					html += "<td>" + doc.name + "</td>";
					html += "<td>" + doc.score + "</td>";
					html += "<td>" + doc.rel_num + "</td>";
					html += "<td>" + doc.irrel_num + "</td>";
					html += "</tr>";
				}

				$(table_id).find("tbody").html(html);

				$(table_id).show();
			});
		}
	});

	$(".dataset-update-btn").click(function(){
		curr_dataset_id = $(this).attr("id");

		var html = "(";
		for(var i = 0; i < datasets[curr_dataset_id]['collaborators_names'].length; i++){
			if(i == datasets[curr_dataset_id]['collaborators_names'].length - 1){
				html += datasets[curr_dataset_id]['collaborators_names'][i];
				break;
			}

			html += datasets[curr_dataset_id]['collaborators_names'][i] + ", ";
		}
		html += ")";

		$("#dataset-update-collaborators label").html("Collborators" + html);
	});

	// add collaborators
	$("#btn-add-collaborator").click(function(){
		if($("#dataset-update-collaborators div:nth-last-child(2) input").val() == ""){
			return;
		}

		var html;
		if($(this).parent().parent().children().length == 3){
			var html = "<div class='col-sm-8 col-sm-offset-3'><input id='dataset-update-collaborator' class='form-control collaborator' type='text'></div>";
		}
		else{
			var html = "<div class='col-sm-8 col-sm-offset-3' style='margin-top:5px;'><input id='dataset-update-collaborator' class='form-control collaborator' type='text'></div>";
		}

		$(this).parent().before(html);
	});

	// update dataset
	$("#update-dataset-btn").click(function(){
		// form data
		var ds_id = curr_dataset_id;
		var ds_name = $("#dataset-update-name").val();
		var ds_privacy = $("#dataset-update-privacy option:selected").val();
		var collaborators = [];
		$(".collaborator").each(function(i){
			if(datasets[curr_dataset_id]['collaborators_names'].indexOf($(this).val()) != -1){
				alert("The intructor already exists");
				return;
			}

			if($(this).val() != "")
				collaborators.push($(this).val());
		});

		var data = {
			"ds_id" : ds_id,
			"ds_name" : ds_name,
			"ds_privacy" : ds_privacy,
			"collaborators" : collaborators
		};

		$.ajax({
			type: "POST",
			dataType: "json",
			url: "/dataset_update",
			data: JSON.stringify(data),
			contentType: 'application/json; charset=utf-8'
		})
		.success(function(data){
			location.reload();
		});
	});
});



