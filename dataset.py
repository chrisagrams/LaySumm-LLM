import json


def load_test_set(path: str) -> json:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def construct_lay_sum_query(elem: dict) -> str:
    base_prompt = "Write down a readable summary of the following biomedical article using less technical terminology (e.g., lay summary) such that it can be understandable for non-expert audiences:"
    abstract = "\n".join(elem["abstract"])
    article = "\n".join(
        [
            "\n".join(section) if isinstance(section, list) else section
            for section in elem["sections"]
        ]
    )

    return f"{base_prompt}\n{abstract}\n{article}"


def get_reference_sum(elem: dict) -> str:
    return "\n".join(elem["summary"])
