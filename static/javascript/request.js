function search(search_package){
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
	})
	.success(function(data){
		console.log(data);
		render_result(data);
	});
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
}

