def reciprocal_rank_fusion(rankings, k=60):
    scores={}
    for ranking in rankings:
        for rank , doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id,0) + 1/(rank+k+1)
    return sorted(scores.items(),key=lambda x:x[1],reverse=True)
            
