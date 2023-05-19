import json

key_mappings = {
    "keywords": "关键词",
    "company name": "供方名称",
    "company description": "公司描述",
    "product name": "产品名称",
    "行业": "应用板块",
    "产品类型": "产品类型"
}

render_queue = ["product name", "company name", "行业", "产品类型", "company description", "keywords"]

tol = 50


class MarkdownUtil:
    def __init__(self, target: str or None):
        """

        :param target: markdown string
        """
        if target:
            self._target = target
        else:
            self._target = ""

    def retarget(self, target: str or None):
        """

        :param target: markdown string
        :return:
        """
        if target:
            self._target = target
        else:
            self._target = ""

    def get(self) -> str:
        return self._target

    def add_header(self, header: str or None) -> str:
        """

        :param header: normal header string
        :return:
        """
        if not header:
            header = "产品说明书"
        self._target = f"""# {header}\n\n## 一、基本信息\n\n""" + self._target
        return self._target

    def dict2md(self, dict_result: dict) -> str:
        """

        :param dict_result:
        :return:
        """
        self.retarget(None)
        self.add_header(None)

        for task in render_queue:
            if task in dict_result.keys():
                t = dict_result[task]
                if type(t) is list:
                    flattened = ", ".join(t)
                else:
                    flattened = t
                if len(flattened) > tol:
                    self._target += f"""**【{key_mappings[task]}】** \n\t {flattened}\n\n"""
                else:
                    self._target += f"""**【{key_mappings[task]}】** {flattened}\n\n"""
        return self._target


if __name__ == '__main__':
    md_util = MarkdownUtil("")
    result = {
        "keywords": ["数据科技", "产融数字化", "智能数据产品", "产业图谱"],
        "company name": "数库科技",
        "company description": "一家引领产融数字化的数据科技公司，长期致力于在金融及产业领域提供基于产业逻辑的智能数据产品及系统服务，为金融机构、产业园区、企业集团及政府部门在金融及产业数字化转型领域提供完整成熟的数据解决方案",
        "product name": ["SAM产业链", "SmarTag智能资讯引擎", "DAS智能化数据工厂", "企业图谱", "银行数字化平台"],
        "行业": "金融、治理、工业",
        "产品类型": " 数据集"}
    print(md_util.dict2md(result))

