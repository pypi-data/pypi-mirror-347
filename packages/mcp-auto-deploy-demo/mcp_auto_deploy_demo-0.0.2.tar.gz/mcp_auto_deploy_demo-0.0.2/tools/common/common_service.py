
"""
公共服务方法
包含处理日期、选择框以及导航URL等常用方法
"""
import logging
import asyncio
import re
from typing import Dict, Any
from datetime import datetime, timedelta
import traceback

logger = logging.getLogger(__name__)

async def set_date_range(page, selector: str, start_datetime: str, end_datetime: str) -> None:
    """设置日期范围选择器的值

    Args:
        page: Playwright页面对象
        selector: 日期范围选择器
        start_datetime: 开始日期时间值，格式：YYYY-MM-DD HH:mm:ss
        end_datetime: 结束日期时间值，格式：YYYY-MM-DD HH:mm:ss
    """
    try:
        logger.info(f"设置日期范围: {start_datetime} - {end_datetime}")

        # 点击日期范围选择器，打开日期选择面板
        await page.click(selector)
        await asyncio.sleep(0.5)  # 等待日期选择面板显示

        # 设置开始时间
        await page.fill('.ant-picker-input-active input', start_datetime)
        await asyncio.sleep(0.5)

        # 点击确定按钮完成开始时间选择
        confirm_button = '.ant-btn-primary:has-text("确 定")'
        await page.click(confirm_button)
        logger.info("已点击日期选择器的确定按钮，完成开始时间选择")
        await asyncio.sleep(0.5)

        # 此时会自动跳转到结束时间选择
        # 设置结束时间
        await page.fill('.ant-picker-input-active input', end_datetime)
        await asyncio.sleep(0.5)

        # 再次点击确定按钮完成整个日期范围选择
        await page.click(confirm_button)
        logger.info("已点击日期选择器的确定按钮，完成结束时间选择")
        await asyncio.sleep(0.5)

        # 如果日期选择器仍然可见，点击空白处关闭
        try:
            date_picker_visible = await page.query_selector('.ant-picker-dropdown:visible')
            if date_picker_visible:
                await page.click('body', position={"x": 10, "y": 10})
        except Exception as e:
            logger.warning(f"尝试关闭日期选择器时出错: {str(e)}")

        logger.info(f"已设置日期范围 {selector}: {start_datetime} - {end_datetime}")
    except Exception as e:
        logger.error(f"设置日期范围失败 {selector}: {e}")
        # 尝试点击页面其他位置关闭日期选择面板
        try:
            await page.click("body", position={"x": 0, "y": 0})
        except:
            pass

async def fill_select(page, select_id: str, option_text: str) -> bool:
    """填写下拉选择
    Args:
        page: Playwright页面对象
        select_id: 下拉框的ID
        option_text: 要选择的选项文本

    Returns:
        bool: 操作是否成功
    """
    try:
        # 构建选择器，使用更精确的选择
        selector = f"#{select_id} + .ant-select-selection-search-input, #{select_id}"

        # 首先尝试确保元素可见并滚动到视图
        await page.wait_for_selector(selector, state='visible', timeout=5000)
        try:
            element = await page.query_selector(selector)
            if element:
                # 先滚动到元素位置，减少页面跳动
                await element.scroll_into_view_if_needed()
                await asyncio.sleep(0.5)
        except Exception as e:
            logger.warning(f"滚动到元素位置失败: {e}")

        # 等待一下，确保页面稳定
        await asyncio.sleep(0.5)

        # 使用强制点击策略，避免被其他元素遮挡
        try:
            # 查找下拉框所在的父元素，使用更可靠的方式点击
            container_selector = f".ant-select:has(#{select_id})"
            await page.click(container_selector, force=True)
        except Exception as e:
            logger.warning(f"使用选择{container_selector} 点击失败: {e}")
            # 回退到直接点击原始元素
            await page.click(selector, force=True)

        # 等待下拉选项出现
        dropdown_selector = ".ant-select-dropdown:not(.ant-select-dropdown-hidden)"
        await page.wait_for_selector(dropdown_selector, state='visible', timeout=5000)

        # 给足够时间让下拉菜单完全展开
        await asyncio.sleep(1)

        # 查找并点击指定选项（使用更精确的匹配方式）
        option_selector = f'.ant-select-item-option-content:text-is("{option_text}")'
        try:
            await page.click(option_selector, timeout=5000)
        except Exception as e:
            logger.warning(f"精确匹配选项失败: {e}, 尝试模糊匹配")
            # 使用模糊匹配
            option_selector = f'.ant-select-item-option-content:has-text("{option_text}")'
            await page.click(option_selector, timeout=5000)

        # 等待下拉菜单关闭
        await asyncio.sleep(0.5)

        logger.info(f"已选择 {select_id}: {option_text}")
        return True
    except Exception as e:
        logger.error(f"选择下拉选项失败 {select_id}: {e}")
        # 尝试关闭可能仍打开的下拉菜单
        try:
            await page.keyboard.press("Escape")
        except:
            pass
        return False

