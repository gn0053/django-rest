from algoliasearch_django import algolia_engine

def get_client():
    return algolia_engine.client

def get_index(param_list):
    client = get_client()
    index = client.multiple_queries(param_list)
    return index

def perform_search(query, *args, **kwargs):
    param_list = []
    individual_params = {}
    tags = ""
    if "tags" in kwargs:
        tags = kwargs.pop("tags") or []
        if len(tags) > 0:
            individual_params["tagFilters"] = tags
    index_filters = [f"{k}:{v}" for k,v in kwargs.items() if v]
    if len(index_filters) > 0:
        individual_params["facetFilters"] = index_filters
        
    param_list.append(individual_params| {"indexName":"cfe_Product", "query":query})
    param_list.append(individual_params| {"indexName":"cfe_Article", "query":query})
    
    result = get_index(param_list)
   
    return result