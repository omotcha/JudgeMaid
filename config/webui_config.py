_version = "0.0.1"
_type = "demo"

# service configs

concurrency_cnt = 1
server_name = '127.0.0.1'
server_port = 7860
show_api = False
share = False
in_browser = False

# UI configs

# change the webui title as you wish
webui_title = f"""
# DocQA WebUI

| version {_version} ({_type}) | 
"""

# change the block css as you wish
block_css = """
.importantButton {
    background: linear-gradient(45deg, #700570,#5d1c88, #7000ff) !important;
    border: none !important;
}

.importantButton:hover {
    background: linear-gradient(45deg, #ff00f0,#701cff, #7000ff) !important;
    border: none !important;
}"""

# show progress when having latencies
latent_progress = True

# display the result in json/markdown
display_markdown = True

# allow multithreading
allow_multithreading = True
