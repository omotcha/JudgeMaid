# change it when logging in by another user
user = "181217BMTKHNT2W0"

# change it when session being changed
page_id = "69ea4499ebae5820d775213b72969c57"

# currently only support single-tag search
# 信息安全/网络安全/数据安全
tag = "xxx"

# chrome web driver url, port may be different
url = "http://localhost:9222"

# session-less API-url
API_0 = "https://wenshu.court.gov.cn/"

# API-url that needs logging in
API_1 = f"https://wenshu.court.gov.cn/website/wenshu/{user}/index.html?pageId={page_id}&s21={tag}"
