input_raw = """        普适智能是一家为客户提供知识图谱应用落地解决方案和产品服务的人工智能公司。自主研发企业级一站式知识图谱平台（知识中台），将AI深度渗透到金融客户的业务决策流程，帮助构建知识大脑，助力商业决策科学化、企业管理高效化。聚焦垂直于银行、证券、保险、政务等领域。
        普适智能的知识中台是一站式“图智能”应用服务提供商，专注为企业提供知识中台以及相关应 用服务，构建统一的企业知识中心， 加速企业数字化进程。中台具有以下优势：（1）零编码。从知识的构建，管理到知识的应用，挖掘，全流程无编码化，提高了开发过程的敏捷型，并大大降低了知识图谱的技术门槛；（2）动态构建。平台兼容了离线，增量，实时，专家编辑等数据接入形式，并兼容多类存储介质(hive, MySql, Oracle等)，保证了知识的及时性。同时平台抽象了图谱的数据逻辑层（本体），可以实现基于本体的快速数据变化；（3）多角色多团队协作。平台在设计时考虑了知识图谱开发过程涉及的多个角色类型，并抽象了一套角色标准。并可以对多团队多图谱的情况进行
了权限的涉及，强化了协作以及数据安全；（4）丰富的应用生态。基于平台，提供了不同行业的企业级知识图谱应用，用户可以根据模版快速在本地落地各类图谱应用。同时平台开放了各类API接口，开发者也可以方便对平台进行定制化业务场景开发。
        架构方面，普适智能的知识中台分为图谱构建平台、图谱可视化平台和图谱分析平台。图谱构建平台核心功能是将数据转成图谱。图谱构建平台包括基础图/场景图构建、图谱定义、图谱构建、数据源管理几个模块；图谱可视化平台基于WebGL强大的绘图能力和多场景下的业务操作积累，汇总出了一系列便于用户查询图数据、挖掘图数据的操作分析功能，包括：展开查询、路径查询、实体强化、时序分析、分页展示等。帮助用户对图谱进行充分的线索挖掘；图谱分析平台集合图计算、特征计算、图向量化、图神经网络等技术，实现在零编码的情况下对构建好的图谱进行实时/离线指标计算、模式匹配、社群分析、标签预测等图分析，可以对计算结果进行应用发布。帮助业务人员方便、快捷的挖掘数据信息、发现潜在关联，实时预警，实现用户之间的协同分析、决策等。"""

input_yaml = """paths:
  /users:
    get:
      summary: List users
      security:
        - OAuth2:
          - admin
      parameters:
        - $ref: '#/components/parameters/usersSearch'
        - $ref: '#/components/parameters/usersBlocked'
        - $ref: '#/components/parameters/start'
        - $ref: '#/components/parameters/count'
        - $ref: '#/components/parameters/usersSort'
      responses:
        '200':
          description: successful operation
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
"""