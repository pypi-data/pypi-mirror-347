# auto-deploy
自动运营部署项目
启动流程：
uv venv --python 3.12
.venv\Scripts\activate
uv pip install -r requirements.txt
playwright install
# sse模式启动
python main.py
# stdio模式启动
python stdio_main.py


# mcp-client配置流程
# sse模式