async def login_to_system(service, username :str, password :str) -> Dict[str, Any]:
    """执行单独的登录操作，登录到系统
    Args:
        service: PlaywrightService实例
        username: 用户名
        password: 密码
        
    Returns:
        登录结果
    """
    try:
        # 检查是否已初始化
        if not service:
            logger.error("服务未初始化")
            return {
                "success": False,
                "message": "服务未初始化",
            }

        # 检查是否已登录
        if service.is_logged_in:
            logger.info("已登录，跳过登录操作")
            return {
                "success": True,
                "message": "已登录，跳过登录操作",
            }

        # 检查用户名和密码
        if not username or not password:
            return {
                "success": False,
                "message": "未配置用户名或密码",
                "data": {
                    "username": bool(username),
                    "password": bool(password)
                }
            }

        logger.info("开始启动浏览器...")
        # 设置浏览器为可见模式
        service.headless = False

        # 确保浏览器已启动
        browser_started = False
        max_browser_retries = 3

        for attempt in range(max_browser_retries):
            try:
                logger.info(f"{attempt + 1} 次尝试启动浏览器")
                browser_started = await service.ensure_browser()
                if browser_started:
                    logger.info("浏览器启动成功")
                    break
                else:
                    logger.warning(f"{attempt + 1} 次启动浏览器失败，准备重试")
                    await asyncio.sleep(2)
            except Exception as e:
                logger.error(f"{attempt + 1} 次启动浏览器出错: {str(e)}")
                if attempt < max_browser_retries - 1:
                    await asyncio.sleep(2)
                else:
                    return {
                        "success": False,
                        "message": f"多次尝试启动浏览器均失败: {str(e)}",
                        "data": {"error": str(e)}
                    }

        if not browser_started:
            return {
                "success": False,
                "message": "浏览器启动失败，请检查系统环境",
                "data": {}
            }

        # 直接导航到登录页
        login_url = service.config.get("login_url", "")
        logger.info(f"导航到登录页 {login_url}")

        # 尝试导航到登录页
        max_retries = 3
        success = False

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"导航到登录页面尝试 {attempt}/{max_retries}")
                await service.page.goto(login_url, wait_until='networkidle')
                success = True
                break
            except Exception as e:
                logger.error(f"导航到登录页面尝试 {attempt} 失败: {e}")

                if attempt < max_retries:
                    logger.info("等待2秒后重试")
                    await asyncio.sleep(2)
                    # 如果浏览器可能已关闭，尝试重新启动
                    await service.ensure_browser()

        if not success:
            return {
                "success": False,
                "message": "无法导航到登录页面，请检查网络连接",
                "data": {}
            }

        # 执行登录
        login_success = await service.login()

        if login_success:
            # 检查当前URL，确认登录是否成功
            current_url = service.page.url
            page_content = await service.extract_text_content()
            page_title = await service.page.title()

            # 登录成功的文本指示器
            success_indicators = ["登录成功", "登陆成功",
                                "login success", "登录中央认证系统", "您已经成功登录"]
            has_success_text = any(
                indicator in page_content for indicator in success_indicators)

            # 即使URL仍包含login，但如果页面内容包含成功提示，也认为登录成功
            if "login" in current_url.lower() and not has_success_text:
                # 如果还在登录页面，且没有成功提示，可能登录失败
                return {
                    "success": False,
                    "message": f"登录可能失败，仍然位于登录相关页面且没有成功提示: {current_url}",
                    "data": {"current_url": current_url}
                }
            # 如果页面包含 正在未信任的设备上登录 表示需要用户输入验证码，直接返回输入验证码的提示
            if "正在未信任的设备上登录" in page_content:
                return {
                    "success": False,
                    "message": "登录需要输入验证码，请在浏览器中输入验证码后再尝试"
                }

            # 记录登录状态
            service.is_logged_in = True

            # 记录成功指示
            success_message = "登录成功"
            if has_success_text:
                success_message = f"登录成功，页面显示成功提示: {page_title}"

            return {
                "success": True,
                "message": success_message,
                "data": {
                    "current_url": current_url,
                    "page_title": page_title,
                    "has_success_text": has_success_text
                }
            }
        else:
            return {
                "success": False,
                "message": "登录失败，请检查用户名和密码",
                "data": {
                    "username_provided": bool(username),
                    "password_provided": bool(password)
                }
            }
    except Exception as e:
        logger.error(f"登录过程出错: {str(e)}", exc_info=True)
        return {
            "success": False,
            "message": f"登录过程出错: {str(e)}",
            "data": {
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        }

async def navigate_url(service, url: str, username: str, password: str) -> bool:
    """导航到指定URL
    Args:
        service: PlaywrightService实例
        url: 目标URL
        username: 用户名
        password: 密码
        
    Returns:
        bool: 导航是否成功
    """
    try:
        if not service:
            raise RuntimeError("浏览器自动化服务未初始化")

        # 确保浏览器已启动
        if not await service.ensure_browser():
            return False
        # 尝试导航，最多重试3次
        success = False
        max_retries = 3

        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"导航尝试 {attempt}/{max_retries}")
                success = await service.navigate_to(url)
                # 如果页面提示需要登录，则先登录
                if "登录" in await service.page.content():
                    logger.info("页面提示需要登录，先登录")
                    # 这里需要工具类提供用户名和密码
                    result = await login_to_system(service, username, password)
                    if not result["success"]:
                        return False
                # 等待页面加载完成
                await asyncio.sleep(2)
                if success:
                    return True

            except Exception as e:
                logger.error(f"导航尝试{attempt}出错: {str(e)}")
            if attempt < max_retries:
                await asyncio.sleep(2)

        # 尝试导航到目标页面
        logger.info(f"登录后导航到目标页面: {url}")

        return success
            
    except Exception as e:
        logger.error(f"导航过程出错: {str(e)}", exc_info=True)
        return False