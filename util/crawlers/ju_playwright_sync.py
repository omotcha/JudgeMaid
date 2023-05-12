import os
import json
import time
from playwright.sync_api import sync_playwright
from config.common import tmp_dir
from config.crawler_config import *

# capacity
cap = 20

ju_data = []

target_dir = os.path.join(tmp_dir, "target_json")


def get_ju_list():
    """
    basic judgement data crawler
    :return:
    """
    count = 0
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(url)
        default_context = browser.contexts[0]
        search_page = default_context.pages[0]
        search_page.goto(API_1, wait_until="networkidle", timeout=30000)

        while count < cap:
            lm_lists = search_page.locator('//div[@class="LM_list"]')
            refs = []
            for lm_list in lm_lists.all():
                list_title = lm_list.locator('//div[@class="list_title clearfix"]')
                ref = list_title.locator('//h4')
                refs.append(ref)

            for ref in refs:
                with default_context.expect_page() as tab:
                    ref.click(timeout=0)
                content_page = tab.value
                content_page.wait_for_load_state()
                content = content_page.locator('//div[@class="PDF_box"]')
                content_title = content.locator('//div[@class="PDF_title"]').inner_text()
                content_detail = content.locator('//div[@class="PDF_pox"]')
                details = content_detail.inner_text().split('\n')
                ju_data.append({
                    "title": content_title,
                    "details": details
                })
                content_page.close()
            count += 1
            # click the next page
            next_button = search_page.locator('//a', has_text="下一页")
            next_button.click(timeout=0)
            search_page.wait_for_timeout(3000)

    s = json.dumps(ju_data, ensure_ascii=False)
    timestamp = time.time()
    with open(os.path.join(target_dir, f"{timestamp}.json", ), 'w', encoding='utf-8') as f:
        f.write(s)


if __name__ == '__main__':
    get_ju_list()
