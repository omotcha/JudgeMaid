import re


def clean(s: str) -> str:
    return re.sub(r'\n\s+', '', s)


if __name__ == '__main__':
    print(clean("""
    {
        "keywords": ["人工智能", "知识图谱", "知识中台", "图智能"]
    }"""))
