import math
import os
import wikipedia
import datetime
import urllib.request
import urllib.parse
import re


def calculator(expression: str) -> str:
    """计算数学表达式。参数: expression (str) - 数学表达式，如 '2 + 3 * 4' 或 'math.sqrt(16)'。返回计算结果字符串。"""
    try:
        allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
        allowed["__builtins__"] = {}
        result = eval(expression, allowed)
        return str(result)
    except Exception as e:
        return f"计算错误: {e}"


def wikipedia_search(query: str, sentences: int = 3) -> str:
    """搜索维基百科并返回摘要。参数: query (str) - 搜索关键词；sentences (int, 可选) - 返回的句子数，默认3。返回词条摘要字符串。"""
    try:
        wikipedia.set_lang("zh")
        summary = wikipedia.summary(query, sentences=sentences, auto_suggest=True)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        try:
            summary = wikipedia.summary(e.options[0], sentences=sentences)
            return f"(已选择最相关词条: {e.options[0]})\n{summary}"
        except Exception:
            return f"词条有歧义，候选项: {', '.join(e.options[:5])}"
    except wikipedia.exceptions.PageError:
        wikipedia.set_lang("en")
        try:
            summary = wikipedia.summary(query, sentences=sentences, auto_suggest=True)
            return f"(中文词条未找到，显示英文结果)\n{summary}"
        except Exception as e2:
            return f"未找到相关词条: {e2}"
    except Exception as e:
        return f"搜索错误: {e}"


def file_tool(action: str, filepath: str, content: str = "") -> str:
    """读写本地文件。参数: action (str) - 操作类型，'read' 读取或 'write' 写入；filepath (str) - 文件路径；content (str, 可选) - 写入时的内容。返回操作结果字符串。"""
    try:
        if action == "read":
            if not os.path.exists(filepath):
                return f"文件不存在: {filepath}"
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        elif action == "write":
            dir_path = os.path.dirname(filepath)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return f"已成功写入文件: {filepath}"
        else:
            return f"未知操作: {action}，请使用 'read' 或 'write'"
    except Exception as e:
        return f"文件操作错误: {e}"


def get_current_time(timezone: str = "Asia/Shanghai") -> str:
    """获取当前日期和时间。参数: timezone (str, 可选) - 时区名称，默认为 'Asia/Shanghai'（北京时间）。返回当前时间字符串。"""
    try:
        now = datetime.datetime.now()
        result = now.strftime("%Y年%m月%d日 %H:%M:%S")
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        weekday = weekdays[now.weekday()]
        return f"当前时间：{result}，{weekday}"
    except Exception as e:
        return f"获取时间失败: {e}"


def unit_converter(value: float, from_unit: str, to_unit: str) -> str:
    """单位换算工具。参数: value (float) - 数值；from_unit (str) - 原单位；to_unit (str) - 目标单位。支持长度(m/km/cm/mm/inch/foot/mile)、重量(kg/g/lb/oz)、温度(celsius/fahrenheit/kelvin)。"""
    try:
        from_unit = from_unit.lower().strip()
        to_unit = to_unit.lower().strip()

        # 长度换算（统一到米）
        length_to_meter = {
            "m": 1, "meter": 1, "meters": 1, "米": 1,
            "km": 1000, "kilometer": 1000, "kilometers": 1000, "千米": 1000, "公里": 1000,
            "cm": 0.01, "centimeter": 0.01, "厘米": 0.01,
            "mm": 0.001, "millimeter": 0.001, "毫米": 0.001,
            "inch": 0.0254, "inches": 0.0254, "英寸": 0.0254,
            "foot": 0.3048, "feet": 0.3048, "ft": 0.3048, "英尺": 0.3048,
            "mile": 1609.344, "miles": 1609.344, "英里": 1609.344,
        }
        # 重量换算（统一到千克）
        weight_to_kg = {
            "kg": 1, "kilogram": 1, "kilograms": 1, "千克": 1, "公斤": 1,
            "g": 0.001, "gram": 0.001, "grams": 0.001, "克": 0.001,
            "lb": 0.453592, "lbs": 0.453592, "pound": 0.453592, "pounds": 0.453592, "磅": 0.453592,
            "oz": 0.0283495, "ounce": 0.0283495, "ounces": 0.0283495, "盎司": 0.0283495,
        }

        if from_unit in length_to_meter and to_unit in length_to_meter:
            result = value * length_to_meter[from_unit] / length_to_meter[to_unit]
            return f"{value} {from_unit} = {round(result, 6)} {to_unit}"

        if from_unit in weight_to_kg and to_unit in weight_to_kg:
            result = value * weight_to_kg[from_unit] / weight_to_kg[to_unit]
            return f"{value} {from_unit} = {round(result, 6)} {to_unit}"

        # 温度换算
        temp_units = {"celsius", "fahrenheit", "kelvin", "摄氏度", "华氏度", "开尔文", "c", "f", "k"}
        if from_unit in temp_units and to_unit in temp_units:
            # 先转成摄氏度
            if from_unit in ("fahrenheit", "华氏度", "f"):
                celsius = (value - 32) * 5 / 9
            elif from_unit in ("kelvin", "开尔文", "k"):
                celsius = value - 273.15
            else:
                celsius = value
            # 再从摄氏度转目标
            if to_unit in ("fahrenheit", "华氏度", "f"):
                result = celsius * 9 / 5 + 32
            elif to_unit in ("kelvin", "开尔文", "k"):
                result = celsius + 273.15
            else:
                result = celsius
            return f"{value} {from_unit} = {round(result, 4)} {to_unit}"

        return f"不支持的单位换算: {from_unit} → {to_unit}"
    except Exception as e:
        return f"换算错误: {e}"


def web_fetch(url: str) -> str:
    """抓取网页内容并返回纯文本。参数: url (str) - 网页URL，如 'https://example.com'。返回网页的纯文本内容（最多2000字）。"""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; AIAgent/1.0)"}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read()
            encoding = response.headers.get_content_charset() or "utf-8"
            html = raw.decode(encoding, errors="replace")

        # 去除脚本和样式
        html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL | re.IGNORECASE)
        # 去除所有HTML标签
        text = re.sub(r"<[^>]+>", " ", html)
        # 清理多余空白
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) > 2000:
            text = text[:2000] + "...(内容已截断)"
        return text if text else "页面内容为空"
    except Exception as e:
        return f"网页抓取失败: {e}"


TOOL_REGISTRY = {
    "calculator": calculator,
    "wikipedia_search": wikipedia_search,
    "file_tool": file_tool,
    "get_current_time": get_current_time,
    "unit_converter": unit_converter,
    "web_fetch": web_fetch,
}
