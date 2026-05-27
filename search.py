from ddgs import DDGS
def ans_questions(query):
    total_ans = []    
    with DDGS() as ddgs: 
        results = list(ddgs.text(query, max_results=3))
    for i in results:
        total_ans.append(f"{i['title']}: {i['body']} - {i['href']}") 
    return total_ans
    
