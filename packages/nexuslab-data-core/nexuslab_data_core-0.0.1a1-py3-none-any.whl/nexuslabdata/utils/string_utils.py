import re


def split_camel_case_string(input_str: str) -> list[str]:
    return re.findall(
        r"(?:[A-Z]{2,}(?=[A-Z][a-z]|$))|(?:[A-Z][a-z]+)", input_str
    )


def un_camel(input_str: str) -> str:
    return " ".join(split_camel_case_string(input_str))


def camel_to_snake(name: str) -> str:
    s1 = re.sub(r"(?<!^)(?=[A-Z])", "_", name)
    return s1.lower()
