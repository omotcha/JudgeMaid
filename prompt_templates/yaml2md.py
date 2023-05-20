prompt_yaml2md_en = """
Following is part of an API doc. Please analyze the data fields of HTTP requests and responses and generate a markdown documentation as required.


Requirements:
1. The documentation has no title.
2. As for HTTP request, generate a subtitle called "输入字段" and a table containing fields as follows：
    "序号" representing the index of table, counting from 1 like 1,2,3,...
    "参数名称" representing the attribute name in English, 
    "字段名称" representing the attribute name in Chinese,
    "字段描述" representing the Chinese summerization of the attribute,
    "样例值" representing the example value.
   
3. Generate another subtitle called "输出字段" and a corresponding table for HTTP response in same fashion.
4. Each table must have at least one item. If no item found, do not generate the table and the captions.
5. Please fill "-" into cells whenever you cannot decide what to fill. Do not generate or make up anything that cannot be found from the API doc.


Part of API doc:

```
{context}
```
"""