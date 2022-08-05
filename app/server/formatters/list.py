def format_list(data, format_item, limit):
    """
    Format lists where 1 extra elemet is included if there is a 'next page'.
    Limit is the given limit + 1 (what was used in the db query)
    """
    visible_data = data[: limit - 1]
    return {
        "data": [format_item(i) for i in visible_data],
        "count": len(visible_data),
        "has_more": len(data) == limit,
    }
