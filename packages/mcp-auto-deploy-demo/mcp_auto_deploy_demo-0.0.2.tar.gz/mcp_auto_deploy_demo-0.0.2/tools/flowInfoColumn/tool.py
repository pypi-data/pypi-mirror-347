"""信息流栏目自动化部署工具实现"""
from typing import Dict, Any, List, Annotated
import logging
import asyncio
import re
from pydantic import Field
from tools.base import BaseTool, tool_method
from core.utils import RequestTimer
from tools.common.playwright_service import PlaywrightService
import traceback
import re
from datetime import datetime, timedelta
from tools.common.common_service import set_date_range, fill_select, login_to_system, navigate_url

logger = logging.getLogger(__name__)


class FlowInfoColumnTool(BaseTool):
    """系统部署工具

    提供少儿信息流的自动化部署功能
    """

    def __init__(self, config: Dict[str, Any]):
        """初始化工具类

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.username = config.get("username", "")
        self.password = config.get("password", "")
        self.base_url = config.get("base_url", "")
        self.login_url = config.get("login_url", "")

        if not self.username or not self.password:
            logger.warning(
                "未配置用户名或密码，请在环境变量中设置DEPLOY_USERNAME和DEPLOY_PASSWORD")

        self.pending_submission = None
        self.last_created_page_id = None
        self.pending_column_submission = None

        # 添加表单会话和参数存储
        self.form_sessions = {}  # 存储表单会话

    async def initialize(self) -> None:
        """初始化服务（仅初始化数据结构，不启动浏览器）"""
        try:
            self.service = await PlaywrightService.get_instance(self.config)
            success = await self.service.initialize()
            if success:
                logger.info("浏览器自动化服务初始化成功")
            else:
                logger.error("浏览器自动化服务初始化失败")
                raise RuntimeError("浏览器自动化服务初始化失败")
        except Exception as e:
            logger.error(f"浏览器自动化服务初始化失败 {str(e)}", exc_info=True)
            raise

    async def cleanup(self) -> None:
        """清理资源"""
        if self.service:
            await self.service.cleanup()

        self.service = None
        self.pending_submission = None
        self.last_created_page_id = None
        self.pending_column_submission = None
        logger.info("浏览器自动化服务资源已清理")

    @tool_method(description="查询具体栏目")
    async def query_column(
        self,
        content_id: Annotated[str, Field(description="信息流ID")],
        column_title: Annotated[str, Field(description="栏目标题")]
    ) -> Dict[str, Any]:
        """选择栏目资源 (必须的参数需要用户提供，不允许自动生成)

        Args:
            content_id: 信息流ID（必须）
            column_title: 栏目标题（必须）

        Returns:
            资源选择结果
        """
        try:

            # 必填参数检查
            if not content_id:
                return {
                    "success": False,
                    "message": "信息流id不能为空",
                }
            if not column_title:
                return {
                    "success": False,
                    "message": "媒资形式不能为空",
                    "data": {"请提示用户输入工具必填参数"}
                }
            # 校验外层页面是否是新增栏目页面
            if content_id and column_title:
                # 按照栏目标题搜索对应的栏目
                url = f"{self.config.get('base_url')}/page/cms-lite-launcher/#/page/addPage?id={content_id}"
                success = await navigate_url(self.service, url, self.username, self.password)
                if not success:
                    return {
                        "success": False,
                        "message": "导航到栏目列表页面失败",
                        "data": {}
                    }
                # 等待页面加载完成
                await self.service.page.wait_for_load_state("networkidle", timeout=5000)
                # 确保页面完全加载
                await asyncio.sleep(2) 
                
                #如果当前页面进入了编辑栏目的页面，需要先把这个二级弹窗关掉
                # 检查并关闭可能存在的编辑栏目弹窗
                try:
                # 检查是否存在编辑栏目的弹窗
                    edit_modal_visible = await self.service.page.query_selector('.ant-modal-content form.ant-form-horizontal')
                    if edit_modal_visible:
                        logger.info("检测到编辑栏目弹窗，尝试关闭")
                    
                        # 方法1：点击右上角的关闭按钮 (X)
                        close_button = await self.service.page.query_selector('.ant-modal-close')
                        if close_button:
                            await close_button.click()
                            logger.info("点击右上角X按钮关闭编辑栏目弹窗")
                        else:
                        # 方法2：点击取消按钮
                            await self.service.page.click('.ant-modal-footer button.ant-btn-default:has-text("取 消")')
                            logger.info("点击取消按钮关闭编辑栏目弹窗")
                    
                        # 等待弹窗消失
                        await asyncio.sleep(1)
                        await self.service.page.wait_for_selector('.ant-modal-content', state='hidden', timeout=3000)
                        logger.info("编辑栏目弹窗已关闭")
                except Exception as e:
                    logger.warning(f"尝试关闭弹窗时出错: {str(e)}")

                logger.info(f"正在寻找标题为 '{column_title}' 的栏目")

                # 根据栏目标题找到对应的栏目行
                row_selector = f'.ant-table-tbody tr:has-text("{column_title}")'
                row = await self.service.page.query_selector(row_selector)

                if not row:
                    return {
                        "success": False,
                        "message": f"未找到标题为 '{column_title}' 的栏目",
                        "data": {}
                    }

                # 在该行中找到编辑按钮并点击
                edit_button = await row.query_selector('button:has-text("编辑")')
                if edit_button:
                    await edit_button.click()
                    logger.info(f"已点击 '{column_title}' 栏目的编辑按钮")
                    # 等待编辑页面加载
                    await asyncio.sleep(1)
                    return {
                        "success": True,
                        "message": "获取栏目详情成功，详情请查看浏览器页面",
                        "data": {}
                    }
        except Exception as e:
            logger.error(f"获取栏目详情失败: {str(e)}")
            return {
                "success": False,
                "message": f"获取栏目详情失败: {str(e)}",
                "data": {}
            }

    @tool_method(description="为栏目选择资源")
    async def select_column_resource(
        self,
        resource_channel: Annotated[str, Field(description="频道类型 由用户输入提供 可选值:少儿 教育 健身 老年 戏曲 广场舞")],
        resource_media_type: Annotated[str, Field(description="媒资形式，可选值:视频 音频 爱奇艺SDK 优酷SDK")],
        keyword: Annotated[str, Field(description="搜索关键字可选条件 片名 导演 演员 视频ID")],
        keyword_info: Annotated[str, Field(description="对应具体的片名、导演、演员或视频ID值")],
        resource_module: Annotated[str, Field(
            description="资源类型，可选值:媒资专辑 专题 频道页")] = "媒资专辑"
    ) -> Dict[str, Any]:
        """选择栏目资源 必填的参数需要用户提供，不允许自动生成，必填参数缺少必须暂停，询问用户提供，直到必填参数齐全
        

        Args:
            resource_channel: 频道类型 （必须） 可选值:少儿 教育 健身 老年 戏曲 广场舞
            resource_media_type: 媒资形式，（必须） 可选值:视频 音频 爱奇艺SDK 优酷SDK
            keyword: 搜索关键字可选条件 （必须） 片名 导演 演员 视频ID
            keyword_info: 对应具体的片名、导演、演员或视频ID值 （必须）
            如果视频id有多个时，请用逗号隔开（如rnPNIxRPTT1591761795037,gYJXgbxjpx1591761795038,UXqUNidqxU1591878819508）
            此时你需要将keyword_info的值按逗号分割开，每次取一个填充到关键字的输入框
            比如先设为 rnPNIxRPTT1591761795037,添加完第一个视频ID后，再调用工具选择第二个视频ID，依次类推
            resource_module: 资源类型，可选值:媒资专辑 专题 频道页

        Returns:
            资源选择结果
        """
        try:
            # 必填参数检查
            if not resource_channel:
                return {
                    "success": False,
                    "message": "频道类型不能为空",
                    "data": {"请提示用户输入工具必填参数"}
                }
            if not resource_media_type:
                return {
                    "success": False,
                    "message": "媒资形式不能为空",
                    "data": {"请提示用户输入工具必填参数"}
                }
            resource_number = 10
            # 如果当前页面没有栏目序号元素时，请提示用户先调用query_column工具进行栏目查询
            column_number_selector = '.ant-modal-content:has(#sort)'
            column_number_exists = await self.service.page.query_selector(column_number_selector)
            if not column_number_exists:
                return {
                    "success": False,
                    "message": "当前页面不处于栏目资源添加，先先提供信息流id和栏目标题，再根据query_column工具查询对应的栏目,再调用select_column_resource工具进行资源选择",
                }
            # 资源选择部分处理
            logger.info("准备处理资源选择")

            # 1. 检查是否已经出现资源选择模态框
            resource_modal_selector = '.ant-modal-title:has-text("添加资源")'
            resource_modal_exists = await self.service.page.query_selector(resource_modal_selector)

            # 如果模态框还没有出现，需要双击合适的资源格
            if not resource_modal_exists:
                # 获取所有模板格子及其状态
                template_cells_info = await self.service.page.evaluate('''
                () => {
                    const cells = document.querySelectorAll('[class^="templateCol___"]');
                    return Array.from(cells).map((cell, index) => {
                        // 多种判断方法组合使用
                        const hasFilled = 
                            // 1. 检查是否有filled类或包含bgImg类的元素
                            cell.className.includes('filled') ||
                            cell.querySelector('[class^="bgImg___"]') !== null ||
                            // 2. 检查是否有内容元素
                            cell.querySelector('[class^="itemContent___"]:not(:empty)') !== null ||
                            // 3. 检查是否有img标签
                            cell.querySelector('img') !== null;
                        
                        return {
                            index: index,
                            hasFilled: hasFilled
                        };
                    });
                }
                ''')

                logger.info(f"模板格子状态: {template_cells_info}")

                # 找到第一个未填充的资源格
                empty_cell_index = -1
                for cell in template_cells_info:
                    if not cell.get('hasFilled', True):
                        empty_cell_index = cell.get('index')
                        break

                if empty_cell_index >= 0:
                    logger.info(f"找到未填充的资源格，索引: {empty_cell_index}")

                    # 直接使用Playwright API双击
                    cells = await self.service.page.query_selector_all('[class^="templateCol___"]')
                    if empty_cell_index < len(cells):
                        cell = cells[empty_cell_index]
                        # 再次确认没有img元素
                        has_image = await cell.query_selector('img')
                        if not has_image:
                            # 确保元素可见
                            await cell.scroll_into_view_if_needed()
                            # 双击元素
                            await cell.dblclick()
                            logger.info(
                                f"已使用Playwright API双击索引为 {empty_cell_index} 的未填充资源格")
                            await asyncio.sleep(1)
                else:
                    logger.warning("未找到未填充的资源格，尝试从左往右依次检查和双击")

                    # 从左到右尝试双击每个资源格，通过检查是否有img元素来判断
                    cells = await self.service.page.query_selector_all('[class^="templateCol___"]')
                    for i, cell in enumerate(cells):
                        try:
                            # 检查是否已有资源填充
                            has_image = await cell.query_selector('img')
                            has_bg_img = await cell.query_selector('[class^="bgImg___"]')

                            if not has_image and not has_bg_img:
                                logger.info(f"尝试双击第 {i+1} 个未填充的资源格")
                                await cell.scroll_into_view_if_needed()
                                await cell.dblclick()
                                await asyncio.sleep(0.5)

                                # 检查是否出现添加资源模态框
                                resource_modal = await self.service.page.query_selector('.ant-modal-title:has-text("添加资源")')
                                if resource_modal:
                                    logger.info(f"双击第 {i+1} 个资源格成功，已出现添加资源模态框")
                                    break
                        except Exception as e:
                            logger.warning(f"检查或双击第 {i+1} 个资源格失败: {str(e)}")

            # 再次检查是否已经出现资源选择模态框
            resource_modal_exists = await self.service.page.query_selector(resource_modal_selector)
            if not resource_modal_exists:
                logger.warning("尝试多种方式后仍未能打开资源选择模态框")
                return {
                    "success": False,
                    "message": "模板框已填满，请和用户确认是否调用save_column工具进行保存",
                    "data": {}
                }

            logger.info("资源选择模态框已打开，开始设置搜索条件")

            # 2. 设置资源类型 (媒资专辑/专题/频道页)
            if resource_module:
                logger.info(f"设置资源类型: {resource_module}")
                if resource_module == "视频" or resource_module == "媒资专辑" or resource_module == "video":
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) label:has-text("媒资专辑")')
                elif resource_module == "topic" or resource_module == "专题":
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) label:has-text("专题")')
                elif resource_module == "channel_page" or resource_module == "频道页":
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) label:has-text("频道页")')

            # 3. 设置频道类型
            if resource_channel:
                try:
                    logger.info(f"设置频道类型: {resource_channel}")
                    # 在资源模态框内点击频道类型下拉
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) #channelId, .ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-select:has(#channelId)')
                    await asyncio.sleep(0.5)

                    # 选择下拉选项 (直接点击资源类型的选项)
                    channel_option = f'.ant-select-dropdown .ant-select-item-option-content:has-text("{resource_channel}")'
                    await self.service.page.click(channel_option, timeout=3000)
                    logger.info(f"已选择频道类型: {resource_channel}")
                except Exception as e:
                    logger.warning(f"设置频道类型失败: {str(e)}")

            # 4. 如果需要设置媒资形式
            if resource_media_type and resource_media_type != "视频":  # 默认已经是"视频"
                try:
                    logger.info(f"设置媒资形式: {resource_media_type}")
                    # 在资源模态框内点击媒资形式下拉
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) #mediaType, .ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-select:has(#mediaType)')
                    await asyncio.sleep(0.5)

                    # 选择下拉选项
                    media_option = f'.ant-select-dropdown .ant-select-item-option-content:has-text("{resource_media_type}")'
                    await self.service.page.click(media_option, timeout=3000)
                    logger.info(f"已选择媒资形式: {resource_media_type}")
                except Exception as e:
                    logger.warning(f"设置媒资形式失败: {str(e)}")

            # 5. 设置关键字搜索
            if keyword and keyword_info:
                try:
                    logger.info(f"设置关键字搜索类型: {keyword}, 关键字内容: {keyword_info}")

                    # 5.1 点击关键字类型下拉框
                    keyword_type_selector = '.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-input-group-addon .ant-select-selector'
                    await self.service.page.click(keyword_type_selector)
                    await asyncio.sleep(0.5)

                    # 5.2 选择关键字类型选项(片名/导演/演员/视频ID)
                    keyword_type_option = f'.ant-select-dropdown .ant-select-item-option-content:has-text("{keyword}")'
                    await self.service.page.click(keyword_type_option, timeout=3000)
                    await asyncio.sleep(0.5)

                    # 5.3 在"请输入"框中填写关键字内容
                    keyword_input = '.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-input-group input[placeholder="请输入"]'
                    await self.service.page.fill(keyword_input, keyword_info)

                    # 5.4 点击查询按钮
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) button:has-text("查 询")')
                    logger.info("已点击查询按钮")
                    await asyncio.sleep(1)  # 等待搜索结果
                except Exception as e:
                    logger.warning(f"设置关键字搜索失败: {str(e)}")

            # 6. 选择搜索结果
            try:
                # 等待2秒确保查询完成
                await asyncio.sleep(2)

                # 检查是否有搜索结果
                result_table = '.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-table-tbody tr'
                has_results = await self.service.page.query_selector(result_table)

                if has_results:
                    logger.info("检测到搜索结果，选择资源")
                    
                    # 如果没有结果，则返回
                    if not has_results:
                        return {
                            "success": False,
                            "message": """
                            先尝试将关键词拆分，比如将rnPNIxRPTT1591761795037,gYJXgbxjpx1591761795038拆分成rnPNIxRPTT1591761795037和gYJXgbxjpx1591761795038 分别再调用资源选择工具搜索一次
                            如果还是没有找到任何搜索结果，请和用户确认是否需要重新设置搜索条件
                            """,
                        }

                    # 使用表格头部的全选框（如果需要全选）
                    if resource_number > 3:
                        # 点击表头的全选框
                        select_all_checkbox = '.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-table-thead .ant-checkbox-wrapper input'
                        select_all_exists = await self.service.page.query_selector(select_all_checkbox)

                        if select_all_exists:
                            logger.info("使用全选框选择所有资源")
                            await self.service.page.click(select_all_checkbox)
                            # 等待1秒确保全选完成
                            await asyncio.sleep(1)
                        else:
                            logger.warning("未找到全选框，将使用单个选择方式")
                            # 如果没有全选框，则逐个选择
                            for i in range(min(resource_number, 10)):  # 限制最大选择数量为10
                                checkbox = f'.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-table-tbody tr:nth-child({i+1}) .ant-checkbox-input'
                                await self.service.page.click(checkbox)
                                logger.info(f"已选择第{i+1}个资源结果")
                    else:
                        # 如果只需要选择少量资源，直接逐个选择
                        for i in range(min(resource_number, 10)):  # 限制最大选择数量为10
                            checkbox = f'.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-table-tbody tr:nth-child({i+1}) .ant-checkbox-input'
                            await self.service.page.click(checkbox)
                            logger.info(f"已选择第{i+1}个资源结果")

                    # 点击确定按钮
                    await asyncio.sleep(0.5)
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-modal-footer button.ant-btn-primary:has-text("确 定")')
                    logger.info("已点击确定按钮")

                    # 等待对话框关闭
                    await self.service.page.wait_for_selector('.ant-modal-title:has-text("添加资源")', state='hidden', timeout=5000)
                    
                # 计算已经填充的资源个数
                # 获取所有模板格子及其状态
                template_cells_status = await self.service.page.evaluate('''
                () => {
                    const cells = document.querySelectorAll('[class^="templateCol___"]');
                    return Array.from(cells).map((cell, index) => {
                        // 多种判断方法组合使用
                        const hasFilled = 
                            // 1. 检查是否有filled类或包含bgImg类的元素
                            cell.className.includes('filled') ||
                            cell.querySelector('[class^="bgImg___"]') !== null ||
                            // 2. 检查是否有内容元素
                            cell.querySelector('[class^="itemContent___"]:not(:empty)') !== null ||
                            // 3. 检查是否有img标签
                            cell.querySelector('img') !== null;
                        
                        return {
                            index: index,
                            hasFilled: hasFilled
                        };
                    });
                }
                ''')

                logger.info(f"模板格子状态: {template_cells_status}")

                # 找到第一个未填充的资源格
                count = 0
                for cell in template_cells_status:
                    if cell.get('hasFilled', True):
                        count += 1
                logger.info(f"未填充的资源格数量: {count}")
                remain = len(template_cells_status) - count
                if remain > 0:
                    return {
                        "success": True,
                        "message": f"资源选择成功，还剩余{remain}个资源需要填充，不能调用save_column工具进行保存，需要请询问用户下一次调用select_column_resource工具所需要的必填参数，方便进行下一个资源的填充",
                    }
                else:
                    return {
                        "success": True,
                        "message": "资源填充完毕，你必须暂停，请和用户确认后，在决定是否调用save_column工具进行保存",
                    }
            except Exception as e:
                logger.error(f"选择资源结果失败: {str(e)}")
                # 尝试点击取消按钮
                try:
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-modal-footer button:has-text("取 消")')
                except:
                    pass

                return {
                    "success": False,
                    "message": f"选择资源结果失败: {str(e)}",
                    "data": {
                        "error": str(e)
                    }
                }

        except Exception as e:
            logger.error(f"选择资源失败: {str(e)}")
            return {
                "success": False,
                "message": f"选择资源失败: {str(e)}",
                "data": {
                    "error": str(e)
                }
            }

    @tool_method(description="获取模板名称")
    async def get_all_templates(self) -> Dict[str, Any]:
        """获取模板名称

        Returns:
            List[str]: 模板列表
        """
        url = f"{self.config.get('base_url')}/page/cms-lite-launcher/#/page/template"
        logger.info(f"获取模板 {url}")

        success = await navigate_url(self.service, url, self.username, self.password)

        if success:
            # 提取页面内容，返回列表页中的模板名称
            logger.info("页面加载成功，准备提取模板名称")
            # 等待表格加载完成
            await self.service.page.wait_for_selector('th.ant-table-cell:has-text("模板名称")', timeout=5000)

            # 使用Playwright API直接提取表格数据
            template_names = []

            # 获取所有表格行
            rows = await self.service.page.query_selector_all('.ant-table-tbody tr')
            logger.info(f"找到 {len(rows)} 行数据")

            # 从每行提取模板名称
            for row in rows:
                # 获取第二列单元格（模板名称列）
                name_cell = await row.query_selector('td:nth-child(2)')
                if name_cell:
                    # 获取文本内容
                    name_text = await name_cell.text_content()
                    if name_text and name_text.strip():
                        template_names.append(name_text.strip())

            logger.info(f"提取到的模板名称: {template_names}")
            size = len(template_names)
            return {
                "success": True,
                "message": f"获取模板成功，详情须展示给用户，供用户选择，共获取到了{size}个模板，详情如下：{template_names}",
            }
        else:
            return {
                "success": False,
                "message": "获取所有模板失败",
            }

    @tool_method(description="创建或修改信息流栏目")
    async def fill_column_form(
        self,
        page_id: Annotated[str, Field(description="信息流ID")],
        title: Annotated[str, Field(description="栏目标题")],
        description: Annotated[str, Field(description="栏目描述")],
        template_names: Annotated[List[str], Field(description="模板名称，例如ai绘本专用模板3")],
        publish_start_time: Annotated[str, Field(description="发布开始时间，格式: YYYY-MM-DD HH:mm:ss")],
        publish_end_time: Annotated[str, Field(description="发布结束时间，格式: YYYY-MM-DD HH:mm:ss")],
        enable_sub: Annotated[bool, Field(description="是否需要子栏目")] = False,
        sub_num: Annotated[int, Field(description="子栏目数量")] = 0,
        hide_title: Annotated[bool, Field(description="是否隐藏标题")] = False,
        img_title: Annotated[bool, Field(description="图片标题")] = False,
        is_recommend: Annotated[bool, Field(description="使用推荐算法")] = False,
        sort_number: Annotated[str, Field(description="栏目序号")] = "",
        is_top: Annotated[bool, Field(description="置顶")] = False,
    ) -> Dict[str, Any]:
        """填写信息流栏目表单 必填的参数需要用户提供，不允许自动生成，必填参数缺少必须暂停，询问用户提供，直到必填参数齐全
        1.后面标有必填字样的参数需要用户提供，不允许自动生成，必填参数缺少必须暂停，询问用户提供，直到必填参数齐全
        2.若发布开始时间或发布结束时间未按YYYY-MM-DD HH:mm:ss格式提供，需要先调用query_current_time工具计算出用户想要的时间
        3.可以先调用get_all_template工具获取所有模板，然后提示用户选择模板
        4.如果enable_sub为True，则sub_num为必填参数，否则为可选参数


        Args:
            page_id: 信息流ID（必填）
            title: 栏目标题（必填）
            description: 栏目描述（必填）
            template_names: 模板名称列表（必填）
            hide_title: 是否隐藏标题
            enable_sub: 是否包含子栏目 是或否 默认为否 （
            sub_num: 子栏目数量 （包含子栏目为是时 子栏目数量必填）
            img_title: 图片标题 是或否 默认为否
            is_recommend: 使用推荐算法 是或否 默认为否
            sort_number: 栏目序号 
            is_top: 置顶 是或否 默认为否
            publish_start_time: 发布开始时间 格式: YYYY-MM-DD HH:mm:ss （必填）
            publish_end_time: 发布结束时间 格式: YYYY-MM-DD HH:mm:ss （必填）

        Returns:
            表单填写结果
        """

        with RequestTimer(f"fill_column_form - {title}"):
            try:
                # 必填参数校验
                if not page_id:
                    return {
                        "success": False,
                        "message": "信息流ID不能为空",
                    }
                if not title:
                    return {
                        "success": False,
                        "message": "栏目标题不能为空",
                    }
                if not description:
                    return {
                        "success": False,
                        "message": "栏目描述不能为空",
                    }
                if not template_names:
                    return {
                        "success": False,
                        "message": "模板名称不能为空",
                    }
                if not publish_start_time or not publish_end_time:
                    return {
                        "success": False,
                        "message": "发布开始时间和结束时间不能为空",
                    }
                # 校验时间格式是否正确
                try:
                    datetime.strptime(publish_start_time, "%Y-%m-%d %H:%M:%S")
                    datetime.strptime(publish_end_time, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    # 调用时间工具转换格式
                    now = datetime.now()
                    publish_start_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    publish_end_time = (
                        now + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

                if not self.service:
                    raise RuntimeError("浏览器自动化服务未初始化")

                # 确保浏览器已启动
                if not await self.service.ensure_browser():
                    return {
                        "success": False,
                        "message": "浏览器启动失败，无法填写表单",
                        "data": {}
                    }

                # 1. 如果提供了page_id，导航到对应的页
                if not page_id and self.last_created_page_id:
                    page_id = self.last_created_page_id

                if not page_id:
                    return {
                        "success": False,
                        "message": "未提供信息流ID，无法添加栏目",
                        "data": {}
                    }

                # 导航到信息流编辑页面
                column_url = f"{self.config.get('base_url')}/page/cms-lite-launcher/#/page/addPage?id={page_id}"
                logger.info(f"导航到栏目编辑页 {column_url}")

                success = await navigate_url(self.service, column_url, self.username, self.password)
                if not success:
                    return {
                        "success": False,
                        "message": "导航到栏目编辑页失败",
                        "data": {}
                    }

                # 等待页面加载完成，确保已进入编辑页面
                await self.service.page.wait_for_selector('#title', state='visible')
                logger.info("页面加载完成，页面标题输入框可见")

                # 在信息流内容部署区域，点新增"按钮
                logger.info("点击新增按钮")
                # 如果当前页面没有新增按钮，表示已经在资源选择页了
                if not await self.service.page.query_selector('.ant-card:has-text("信息流内容部") button:has-text("新 增")'):
                    logger.info("当前页面没有新增按钮，进行下一个步骤")
                    pass
                else:
                    await self.service.page.click('.ant-card:has-text("信息流内容部") button:has-text("新 增")')

                # 等待模态框出现
                logger.info("等待栏目表单模态框出现")
                await self.service.page.wait_for_selector('.ant-modal-content', state='visible', timeout=5000)
                await asyncio.sleep(1)
                # 等待模态框完全展开

                # 操作模态框内的表单元素
                # 填写标题 - 父栏目标题输入框的ID就是简单的 #title
                if title:
                    logger.info(f"填写父栏目标题: {title}")
                    # 先清空输入框，避免追加文本
                    await self.service.page.fill('.ant-modal-content #title', '')
                    await self.service.page.fill('.ant-modal-content #title', title)

                # 填写描述 - 父栏目描述输入框的ID就是简单的 #desc
                if description:
                    logger.info(f"填写父栏目描述: {description}")
                    if await self.service.page.query_selector('.ant-modal-content #desc'):
                        # 先清空输入框，避免追加文本
                        await self.service.page.fill('.ant-modal-content #desc', '')
                        await self.service.page.fill('.ant-modal-content #desc', description)
                    else:
                        logger.info("父栏目描述输入框不存在")

                # 设置栏目序号
                if sort_number:
                    logger.info(f"设置栏目序号: {sort_number}")
                    await self.service.page.fill('.ant-modal-content #sort', sort_number)

                # 设置模板
                if template_names and len(template_names) > 0:
                    for template_name in template_names:
                        logger.info(f"选择模板: {template_name}")
                        # 点击模板选择
                        await self.service.page.click('.ant-modal-content #templateIds')
                        # 等待下拉列表
                        await self.service.page.wait_for_selector('.ant-select-dropdown', state='visible', timeout=3000)
                        # 选择模板
                        template_option = f'.ant-select-dropdown .ant-select-item-option:has-text("{template_name}")'
                        template_exists = await self.service.page.wait_for_selector(template_option, state='visible', timeout=3000)
                        if template_exists:
                            await self.service.page.click(template_option)
                            logger.info(f"已选择模板: {template_name}")
                        else:
                            logger.warning(f"未找到模板 {template_name}")

                # 等待短暂时间，确保模板选择操作完成
                await asyncio.sleep(0.5)

                # 如果模板下拉列表仍然可见，点击空白处关闭
                if self.service.page.query_selector('.ant-select-selector'):
                    logger.info("点击空白处关闭模板下拉列表")
                    await self.service.page.click('body')
                    
                # 设置二级栏目
                if enable_sub:
                    logger.info("设置二级栏目")
                    # 如果当前页面没有二级栏目选项，则进行下一个步骤
                    if not await self.service.page.query_selector('.ant-modal-content #enableSub'):
                        logger.info("当前页面没有二级栏目选项，进行下一个步骤")
                        pass
                    else:
                        await self.service.page.click('.ant-modal-content #enableSub')
                # 如果存在子栏目数量，则点击加号，添加对应个数的子栏目
                if enable_sub and sub_num and sub_num > 0:
                    logger.info(f"准备添加{sub_num}个子栏目")
                    try:
                        # 等待子栏目导航列表加载
                        await self.service.page.wait_for_selector('.ant-tabs-nav-list', timeout=3000)
                        
                        # 获取当前已有的子栏目数量
                        existing_tabs = await self.service.page.query_selector_all('.ant-tabs-nav-list .ant-tabs-tab-with-remove')
                        existing_count = len(existing_tabs)
                        logger.info(f"当前已有{existing_count}个子栏目")
                        
                        # 计算需要新增的子栏目数量
                        tabs_to_add = sub_num - existing_count
                        
                        # 如果需要新增子栏目
                        if tabs_to_add > 0:
                            logger.info(f"需要新增{tabs_to_add}个子栏目")
                            # 找到加号按钮
                            add_button_selector = '.ant-tabs-nav-add'
                            add_button = await self.service.page.query_selector(add_button_selector)
                            
                            if add_button:
                                # 点击加号按钮指定次数
                                for i in range(tabs_to_add):
                                    await add_button.click()
                                    logger.info(f"点击加号按钮添加第{i+1}个子栏目")
                                    # 短暂等待，确保UI响应
                                    await asyncio.sleep(0.3)
                                
                                logger.info(f"成功添加{tabs_to_add}个子栏目")
                                
                                # 确保子栏目添加完后重新点击回父栏目标签
                                parent_tab_selector = '.ant-tabs-tab:first-child .ant-tabs-tab-btn'
                                await self.service.page.click(parent_tab_selector)
                                logger.info("已点击回父栏目标签")
                                await asyncio.sleep(0.5)  # 确保UI响应
                            else:
                                logger.warning("未找到子栏目加号按钮")
                        elif tabs_to_add < 0:
                            logger.info(f"当前子栏目数量({existing_count})已超过需要的数量({sub_num})，无需添加")
                        else:
                            logger.info(f"当前子栏目数量({existing_count})已满足需要的数量({sub_num})，无需添加")
                            
                    except Exception as e:
                        logger.error(f"添加子栏目失败: {str(e)}")
                else:
                    logger.info("不需要添加子栏目或子栏目数量未指定")

                # 若未设置发布时间，则设置为当前时间
                if not publish_start_time:
                    publish_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if not publish_end_time:
                    publish_end_time = (
                        datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

                # 设置发布时间
                if publish_start_time and publish_end_time:
                    logger.info(
                        f"设置发布时间: {publish_start_time} - {publish_end_time}")
                    # 使用专用的日期范围设置方法
                    await set_date_range(self.service.page, '.ant-modal-content #publishTime', publish_start_time, publish_end_time)

                # 设置隐藏标题 - 恢复表单设置
                if hide_title:
                    logger.info("设置隐藏标题")
                    # 如果当前页面没有隐藏标题选项，则进行下一个步骤
                    if not await self.service.page.query_selector('.ant-modal-content #titleVisible'):
                        logger.info("当前页面没有隐藏标题选项，进行下一个步骤")
                        pass
                    else:
                        await self.service.page.click('.ant-modal-content #titleVisible')

                
                # 设置图片标题
                if img_title:
                    logger.info("设置图片标题")
                    # 如果当前页面没有图片标题选项，则进行下一个步骤
                    if not await self.service.page.query_selector('.ant-modal-content #imgTitle'):
                        logger.info("当前页面没有图片标题选项，进行下一个步骤")
                        pass
                    else:
                        await self.service.page.click('.ant-modal-content #imgTitle')

                # 设置使用推荐算法
                if is_recommend:
                    logger.info("设置使用推荐算法")
                    # 如果当前页面没有使用推荐算法选项，则进行下一个步骤
                    if not await self.service.page.query_selector('.ant-modal-content #isRecommend'):
                        logger.info("当前页面没有使用推荐算法选项，进行下一个步骤")
                        pass
                    else:
                        await self.service.page.click('.ant-modal-content #isRecommend')

                # 设置置顶
                if is_top:
                    logger.info("设置置顶")
                    await self.service.page.click('.ant-modal-content #isTop')

                # 构建返回结果
                result = {
                    "success": True,
                    "message": "信息流栏目配置填写完成，你必须暂停，提示用户输入fill_sub_column_form工具所需要的必填参数,以进行子栏目的填写" if enable_sub else "信息流栏目配置填写完成，你必须暂停，提示用户输入select_column_resource工具所需要的必填参数，以进行栏目资源的选择"
                }
                
                return result

            except Exception as e:
                logger.error(f"填写信息流栏目表单失败 {e}")
                traceback.print_exc()
                return {
                    "status": "error",
                    "message": f"填写信息流栏目表单失败: {str(e)}",
                    "error": traceback.format_exc()
                }

    @tool_method(description="保存栏目")
    async def save_column(
        self,
        save_type: str
    ) -> Dict[str, Any]:
        """保存栏目 (参数必须由用户提供，不允许自动生成)
        Args:
            save_type: 保存类型，保存（必须）

        Returns:
            提交结果
        """
        with RequestTimer("confirm_column_submission"):
            try:
                if not self.service:
                    raise RuntimeError("浏览器自动化服务未初始化")

                # 确保浏览器已启动
                if not await self.service.ensure_browser():
                    return {
                        "success": False,
                        "message": "浏览器启动失败，无法确认提交栏目",
                        "data": {}
                    }

                # 根据用户选择的保存类型点击对应按钮
                button_text = "保 存"
                save_button_selector = f'.ant-modal-footer button.ant-btn-primary:has-text("{button_text}")'

                await self.service.click_element(save_button_selector)

                # 等待3秒
                await asyncio.sleep(3)

                return {
                    "success": True,
                    "message": "栏目保存成功"
                }

            except Exception as e:
                logger.error(f"确认提交栏目失败: {str(e)}", exc_info=True)
                return {
                    "success": False,
                    "message": f"确认提交栏目失败: {str(e)}",
                }

    @tool_method(description="更新栏目资源")
    async def replace_column_resource(
        self,
        content_id: Annotated[str, Field(description="信息流ID")],
        column_title: Annotated[str, Field(description="栏目标题")],
        resource_index: Annotated[int, Field(description="需要替换的第几个资源")],
    ) -> Dict[str, Any]:
        """替换栏目资源 必填参数需要由用户提供，不允许自动生成，必填参数缺少必须暂停，询问用户提供，直到必填参数齐全
        Args:
            content_id: 信息流ID (必填)
            column_title: 栏目标题 (必填)
            resource_index: 需要替换的第几个资源 （必填）

        Returns:
            替换资源结果
        """
        try:
            # 必填参数检查
            if not content_id:
                return {
                    "success": False,
                    "message": "信息流ID不能为空",
                }
            if not column_title:
                return {
                    "success": False,
                    "message": "栏目标题不能为空",
                }
            if not resource_index or resource_index <= 0:
                return {
                    "success": False,
                    "message": "需要替换的资源序号不能为空且必须大于0",
                }

            # 跳转至资源编辑页
            logger.info(f"准备替换栏目 '{column_title}' 中的第 {resource_index} 个资源")
            query_column_result = await self.query_column(content_id=content_id, column_title=column_title)
            if not query_column_result["success"]:
                return {
                    "success": False,
                    "message": "跳转资源编辑页失败",
                }
            logger.info("跳转资源编辑页成功")
            # 等待页面加载完成
            await self.service.page.wait_for_load_state("networkidle", timeout=5000)
            await asyncio.sleep(1)  # 确保页面完全加载
            

            # 获取表格中所有行
            rows = await self.service.page.query_selector_all('.ant-table-tbody tr:not(.ant-table-placeholder)')
            logger.info(f"找到 {len(rows)} 行资源")

            # 检查提供的索引是否有效
            if not rows:
                return {
                    "success": False,
                    "message": "未找到任何资源行",
                }
                
            if resource_index <= 0 or resource_index > len(rows):
                return {
                    "success": False,
                    "message": f"提供的资源索引 {resource_index} 超出了有效范围 1-{len(rows)}",
                }

            # 找到第resource_index行（注意：resource_index是从1开始的，而数组索引是从0开始的）
            target_row = rows[resource_index - 1]
            logger.info(f"尝试在第 {resource_index} 行查找替换资源按钮")

            # 尝试不同的选择器来找替换资源按钮
            replace_button = None
            
            # 查找所有按钮，检查文本
            if not replace_button:
                try:
                    buttons = await target_row.query_selector_all('button')
                    logger.info(f"在目标行找到 {len(buttons)} 个按钮")
                    
                    for i, btn in enumerate(buttons):
                        btn_text = await btn.text_content()
                        logger.info(f"按钮 {i+1} 文本: '{btn_text.strip()}'")
                        if "替换资源" in btn_text:
                            replace_button = btn
                            logger.info(f"在按钮 {i+1} 找到文本包含'替换资源'的按钮")
                            break
                except Exception as e:
                    logger.error(f"遍历按钮查找替换资源失败: {str(e)}")
                    
            if not replace_button:
                return {
                    "success": False,
                    "message": f"在第 {resource_index} 行未找到'替换资源'按钮",
                }

            logger.info(f"找到'替换资源'按钮，准备点击")
            await replace_button.click()
            await asyncio.sleep(1)  # 等待资源选择模态框打开

            # 检查是否打开了资源选择模态框
            resource_modal = await self.service.page.query_selector('.ant-modal-title:has-text("添加资源")')
            if not resource_modal:
                return {
                    "success": False,
                    "message": "点击'替换资源'按钮后未能打开资源选择模态框",
                }

            return {
                "success": True,
                "message": f"成功点击第 {resource_index} 行的'替换资源'按钮，已打开资源选择模态框。请使用select_column_resource工具继续选择具体要替换的资源",
            }

        except Exception as e:
            logger.error(f"替换栏目资源失败: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"替换栏目资源失败: {str(e)}",
                "data": {"error": str(e)}
            }

    @tool_method(description="填写子栏目")
    async def fill_sub_column_form(
        self,
        page_id: Annotated[str, Field(description="信息流ID")],
        title: Annotated[str, Field(description="栏目标题")],
        description: Annotated[str, Field(description="栏目描述")],
        sub_index: Annotated[int, Field(description="子栏目序号")],
        is_recommend: Annotated[bool, Field(description="使用推荐算法")] = False,
        img_title: Annotated[bool, Field(description="图片标题")] = False
    ) -> Dict[str, Any]:
        """填写子栏目 必填参数需要由用户提供，不允许自动生成，必填参数缺少必须暂停，询问用户提供，直到必填参数齐全
        1.所有后面带有必填字样的参数需要用户提供，不允许自动生成，其余的不做要求
        Args:
            page_id: 信息流ID （必填）
            title: 栏目标题 （必填）
            description: 栏目描述 （必填）
            sub_index: 子栏目序号 （必填）
            is_recommend: 使用推荐算法 是或否 默认为否
            img_title: 图片标题 是或否 默认为否

        Returns:
            填写结果
        """
        try:
            # 必填参数检查
            if not page_id:
                return {
                    "success": False,
                    "message": "信息流ID不能为空"
                }
            if not title:
                return {
                    "success": False,
                    "message": "栏目标题不能为空"
                }

            if not description:
                return {
                    "success": False,
                    "message": "栏目描述不能为空"
                }

            if not sub_index or sub_index <= 0:
                return {
                    "success": False,
                    "message": "子栏目索引不能为空且必须大于0"
                }
            # 检查当前页面是否包含栏目序号
            column_sort_selector = '.ant-modal-content:has(#sort)'
            if not await self.service.page.query_selector(column_sort_selector):
                return {
                    "success": False,
                    "message": "当前页面不在新增栏目页面，请先调用fill_column_form工具填写栏目信息"
                }
            # 检查二级栏目选项是否被勾选，如果未勾选，直接勾选
            sub_column_selector = '.ant-modal-content #enableSub'
            if not await self.service.page.query_selector(sub_column_selector):
                await self.service.page.click(sub_column_selector)
            # 点击子栏目标签
            try:
                # 等待子栏目标签加载
                await self.service.page.wait_for_selector('.ant-tabs-nav-list', timeout=3000)
                
                # 点击对应的子栏目标签按钮 - 直接使用子栏目索引选择对应的标签按钮
                tab_button_selector = f'.ant-tabs-tab:nth-child({sub_index}) .ant-tabs-tab-btn'
                await self.service.page.click(tab_button_selector)
                logger.info(f"已点击第 {sub_index} 个子栏目标签")
                
                # 等待标签内容加载
                await asyncio.sleep(0.5)
            except Exception as e:
                logger.error(f"点击子栏目标签失败: {str(e)}")
                return {
                    "success": False,
                    "message": f"点击子栏目标签失败: {str(e)}"
                }

            # 子栏目的ID格式为 childColumns_{index}_title，其中index是从0开始的索引
            child_index = sub_index - 1  # 将从1开始的用户索引转换为从0开始的内部索引
            
            # 填写子栏目标题
            if title:
                child_title_id = f"childColumns_{child_index}_title"
                logger.info(f"填写子栏目标题 (ID: {child_title_id}): {title}")
                # 先清空输入框，避免追加文本
                await self.service.page.fill(f".ant-modal-content #{child_title_id}", '')
                await self.service.page.fill(f".ant-modal-content #{child_title_id}", title)
            
            # 填写子栏目描述
            if description:
                child_desc_id = f"childColumns_{child_index}_desc"
                logger.info(f"填写子栏目描述 (ID: {child_desc_id}): {description}")
                # 先清空输入框，避免追加文本
                await self.service.page.fill(f".ant-modal-content #{child_desc_id}", '')
                await self.service.page.fill(f".ant-modal-content #{child_desc_id}", description)
            
            # 设置子栏目推荐算法
            if is_recommend:
                child_recommend_id = f"childColumns_{child_index}_isRecommend"
                logger.info(f"设置子栏目推荐算法 (ID: {child_recommend_id}): {is_recommend}")
                
                # 获取当前复选框状态
                is_checked = await self.service.page.evaluate(f'''
                () => {{
                    const checkbox = document.getElementById('{child_recommend_id}');
                    return checkbox ? checkbox.checked : false;
                }}
                ''')
                
                # 如果当前状态与期望状态不同，则点击切换
                if is_checked != is_recommend:
                    await self.service.page.click(f".ant-modal-content #{child_recommend_id}")
            
            # 设置子栏目图片标题
            if img_title:
                child_img_title_id = f"childColumns_{child_index}_towLevelBgImg"
                logger.info(f"设置子栏目图片标题 (ID: {child_img_title_id}): {img_title}")
                
                # 获取当前复选框状态
                is_checked = await self.service.page.evaluate(f'''
                () => {{
                    const checkbox = document.getElementById('{child_img_title_id}');
                    return checkbox ? checkbox.checked : false;
                }}
                ''')
                
                # 如果当前状态与期望状态不同，则点击切换
                if is_checked != img_title:
                    await self.service.page.click(f".ant-modal-content #{child_img_title_id}")

            # 调用select_column_resource工具选择资源
            return {
                "success": True,
                "message": "子栏目填写完成，必须暂停，询问用户调用select_column_resource工具所需要的参数信息，为该子栏目选择资源"
            }

        except Exception as e:
            logger.error(f"填写子栏目失败: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"填写子栏目失败: {str(e)}",
                "data": {"error": str(e)}
            }

