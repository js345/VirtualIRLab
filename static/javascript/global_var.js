var search_result = null;
var search_algorithms = {
	"":[],
	"OkapiBM25":["k1","b","k3"],
	"JelinekMercer":["lambda"],
	"DirichletPrior":["mu"],
	"AbsoluteDiscount":["delta"],
	"PivotedLength":["s"]
};