
from .main import generate_embeddings, search_similar, parse_filter_arg
from datetime import datetime, timezone
import sys
import logging

log = logging.getLogger(__name__)

async def store_embedding(text, relevant_date=None, force_index=False):
    """
    Stores an embedding with metadata in the LanceDB database.
    """

    parsed_relevant_date_obj = None
    if relevant_date is not None:
        try:
            parsed_relevant_date_obj = datetime.fromisoformat(relevant_date)

            if parsed_relevant_date_obj.tzinfo is not None:
                parsed_relevant_date_obj = parsed_relevant_date_obj.astimezone(timezone.utc).replace(tzinfo=None)
        except ValueError:
            log.error(f"Invalid relevant_date format: '{relevant_date}'. Please use ISO8601 format (e.g., 'YYYY-MM-DDTHH:MM:SS' or 'YYYY-MM-DD').")
            sys.exit(1)

    generate_embeddings(text, save=True, relevant_date=parsed_relevant_date_obj, force_index=force_index)

    return True, None

async def search_embeddings(query, count=5, created_date_filters=None, relevant_date_filters=None):
    """
    Searches for embeddings similar to the query text, with optional date filters.
    """

    # Generate embeddings for the query
    query_embedding = generate_embeddings(query)

    parsed_filters = parse_filter_arg(created_date_filters, "created_date")
    parsed_filters.extend(parse_filter_arg(relevant_date_filters, "relevant_date"))

    results = search_similar(query_embedding, k=count, filters=parsed_filters)

    # Extract only the requested fields from the results
    formatted_results = []
    for result in results:
        formatted_result = {
            "cosine_search_distance": result["_distance"],
            "relevant_date": result["relevant_date"].strftime("%Y-%m-%d %H:%M:%S") if result["relevant_date"] is not None else None,
            "created_date": result["created_date"].strftime("%Y-%m-%d %H:%M:%S") if result["created_date"] is not None else None,
            "metadata": result["metadata"]
        }
        formatted_results.append(formatted_result)
    
    return True, formatted_results