import arxiv
import os
from urllib.request import urlretrieve

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



# so this module is for downloading the papers
# input -> list of paperIDs
# process -> download and store papers in a data folder
# output -> returns list of paths of files

def download_papers(paperIDs : list) -> dict:

    folder = "data"

    if not os.path.exists(folder):
        os.makedirs(folder)

    transaction = {
        "success": [],
        "failure": []
    }

    client = arxiv.Client()
    
    for pid in paperIDs:
        
        try:
            paper_list = list(client.results(arxiv.Search(id_list=[pid])))

            if not paper_list:
                raise ValueError(f"No paper found for ID: {pid}")

            paper = paper_list[0]

            full_path = os.path.join(folder, f"{paper.get_short_id()}.pdf")

            if os.path.exists(full_path):
                transaction["success"].append(full_path)
                continue

            urlretrieve(paper.pdf_url, full_path)

            transaction["success"].append(full_path)
        
        except Exception as e:
            transaction["failure"].append({"paper_id": pid, "reason": str(e)})
            print(e)
    
    return transaction