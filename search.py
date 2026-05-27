import arxiv

# so this module is for
# - searching for user input keywords
# - and providing results back to the user

def search_papers(query: str, search_type: str = "kw", sort_choice: str = "1", count: int = 5) -> list:

    client = arxiv.Client()

    if search_type=="ti":
        query = f'ti:"{query}"'
    

    if sort_choice=="1":
        curr_sort = arxiv.SortCriterion.SubmittedDate
    else:
        curr_sort = arxiv.SortCriterion.Relevance
        
    
    search = arxiv.Search(
        query=query,
        max_results=count,
        sort_by=curr_sort
    )
    
    results = []

    for r in client.results(search):
        results.append({
            "title": r.title,
            "paper_id": r.get_short_id(),
            "abstract": r.summary,
            "published": r.published.strftime("%d-%m-%Y")
        })

    return results

# if __name__ == "__main__":
#     results = search_papers("attention is all you need", search_type="ti", sort_choice="2", count=2)

#     for r in results:
#         print(r["title"])
#         print(r["paper_id"])
#         print(r["abstract"])
#         print(r["published"])
#         print()