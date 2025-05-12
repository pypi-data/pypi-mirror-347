"""
信息流自动化部署工具实现
"""
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
from tools.common.common_service import fill_select, login_to_system, navigate_url

logger = logging.getLogger(__name__)


class FlowInfoTool(BaseTool):
    """系统部署工具

    提供少儿信息流的自动化部署功能
    """

    def __init__(self, config: Dict[str, Any]):
        """初始化工具类

        Args:
            config: 配置参数
        """
        super().__init__(config)
        # 不在这里创建service实例，而是在initialize中使用单例模式获取
        self.service = None
        self.username = config.get("username", "")
        self.password = config.get("password", "")
        self.base_url = config.get("base_url", "")

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
            # 使用单例模式获取PlaywrightService实例
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

    @tool_method(description="创建或修改信息流")
    async def fill_information_flow_form(
        self,
        title: Annotated[str, Field(description="信息流标题，必填")],
        channel_id: Annotated[str, Field(description="频道, 必填 可选值有 少儿 教育 健身 电影 广场")],
        terminal_type: Annotated[str, Field(description="下发渠道, 必填 可选值有 TCL 三星 绘本APK 少儿小程序")],
        description: Annotated[str, Field(description="页面描述")] = "",
        fee_type: Annotated[str, Field(description="付费类型")] = "",
        height: Annotated[str, Field(description="配置栏目高度")] = "是",
        preview_style: Annotated[str, Field(description="预览样式")] = "无预览"
    ) -> Dict[str, Any]:
        """创建一个新的信息流表单
        1.后面标有必填字样的参数需要用户提供，不允许自动生成，其余的不做要求
        2. 先提示用户选择对应的下发渠道，根据下发渠道的不同，再提示用户提供相应的表单填写项
            2.1.如果下发渠道为绘本APK，则频道的可选值只有 绘本 付类类型没有可选值
            2.2.如果下发渠道为少儿小程序，频道、付费类型、栏目高度、预览样式都不需要选择，只需要填写 页面标题 和 页面描述即可
        3. 非必填的参数也需要展示给用户，让用户自行选择是否填写
        

        Args:
            title: 信息流标题 （必填）
            channel_id: 频道,（必填） 可选值有 少儿 教育 健身 电影 广场
            terminal_type: 下发渠道,（必填，优先选择，提供好之后再提示用户提供其他参数） 可选值有 TCL 三星 绘本APK 少儿小程序
            description: 页面描述
            fee_type: 付费类型
            height: 配置栏目高度 是或否 默认为是
            preview_style: 预览样式 无预览 顶端大预览框 上焦小预览框 默认为无预览
        Returns:
            Dict: 包含表单填写结果和预览信息
        """
        try:
            # 必填参数检查
            if not title:
                return {
                    "success": False,
                    "message": "请提示用户输入工具必填参数",
                    "data": {""}
                }
            if not channel_id:
                return {
                    "success": False,
                    "message": "请提示用户输入工具必填参数",
                    "data": {""}
                }
            if not terminal_type:
                return {
                    "success": False,
                    "message": "请提示用户输入工具必填参数",
                    "data": {""}
                }

            logger.info(
                f"开始创建信息流: 标题={title}, 频道={channel_id}, 下发渠道={terminal_type}")

            # 确保浏览器已启动
            if not self.service:
                return {
                    "success": False,
                    "message": "浏览器自动化服务未初始化，请先调用initialize方法",
                    "data": {}
                }

            # 确保浏览器已启动
            await self.service.ensure_browser()

            # 检查页面标题并验证是否为添加页面
            add_page_url = self.config.get("base_url") + "/page/cms-lite-launcher/#/page/addPage"
            success = await navigate_url(self.service, add_page_url, self.username, self.password)
            if not success:
                return {
                    "success": False,
                    "message": "导航到添加页面失败",
                    "data": {}
                }

            # 等待表单元素加载
            await self.service.wait_for_selector("#title", timeout=10000)

            # 填写表单
            form_data = {}

            # 填写标题
            await self.service.fill_form("#title", title)
            form_data["title"] = title

            # 填写描述
            if description:
                # 检查描述输入框是否存在
                if await self.service.page.query_selector("#desc"):
                    await self.service.fill_form("#desc", description)
                    form_data["description"] = description
                else:
                    logger.info("页面上没有描述输入框，跳过填写描述")

            # 填写下拉选择
            select_fields = []
            
            # 只添加有值的字段到待处理列表
            if terminal_type:
                select_fields.append({"id": "terminalType", "value": terminal_type})
            if channel_id:
                select_fields.append({"id": "channelId", "value": channel_id})
            if height:
                select_fields.append({"id": "height", "value": height})
            if preview_style:
                select_fields.append({"id": "previewStyle", "value": preview_style})
            if fee_type:
                select_fields.append({"id": "feeType", "value": fee_type})

            # 填写表单，只处理有值且页面上有对应下拉框的字段
            for field in select_fields:
                # 先检查表单项容器是否存在
                form_item_selector = f"#form-item-{field['id']}"
                field_selector = f"#{field['id']}"
                
                # 尝试多种选择器查找元素
                element_exists = (
                    await self.service.page.query_selector(form_item_selector) or 
                    await self.service.page.query_selector(field_selector) or
                    await self.service.page.query_selector(f".ant-form-item:has(#{field['id']})")
                )
                
                if element_exists:
                    logger.info(f"找到表单项 {field['id']}，准备设置值为 {field['value']}")
                    success = await fill_select(self.service.page, field["id"], field["value"])
                    if success:
                        form_data[field["id"]] = field["value"]
                        logger.info(f"成功设置 {field['id']} = {field['value']}")
                    else:
                        logger.error(f"设置 {field['id']} = {field['value']} 失败")
                else:
                    logger.info(f"页面上找不到表单项 {field['id']}，跳过设置")

            # 保存待提交的表单数据
            self.pending_submission = form_data

            # 根据下发渠道的不同，提示用户不同的操作
            if terminal_type == "绘本APK" or terminal_type == "少儿小程序":
                return {
                    "success": True,
                    "message": "信息流表单已创建成功，请确认信息流内容，如果需要修改，请指出需要修改的内容，若不需要修改，可以直接回复 保存 来操作保存这个信息流表单",
                }
            elif terminal_type == "TCL" or terminal_type == "三星":
                return {
                    "success": True,
                    "message": """信息流表单已创建成功，请确认信息流内容，
                    如果需要修改，请指出需要修改的内容，
                    若不需要修改，可以直接回复 保存信息流 来操作保存这个信息流表单
                    如果您需要为信息流部署工具栏 和 背景图，请直接在页面上进行操作""",
                }
        except Exception as e:
            logger.error(f"创建信息流表单失败 {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"创建信息流表单失败: {str(e)}",
            }

    @tool_method(description="保存信息流")
    async def save_information_flow(
        self,
        action: Annotated[str, Field(description="提交动作")]
    ) -> Dict[str, Any]:
        """提交已经填写完成的信息流表单，可以选择 保存(参数必须由用户提供，不允许自动生成)
        Args:
            action: 提交动作（必须），可选值 保存

        Returns:
            Dict: 提交结果，包含是否成功、信息流ID等信        """
        try:

            # 如果页面有新增栏目 字样，表示当前页面是新增栏目页面，需要先保存栏目
            if "新增栏目" in await self.service.page.content():
                logger.info("当前页面是新增栏目页面，需要先保存栏目")
                return {
                    "status": "failed",
                    "message": "当前页面是新增栏目页面，需要先保存栏目",
                    "data": None
                }
            # 验证action参数
            valid_actions = ["保存", "保存并发"]
            if action not in valid_actions:
                return {
                    "status": "failed",
                    "message": f"无效的动作 {action}，可选 {', '.join(valid_actions)}",
                    "data": None
                }

            # 根据操作类型选择对应的按钮文本
            button_text = "保存并发布" if action == "保存并发布" else "保 存"

            # 使用精确的选择器，优先在卡片额外区域查找按钮
            success = False

            # 1. 尝试通过文本内容直接找到按钮
            selector = f"button:has-text(\"{button_text}\")"
            if await self.service.page.query_selector(selector):
                await self.service.page.click(selector)
                success = True
                logger.info(f"已点击{button_text}按钮")

            # 2. 如果上面失败，尝试在卡片额外区域中查找按钮
            if not success:
                selector = f".ant-card-extra button:has-text(\"{button_text}\")"
                if await self.service.page.query_selector(selector):
                    await self.service.page.click(selector)
                    success = True
                    logger.info(f"已在卡片额外区域点击'{button_text}'按钮")

            # 3. 如果前两种方法都失败，根据位置查找按钮
            if not success:
                if action == "保存":
                    selector = ".ant-card-extra button.ant-btn-primary:nth-child(2)"
                else:
                    selector = ".ant-card-extra button.ant-btn-primary:nth-child(3)"

                if await self.service.page.query_selector(selector):
                    await self.service.page.click(selector)
                    success = True
                    logger.info(f"已通过位置点击'{action}'按钮")

            if not success:
                logger.warning(f"所有方法都未能找到'{action}'按钮")

            # 等待结果提示出现
            success_message_selector = ".ant-message-success, .ant-message-notice"
            error_message_selector = ".ant-message-error"

            # 等待操作结果
            try:
                # 尝试等待成功消息
                await self.service.wait_for_selector(success_message_selector, timeout=10000)
                logger.info("检测到成功提示")
                success = True
                result_message = "操作成功完成"
            except Exception as wait_error:
                # 检查是否有错误消息
                try:
                    await self.service.wait_for_selector(error_message_selector, visible=True, timeout=2000)
                    error_text = await self.service.get_text(error_message_selector)
                    logger.error(f"检测到错误提示: {error_text}")
                    return {
                        "status": "failed",
                        "message": f"提交失败: {error_text}",
                        "data": None
                    }
                except:
                    # 如果两种消息都没有，可能是其他问题
                    logger.error(f"等待操作结果超时: {str(wait_error)}")
                    return {
                        "status": "failed",
                        "message": "提交后等待结果超时，无法确定是否成功",
                        "data": None
                    }
            # 导航到列表页 获取信息流ID
            success = await navigate_url(self.service, self.config.get("base_url") + "/page/cms-lite-launcher/#/page/infoFlow", self.username, self.password)
            if not success:
                return {
                    "status": "failed",
                    "message": "导航到列表页失败",
                    "data": None
                }
            # 获取列表页第一行的信息流ID
            flow_id = await self.service.get_text(".ant-table-row:nth-child(1) .ant-table-cell:nth-child(2)")
            return {
                "status": "success",
                "message": f"""
                表单已保存成功，信息流id为{flow_id}
                接下来您可以：
                查看这个信息流的详情
                添加栏目到这个信息流中
                请告诉我您接下来想要做什么？
            """,
            }
        except Exception as e:
            logger.error(f"提交表单失败: {str(e)}", exc_info=True)
            return {
                "status": "failed",
                "message": f"提交表单失败: {str(e)}",
            }
   
    @tool_method(description="查看信息流详情")
    async def view_flow_detail(
        self,
        contnt_id : Annotated[int, Field(description="信息流ID")]
    ) -> Dict[str, Any]:
        """查看信息流详情（必填参数需要用户提供，不允许自动生成）

        Args:
            contnt_id: 信息流ID(必填)

        Returns:
            None
        """
        try:
            # 导航到信息流编辑页面
            column_url = f"{self.config.get('base_url')}/page/cms-lite-launcher/#/page/addPage?id={contnt_id}"
            logger.info(f"导航到栏目编辑页 {column_url}")

            # 尝试导航，最多重试3次
            success = await navigate_url(self.service, column_url, self.username, self.password)
            if success:
                return {
                    "success": True,
                    "message": "导航到信息流编辑页面成功",
                    "data": {}
                }
            else:
                return {
                    "success": False,
                    "message": "导航到信息流编辑页面失败",
                    "data": {}
                }
            
        except Exception as e:
            logger.error(f"查看信息流详情失败: {str(e)}")
            return {
                "success": False,
                "message": f"查看信息流详情失败: {str(e)}",
                "data": {}
            }

    @tool_method(description="你能做什么")
    async def what_can_I_do(
        self,
    ) -> Dict[str, Any]:
        """你能做什么 client端显示内容时必须包含完整的message，不能省略任何内容
        Returns:
            Dict: 包含工具功能描述
        """
        return {
            "success": True,
            "message": """
            1. 创建或修改信息流
                用法示例：帮我创建一个少儿信息流，标题为“少儿信息流”，频道为“少儿”，下发渠道为“绘本APK”，描述为“少儿信息流描述”，付费类型为“免费”，栏目高度为“是”，预览样式为“无预览”
            2. 查看信息流详情
                用法示例：帮我查看id为355的信息流详情
            3. 获取信息流部署可用的模板
                用法示例：帮我获取信息流部署可用的模板
            4. 为信息流新增栏目（暂不支持含子tab的栏目部署）
                用法示例：
                    不包含子栏目：
                    4.1帮我为id为355的信息流新增一个栏目,栏目标题为“少儿信息流”，频道类型为“少儿”，模板名称为“绘本专属”，开始时间为 现在，结束时间为 下个月十号
                       在部署过程中为栏目添加资源时，支持多个资源一起添加，如媒资形式为“视频”，关键字为“视频ID”，具体值为“rnPNIxRPTT1591761795037,gYJXgbxjpx1591761795038,UXqUNidqxU1591878819508”，此时系统会帮你添加这几个资源到信息流栏目中
                    包含子栏目：
                    4.2帮我为id为355的信息流新增一个栏目,栏目标题为“少儿信息流”，频道类型为“少儿”，模板名称为“绘本专属”，开始时间为 现在，结束时间为 下个月十号，包含两个子栏目
            5. 查询信息流中具体的栏目详情
                用法示例：帮我查询id为355的信息流，栏目标题为蜡笔小新的栏目详情
            6. 为信息流中的栏目替换资源
                用法示例：帮我为id为355的信息流，栏目标题为蜡笔小新的栏目替换第三个资源
            7. 为横排专题添加资源（支持多个一起添加）
                用法示例：帮我为id为12009的专题添加如下资源 视频来源：腾讯 ，视频类型 全部，关键字 视频ID 视频id：tnj10n7kiz4s7gb,u14vapl0xrpnke0,pruuc2jjfxihez0,goasq4eka47dtss），此时会将4个资源添加到对应的横排专题中
            """,
        }
