import json

key_mappings_1 = {
    "keywords": "关键词",
    "company name": "供方名称",
    "company description": "公司描述",
    "product name": "产品名称",
    "product description": "产品描述",
    "应用板块": "应用板块",
    "产品类型": "产品类型",
    "数据主题": "数据主题",
    "series name": "系列名称",
    "来源行业": "来源行业"
}

render_queue_1 = ["series name", "product name", "company name", "应用板块", "来源行业", "数据主题", "产品类型", "product description", "keywords"]

key_mappings_2 = {
    "更新频率": "更新频率",
    "覆盖范围": "覆盖范围",
    "存储大小": "存储大小",
    "存储增量": "存储增量",
    "产品条数": "产品条数",
    "数据维度": "数据维度"
}

render_queue_2 = ["更新频率", "覆盖范围", "存储大小", "存储增量", "产品条数", "数据维度"]

key_mappings_5 = {
    "交付方式": "交付方式",
    "性能参数": "性能参数"
}

render_queue_5 = ["交付方式", "性能参数"]

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
        self._target = f"""# {header}\n\n### 一、基本信息\n\n""" + self._target
        return self._target

    def part_1(self, dict_result: dict) -> str:
        """
        基本信息
        :param dict_result:
        :return:
        """
        self.retarget(None)
        self.add_header(None)

        for task in render_queue_1:
            if task in dict_result.keys():
                t = dict_result[task]
            else:
                t = ""
            if type(t) is list:
                flattened = ", ".join(t)
            else:
                flattened = t
            if len(flattened) > tol:
                self._target += f"""**【{key_mappings_1[task]}】** \n\t {flattened}\n\n"""
            else:
                self._target += f"""**【{key_mappings_1[task]}】** {flattened}\n\n"""
        return self._target

    def part_2(self, dict_result: dict) -> str:
        """
        物理信息
        :param dict_result:
        :return:
        """
        self._target += f"""### 二、物理信息\n\n"""
        for task in render_queue_2:
            if task in dict_result.keys():
                t = dict_result[task]
            else:
                t = ""
            if type(t) is list:
                flattened = ", ".join(t)
            else:
                flattened = t
            if len(flattened) > tol:
                self._target += f"""**【{key_mappings_2[task]}】** \n\t {flattened}\n\n"""
            else:
                self._target += f"""**【{key_mappings_2[task]}】** {flattened}\n\n"""
        return self._target

    def part_3(self, dict_result: dict) -> str:
        """
        内容说明
        :param dict_result:
        :return:
        """
        self._target += f"""### 三、内容说明\n\n"""
        if "api doc generation" in dict_result.keys():
            self._target += dict_result["api doc generation"]["result"]
            self._target += "\n\n"
        return self._target

    def part_4(self, dict_result: dict) -> str:
        """
        使用案例
        :param dict_result:
        :return:
        """
        self._target += f"""### 四、使用案例\n\n"""
        if "cases" in dict_result.keys():
            self._target += dict_result["cases"]["result"]
            self._target += "\n\n"
        return self._target

    def part_5(self, dict_result: dict) -> str:
        """
        使用说明
        :param dict_result:
        :return:
        """
        self._target += f"""### 五、使用说明\n\n"""
        for task in render_queue_5:
            if task in dict_result.keys():
                t = dict_result[task]
            else:
                t = ""
            if type(t) is list:
                flattened = ", ".join(t)
            else:
                flattened = t
            if len(flattened) > tol:
                self._target += f"""**【{key_mappings_5[task]}】** \n\t {flattened}\n\n"""
            else:
                self._target += f"""**【{key_mappings_5[task]}】** {flattened}\n\n"""
        return self._target

    def dict2md(self, dict_result: dict) -> str:
        """

        :param dict_result:
        :return:
        """
        self.part_1(dict_result)
        self.part_2(dict_result)
        self.part_3(dict_result)
        self.part_4(dict_result)
        self.part_5(dict_result)
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

