prompt_entity_recognition_zh = """
    下面文字介绍了某公司及其产品，请根据要求从中提取关键信息，并用JSON的形式来描述。请使用单层JSON，不要嵌套。
    若无法从中得到答案，请说"没有提供足够的相关信息"，不允许在答案中添加编造成分。答案请使用中文。

    公司及产品介绍:
    {context}

    关键信息：
    公司名称，公司描述，产品名称(如果有多个产品，请列举)
    """

prompt_entity_recognition_en = """
    Following is an introduction to a company and its product, please extract detailed information in JSON format as required. 
    
    Introduction:
    {context}
    
    Requirements:
    1. JSON layer should be exactly one, do not use nested JSON.
    2. Detailed information includes 4 parts: company name, company description, product name and product description. The corresponding keys are ["company name", "company description", "product name", "product description"]
        - If there are multiple products, you just need to generate the first one.
        - Company description and product description should be concise, with no more than 100 words.
    3. If you cannot decide the answer, please just say "Not enough information has been provided". Do not make up anything that cannot be found in the introduction.
    4. The answer only contains a JSON string. Please answer in Chinese.
    
    Please answer:
    """
