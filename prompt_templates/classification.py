# classification tasks: task name + classes
classification_tasks = {
    "应用板块": {
        "intro": None,
        "top_k": 3,
        "classes": ["金融", "贸易", "治理", "交运", "通信", "消费", "医疗", "工业", "能源", "文旅"]
    },
    "产品类型": {
        "intro": """
        产品类型分为数据集和数据服务。区别在于：
        1. 数据集包含完整数据，数据服务包含服务所需要的部分（最少）数据
        2. 数据集的数据可以进一步加工处理，数据服务不可以
        3. 数据集可以满足实际业务需求，根据业务需求进行应用开发；数据服务只能进行API定义好的查询分析操作
        4. 数据集时效性相对差，数据服务时效性相对高
        5. 数据集相对昂贵，数据服务相对便宜
        """,
        "top_k": None,
        "classes": ["数据集", "数据服务"]
    }
}

prompt_multiple_classification_zh = """
    下面文字是某公司及其产品的简要描述，请判断该产品属于什么类型，最多可以属于{top_k}类:
    {intro}
    
    公司名称: 
    {company_name}
    
    产品名称:
    {product_name}
    
    产品描述:
    {product_description}
    
    
    
    所有类型:
    {classes}
    
    请回答:
    
    """

prompt_binary_classification_zh = """
    下面文字是某公司及其产品的简要描述，请判断该产品属于什么类型(只能选择一种类型):
    {intro}
    
    公司名称: 
    {company_name}
    
    产品名称:
    {product_name}
    
    产品描述:
    {product_description}
    
    
    
    所有类型:
    {classes}
    
    请回答:
    
    """