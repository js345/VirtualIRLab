$("#search").click(function(){
	search(create_search_package());
	console.log("1");
});


$("#search-algorithms").change(function(){
	update_para($("#search-algorithms").val())
});


function render_result(data){
	var html = "";
	
	data.results.forEach(function(doc){
		html += "<tr><td>" +
            "<div class='container-fluid result'>" +
              "<div class='row'>" +
                "<div class='col-md-12'>" +
                  "<p> " + doc.path + "</p>" +
                "</div>" +
              "</div>" +
              "<div class='row'>" +
                "<div class='col-md-8 doc-info'>" +
                  "<p>score:" + doc.score + "</p>" +
                "</div>" + 
                "<div class='col-md-4 btn-container'>" +
                  "<span>Relevance: </span><input id='" + doc.doc_id + "' type='checkbox' name='vehicle' value='Bike'>" +
                "</div>"+
              "</div>"+
            "</div>"+
        "</td></tr>"
	});


	$("#results-container table tbody").html(html);

	search_result = data;
	$("#results-container").show();
}


function create_search_package(){
	var query = $("#query_text").val();
	var url_ = "/search/dev/testdata";
	var ranker = $("#search-algorithms").val();
	var params = {};
	var num_results = 5;

	$(".para-box").children(".input-group").each(function(){
		var param_name = $(this).find("label").html();
		var param_val = $(this).find("input").val();
		params[param_name] = parseFloat(param_val);
	});


	return {
		"url": url_,
		"ranker": ranker,
		"query": query,
		"num_results": num_results,
		"params": params
	};
}


function update_para(algo){
	var params = search_algorithms[algo];

	var html = ""

	params.forEach(function(param){
		html += "<div id='" + param + "' class='input-group'>" +
            "<label>" + param + "</label>" +
            "<input type='number' name=''></div>"
	});

	$(".para-box").html(html);
}