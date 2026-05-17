from elasticsearch import Elasticsearch

es = Elasticsearch(
    "http://elasticsearch:9200",
    request_timeout=30
)

def index_data(data):
    for item in data:
        item.pop("_id", None)  # remove MongoDB ObjectId
        safe_item = convert_to_json_safe(item)

        es.index(index="darkweb", document=safe_item)


def convert_to_json_safe(obj):
    if isinstance(obj, dict):
        return {k: convert_to_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_safe(i) for i in obj]
    else:
        return str(obj) if not isinstance(obj, (str, int, float, bool)) else obj
