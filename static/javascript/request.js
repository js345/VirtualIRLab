function search(){
	search_package = {
		"url": "/search/dev/testdata",
		"ranker": "",
		"query": "one",
		"num_results": 5,
		"params":{}
	}

	data = {
		"ranker":search_package['ranker'],
		"query":search_package['query'],
		"num_results":search_package['num_results'],
		"params":search_package['params']
	};

	$.ajax({
		type: "POST",
		url: search_package['url'],
		data: data,
		tpye: "jsonp"
	})
	.success(function(data){
		console.log(data)
		// $(document).load(data);
		upload(data);
	});
}


function upload(data){
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

	var btn_html = "<tr><td>" + "<button onclick='submit()' class='btn btn-primary btn-block' style='margin-top:30px;'>Submit</button>" + "<tr></td>";
	$("#results-container").html($("#results-container").html()+btn_html);

	search_result = data;
}

function submit(){

	var documents = [];

	search_result.results.forEach(function(doc){
		var judge = document.getElementById(doc.doc_id).checked;
		documents.push({"doc_id":doc.doc_id,"judge": judge});
	});

	var package = {
		"dataset" : "test",
		"doc":documents,
		"query":search_result.query,
		"user":"li"
	}
	console.log(package);
}