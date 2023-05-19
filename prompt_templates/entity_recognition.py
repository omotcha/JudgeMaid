prompt_entity_recognition_zh = """
    下面文字介绍了某公司及其产品，请根据要求从中提取关键信息，并用JSON的形式来描述。
    若无法从中得到答案，请说"没有提供足够的相关信息"，不允许在答案中添加编造成分。答案请使用中文。

    公司及产品介绍:
    {context}

    关键信息：
    公司名称，公司描述，产品名称(如果有多个产品，请列举)
    """

prompt_entity_recognition_en = """
    Following is an introduction to a company and its products, please extract detailed information in JSON format as requested.
    If you cannot decide the answer, please just say "Not enough information has been provided". Do not make up anything that cannot be found in the introduction. Please answer in Chinese.
    
    Introduction:
    {context}
    
    Detailed information:
    company name, company description, product name(please list them all when having multiple products)
    """
