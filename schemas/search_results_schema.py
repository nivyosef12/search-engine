def search_result_serializer(search_result) -> dict:
    return {
        "id": str(search_result["_id"]),
        "url": search_result["url"],
        "description": search_result["description"]
    }


def search_results_serializer(search_results) -> list:
    return [search_result_serializer(search_result) for search_result in search_results]
