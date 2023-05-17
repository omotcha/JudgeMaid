prompt_keyword_extraction_zh = """
    下面文字介绍了某公司及其产品，请根据该公司和产品类型，从中提取三到四个关键词，每个关键词不要太长也不要太短。
    答案请使用中文，并用{display_format}的形式来描述。

    公司及产品介绍:
    {context}
    """

prompt_keyword_extraction_en = """
    Following is an introduction to a company and its products, please extract three or four keywords according to the company type and product type. Each of the keyword should not be too long or too short.
    Please answer in Chinese and in {display_format} format as requested.

    Introduction:
    {context}
    """
