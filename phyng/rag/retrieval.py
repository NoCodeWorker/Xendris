from pathlib import Path
from phyng.rag.schemas import SourceRecord
from phyng.rag.source_registry import list_sources


def search_sources(query: str, root_dir: Path) -> list[SourceRecord]:
    if not query:
        return []
        
    query_lower = query.lower()
    all_sources = list_sources(root_dir)
    results = []
    
    for src in all_sources:
        # Match against title
        if src.title and query_lower in src.title.lower():
            results.append(src)
            continue
            
        # Match against notes
        if src.notes and query_lower in src.notes.lower():
            results.append(src)
            continue
            
        # Match against topics
        if any(query_lower in topic.lower() for topic in src.topics):
            results.append(src)
            continue
            
        # Match against authors
        if any(query_lower in author.lower() for author in src.authors):
            results.append(src)
            continue
            
    return results
