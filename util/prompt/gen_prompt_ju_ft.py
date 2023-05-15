import os
import re
import json
import time
from analyze.ju_playwright import get_ju
from config.common import tmp_dir
from config.finetune_prompt_config import *


target_dir = os.path.join(tmp_dir, "ju_prompts")


def trim_content(title: str, content: str) -> str:
    """
    trim the content to the maximum word limit
    :param title:
    :param content:
    :return:
    """
    if len(content) > max_words:
        loc = content.index(title)
        tol = int((max_words - len(title)) / 2)
        start = loc - tol if loc > tol else 0
        end = loc + len(title) + tol
        if end > len(content):
            end = len(content)
        return content[start:end]
    else:
        return content


def build_prompt(title: str, content: str) -> dict:
    """
    build a prompt-completion pair
    :param title:
    :param content:
    :return:
    """
    sep = "\n\n###\n\n"
    mask = "???"
    stop = "###"
    body = content.replace(title, mask)
    prompt = f"Part of Judgement: {body}{sep}"
    completion = f"{title}{stop}"
    return {
        "prompt": prompt,
        "completion": completion,
        "title": title
    }


def ju_gen_prompt(n: int) -> list:
    """
    generate judgement prompts for llm
    :param n:
    :return:
    """
    ju = get_ju(n)
    raw_prompts = []
    pattern_1 = re.compile(r"《.*?》")
    pattern_1_escape = re.compile(r"\w+关于")
    pattern_2 = re.compile(r"\w+法")
    pattern_3 = re.compile(r"中华人民共和国|最高人民法院\w+")
    escape = {"最高人民法", "最高人民法院关于同意广东省深圳市两级法", "最高人民法院关于审理侵犯商业秘密民事案件适用法"}
    hashes = []

    for ju_item in ju:
        details = ju_item["details"]
        for detail in details:
            tmp_titles = pattern_1.findall(detail)
            for title in tmp_titles:
                rn = pattern_1_escape.search(title)
                if rn:
                    continue
                r = pattern_2.search(title)
                if r:
                    title = r.group()
                    if title in escape:
                        continue
                    rr = pattern_3.search(title)
                    if rr:
                        hd = hash(detail)
                        if hd not in hashes:
                            if len(detail) > max_words:
                                if discard_large_sentence:
                                    continue
                                else:
                                    raw_prompts.append(build_prompt(title, trim_content(title, detail)))
                            elif len(detail) < min_words:
                                continue
                            else:
                                raw_prompts.append(build_prompt(title, detail))
                            hashes.append(hd)

    return raw_prompts


def save_jsonl():
    rps = ju_gen_prompt(0) + ju_gen_prompt(1) + ju_gen_prompt(2)
    lable_bucket = {}
    for rp in rps:
        if rp["title"] in lable_bucket.keys():
            lable_bucket[rp["title"]] += 1
        else:
            lable_bucket[rp["title"]] = 1
    result = []
    for rp in rps:
        if lable_bucket[rp["title"]] >= min_samples_per_class:
            index = {v: k for k, v in enumerate(lable_bucket)}.get(rp["title"])
            tmp_rp = {
                "prompt": rp["prompt"],
                "completion": f" {index}:{rp['completion']}"
            }
            result.append(tmp_rp)

    timestamp = time.time()
    with open(os.path.join(target_dir, f"{timestamp}.jsonl"), 'a', encoding='utf-8') as f:
        for rp in result:
            s = json.dumps(rp, ensure_ascii=False)
            f.write(f"{s}\n")


if __name__ == '__main__':
    save_jsonl()
