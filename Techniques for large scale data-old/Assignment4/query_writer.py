from SPARQLWrapper import SPARQLWrapper, JSON

# query =\
# """ PREFIX : <http://www.semanticweb.org/juliophx/ontologies/2020/4/assignment4#>
# INSERT DATA {
#     :FF a :Person .
#     :FF :personName "A B C" .
# }
# """
queryHead = "PREFIX : <http://www.semanticweb.org/juliophx/ontologies/2020/4/assignment4#>\n INSERT DATA {\n"
query =f":{} a :Person .\n :{} :personName {} .}"

sparql = SPARQLWrapper("http://localhost:7200/repositories/assignment4/statements",returnFormat=JSON)
sparql.method = 'POST'
sparql.setQuery(query)

try:
    sparql.query()
except:
    print("Failed")
