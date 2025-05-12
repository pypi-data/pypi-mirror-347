"""
横排专题的自动添加资源工具实现
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


class TopicTool(BaseTool):
    """

    提供横排专题的自动添加资源功能
    """

    def __init__(self, config: Dict[str, Any]):
        """初始化工具类

        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.username = config.get("username", "")
        self.password = config.get("password", "")
        self.login_url = config.get("login_url", "")
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

    @tool_method(description="为专题添加资源")
    async def fill_topic_resource(
        self,
        topic_id: Annotated[str, Field(description="专题ID")],
        source: Annotated[str, Field(description="视频来源")],
        type: Annotated[str, Field(description="视频类型")],
        key_word: Annotated[str, Field(description="关键字")],
        keyword_info: Annotated[str, Field(description="关键字信息")]
    ) -> Dict[str, Any]:
        '''
           为专题添加资源 必填的参数需要用户提供，不允许自动生成，必填参数缺少必须暂停，询问用户提供，直到必填参数齐全
        Args:
            topic_id: 专题ID （必须）
            source: 视频来源 （必须） 可选值有 腾讯少儿-【南传牌照】、腾讯少儿- 【未来牌照】、腾讯APK/南传/未来、腾讯、优漫、爱奇艺、芒果
            type: 视频类型 （必须） 可选值有 全部 少儿
            key_word: 关键字 （必须） 可选值有片名 导演 演员  视频id
            keyword_info: 对应具体的片名、导演、演员或视频ID值 （必须）
            如果视频id有多个时，请用逗号隔开（如rnPNIxRPTT1591761795037,gYJXgbxjpx1591761795038,UXqUNidqxU1591878819508）
            此时你需要将keyword_info的值按逗号分割开，每次取一个填充到关键字的输入框
            比如先设为 rnPNIxRPTT1591761795037,添加完第一个视频ID后，再调用工具选择第二个视频ID，依次类推
        Return:
            Dict[str, Any]: 返回结果
        '''
        try:
            # 必填参数校验
            if not topic_id:
                return {
                    "success": False,
                    "message": "专题ID不能为空"
                }
            if not source:
                return {
                    "success": False,
                    "message": "视频来源不能为空"
                }
            if not type:
                return {
                    "success": False,
                    "message": "视频类型不能为空"
                }
            if not key_word:
                return {
                    "success": False,
                    "message": "关键字不能为空"
                }
            if not keyword_info:
                return {
                    "success": False,
                    "message": "关键字信息不能为空"
                }
            # 确保浏览器启动
            success = await self.service.ensure_browser()
            if not success:
                return {
                    "success": False,
                    "message": "浏览器启动失败"
                }
            # 如果当前不在专题页面，则打开专题页面
            edit_modal_selector = '.ant-modal-header:has(.ant-modal-title:has-text("编辑"))'
            edit_modal_exists = await self.service.page.query_selector(edit_modal_selector)
            if not edit_modal_exists:
                url = f"{self.config.get('base_url')}/page/cms-launcher/#/topicManage/topic"
                success = await navigate_url(self.service, url, self.username, self.password)
                if not success:
                    return {
                        "success": False,
                        "message": "打开专题页面失败"
                    }
                # 填写专题id
                await self.service.fill_form("#id", topic_id)

                # 点击查询按键
                await self.service.page.click('button.ant-btn-primary:has-text("查 询")')

                # 等待查询结果加载
                await asyncio.sleep(2)
                
                # 点击编辑草稿
                try:
                    # 使用更宽松的选择器并设置timeout和force参数
                    logger.info("尝试点击编辑草稿按钮")
                    
                    # 方法1：使用更精确的选择器
                    await self.service.page.click('a:has-text("编辑草稿")', 
                                              force=True,      # 强制点击，即使元素不可见
                                              timeout=10000,   # 增加超时时间
                                              no_wait_after=True)  # 不等待导航
                    
                    logger.info("已点击编辑草稿按钮")
                    
                    # 等待页面加载完成
                    await self.service.page.wait_for_load_state('networkidle')
                    logger.info("页面已加载完成")
                except Exception as e:
                    logger.error(f"点击编辑草稿按钮失败: {str(e)}")
                    raise Exception(f"点击编辑草稿按钮失败: {str(e)}")

            # 额外等待以确保界面元素完全渲染
            await asyncio.sleep(1)

            # 等待添加资源按钮出现并可点击
            add_resource_button = await self.service.page.wait_for_selector(
                'button:has-text("添加资源")',
                state='visible',
                timeout=5000
            )

            if add_resource_button:
                # 点击添加资源按钮
                await add_resource_button.click()
                logger.info("已点击添加资源按钮")

                # 等待资源搜索模态框出现
                modal_visible = await self.service.page.wait_for_selector(
                    '.ant-modal-content',
                    state='visible',
                    timeout=5000
                )

                if modal_visible:
                    # 填写资源搜索表单
                    form_success = await self.fill_resource_search_form(source, type, key_word, keyword_info)

                    if form_success:
                        # 选择第一个结果
                        first_result = await self.service.page.query_selector('.ant-modal-content .ant-table-tbody tr:first-child .ant-checkbox-input')
                        if first_result:
                            await first_result.click()
                            logger.info("已选择第一个搜索结果")

                            # 点击确定按钮 - 确保在模态框内点击
                            await self.service.page.click('.ant-modal-content button.ant-btn-primary:has-text("确 定")')
                            logger.info("已点击确定按钮")

                            return {
                                "success": True,
                                "message": "资源添加成功，请询问用户下一次调用fill_topic_resource工具所需要的必填参数，方便进行下一个资源的填充，或询问用户是否需要保存专题，如果需要保存专题，请回复保存，然后调用save_topic工具进行保存"
                            }
                        else:
                            return {
                                "success": False,
                                "message": "未找到可选择的资源结果，请询问用户下一次调用fill_topic_resource工具所需要的必填参数，方便进行下一个资源的填充"
                            }
                    else:
                        return {
                            "success": False,
                            "message": "搜索资源失败"
                        }
                else:
                    return {
                        "success": False,
                        "message": "资源搜索模态框未出现"
                    }
            else:
                return {
                    "success": False,
                    "message": "未找到添加资源按钮"
                }

        except Exception as e:
            logger.error(f"添加资源过程出错: {str(e)}")
            return {
                "success": False,
                "message": f"添加资源失败: {str(e)}"
            }

    async def fill_resource_search_form(self, source, type_value, key_word, keyword_info):
        """填写资源搜索表单

        Args:
            source: 视频来源，例如"腾讯少儿-【南传牌照】"等
            type_value: 视频类型，例如"全部"、"少儿"等
            key_word: 关键字类型，例如"片名"、"导演"等
            keyword_info: 关键字内容，要搜索的具体内容

        Returns:
            bool: 表单填写和搜索是否成功
        """
        try:
            logger.info("开始填写资源搜索表单")

            # 1. 设置视频来源
            if source and source != "腾讯少儿-【南传牌照】":  # 判断是否需要修改默认值
                logger.info(f"设置视频来源: {source}")
                # 点击视频来源下拉框
                await self.service.page.click('#licenceId')
                await asyncio.sleep(1)  # 增加等待时间确保下拉框完全显示
                
                # 为不同的视频来源值设置不同的处理方式
                if source == "腾讯":
                    # 根据前端HTML可以看到"腾讯"是第4个选项（索引为3）
                    # 使用基于索引的方式直接选择第4个选项
                    await self.service.page.click('.ant-select-dropdown-menu-item:nth-child(4)')
                    logger.info(f"使用索引方式选择了视频来源: 腾讯（第4个选项）")
                else:
                    # 对于其他选项，使用精确的文本匹配方式
                    # 使用nth-child方式按照选项顺序一一对应
                    if source == "腾讯少儿-【南传牌照】":
                        await self.service.page.click('.ant-select-dropdown-menu-item:nth-child(1)')
                    elif source == "腾讯少儿-【未来牌照】":
                        await self.service.page.click('.ant-select-dropdown-menu-item:nth-child(2)')
                    elif source == "腾讯APK/南传/未来":
                        await self.service.page.click('.ant-select-dropdown-menu-item:nth-child(3)')
                    elif source == "爱奇艺":
                        await self.service.page.click('.ant-select-dropdown-menu-item:nth-child(5)')
                    elif source == "芒果":
                        await self.service.page.click('.ant-select-dropdown-menu-item:nth-child(6)')
                    elif source == "腾讯VOD":
                        await self.service.page.click('.ant-select-dropdown-menu-item:nth-child(7)')
                    else:
                        # 其他选项仍然尝试用文本匹配
                        source_option = f'.ant-select-dropdown-menu-item:has-text("{source}")'
                        await self.service.page.click(source_option, timeout=3000)
                    
                    logger.info(f"已选择视频来源: {source}")
                
                await asyncio.sleep(0.5)

            # 2. 设置视频类型
            if type_value and type_value != "全部":  # 判断是否需要修改默认值
                logger.info(f"设置视频类型: {type_value}")
                # 点击视频类型下拉框
                await self.service.page.click('#type')
                await asyncio.sleep(0.5)
                
                # 选择下拉选项
                type_option = f'.ant-select-dropdown-menu-item:has-text("{type_value}")'
                await self.service.page.click(type_option, timeout=3000)
                logger.info(f"已选择视频类型: {type_value}")
                await asyncio.sleep(0.5)

            # 3. 设置关键字类型
            if key_word and key_word != "片名":  # 判断是否需要修改默认值
                logger.info(f"设置关键字类型: {key_word}")
                # 点击关键字下拉框
                await self.service.page.click('#keyword')
                await asyncio.sleep(0.5)
                
                # 选择下拉选项
                keyword_option = f'.ant-select-dropdown-menu-item:has-text("{key_word}")'
                await self.service.page.click(keyword_option, timeout=3000)
                logger.info(f"已选择关键字类型: {key_word}")
                await asyncio.sleep(0.5)

            # 4. 填写关键字信息
            if keyword_info:
                logger.info(f"填写关键字信息: {keyword_info}")
                await self.service.page.fill('#search', keyword_info)

            # 5. 点击查询按钮 - 确保在资源搜索模态框内点击查询按钮
            logger.info("点击查询按钮")
            # 在模态框内查找查询按钮
            modal_query_button = '.ant-modal-content button.ant-btn-primary:has-text("查 询")'
            await self.service.page.click(modal_query_button, timeout=3000)
            logger.info("已点击查询按钮")

            # 等待查询结果加载
            await asyncio.sleep(2)

            # 判断是否有查询结果 - 在模态框内检查表格
            has_results = await self.service.page.query_selector('.ant-modal-content .ant-table-tbody tr')
            if has_results:
                logger.info("查询结果已加载")
                return True
            else:
                logger.warning("未找到查询结果")
                return False

        except Exception as e:
            logger.error(f"填写资源搜索表单出错: {str(e)}")
            return False
        
    @tool_method(description="保存专题")
    async def save_topic(self):
        '''
            保存专题
        '''
        try:
            # 点击保存按钮
            await self.service.page.click('button.ant-btn-primary:has-text("保存草稿")')
            logger.info("已点击保存草稿按钮")
            return {
                "success": True,
                "message": "专题保存成功"
            }
        except Exception as e:
            logger.error(f"保存专题出错: {str(e)}")
            return {
                "success": False,
                "message": f"保存专题失败: {str(e)}"
            }
