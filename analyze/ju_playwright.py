import os
import json
from config.common import tmp_dir

target_dir = os.path.join(tmp_dir, "target_json")


def get_ju(n: int) -> list:
    """
    get all judgement data
    :param n: the index of jsonl file
    :return:
    """
    dir_l = os.listdir(target_dir)
    if n >= len(dir_l) or n < 0:
        n = -1
    target_jsonl = os.listdir(target_dir)[n]
    with open(os.path.join(target_dir, target_jsonl), 'r', encoding='utf-8') as f:
        crawl_data = json.load(f)
    return crawl_data


def ju_analysis(n: int):
    """
    analyze judgements (jsonl files in target folder)
    :param n: the index of jsonl file
    :return:
    """
    crawl_data = get_ju(n)
    print(crawl_data[9]['title'])


def ju_latest_analysis():
    """
    analyze latest judgement (the last jsonl file in target folder)
    :return:
    """
    crawl_data = get_ju(-1)
    print(len(crawl_data))


if __name__ == '__main__':
    ju_latest_analysis()

