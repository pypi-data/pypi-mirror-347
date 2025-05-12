import wmi
import pythoncom
import time
from typing import Callable, Dict, Any, Optional
import winreg
import re
from datetime import datetime
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class USBEventMonitor:
    """USB设备事件监控器"""

    # 类常量定义
    SEPARATOR = '=' * 60
    # 定义可能的附加字段
    REAL_ID_FIELD = "实际设备ID"
    LOCATION_FIELD = "设备位置"
    DEVICE_ATTRIBUTES = [
        'Caption', 'ClassGuid', 'ConfigManagerErrorCode',
        'ConfigManagerUserConfig', 'CreationClassName', 'Description',
        'Manufacturer', 'Name', 'PNPClass', 'PNPDeviceID',
        'Present', 'Service', 'Status', 'SystemCreationClassName',
        'SystemName'
    ]
    LIST_ATTRIBUTES = ['CompatibleID', 'HardwareID']

    def __init__(self,
                 on_connect: Optional[Callable[[Dict[str, Any]], None]] = None,
                 on_disconnect: Optional[Callable[[Dict[str, Any]], None]] = None,
                 check_interval: float = 0.2,
                 enable_print: bool = False,
                 enable_real_id: bool = True,
                 enable_location: bool = False):
        """
        初始化USB监控器
        :param on_connect: USB设备连接时的回调函数
        :param on_disconnect: USB设备断开时的回调函数
        :param check_interval: 检查间隔时间(秒)
        :param enable_print: 是否打印设备信息
        :param enable_real_id: 是否获取实际设备ID
        :param enable_location: 是否获取设备位置信息
        """
        self._on_connect = on_connect
        self._on_disconnect = on_disconnect
        self._is_running = False
        self._check_interval = max(0.1, check_interval)  # 确保最小间隔
        self._enable_print = enable_print
        self._enable_real_id = enable_real_id
        self._enable_location = enable_location
        self._device_info_cache = {}
        self._device_id_pattern = re.compile(r'Dependent.*?DeviceID=\\"([^"]+)\\"')

        # 根据参数设置基本字段
        self._basic_fields = {"设备ID"}
        if enable_real_id:
            self._basic_fields.add(self.REAL_ID_FIELD)
        if enable_location:
            self._basic_fields.add(self.LOCATION_FIELD)

    def _get_device_info(self, device_id: str, device_obj: Any = None) -> Dict[str, Any]:
        """获取USB设备信息"""
        # 只有在没有新设备对象时才使用缓存
        if device_obj is None and device_id in self._device_info_cache:
            return self._device_info_cache[device_id].copy()

        if not device_id:
            return {"设备ID": "未知设备"}

        # 基本信息
        info = {"设备ID": device_id}

        # 获取实际设备ID
        real_id = ''
        if self._enable_real_id:
            real_id = self._get_real_device_id(device_id)
            if real_id:
                info[self.REAL_ID_FIELD] = real_id

        # 获取设备位置信息
        if self._enable_location and real_id:
            location = self._get_device_location(device_id, real_id)
            if location:
                info[self.LOCATION_FIELD] = location

        # 添加设备对象的属性
        if device_obj is not None:
            # 处理列表类型的属性
            for list_attr in self.LIST_ATTRIBUTES:
                if hasattr(device_obj, list_attr):
                    attr_value = getattr(device_obj, list_attr)
                    if attr_value:
                        info[list_attr] = ', '.join(attr_value)

            # 处理其他属性
            for attr in self.DEVICE_ATTRIBUTES:
                if value := getattr(device_obj, attr, ''):
                    info[attr] = value

            # 缓存设备信息
            self._device_info_cache[device_id] = info.copy()

        return info

    def _get_real_device_id(self, device_path: str) -> str:
        """只获取实际设备ID，不获取位置信息"""
        try:
            # 快速检查路径格式是否有效
            if not device_path:
                return ''
            if device_path.count('&') != 1:
                return ''
            parts = device_path.split("\\")
            device_id = parts[-1]
            # 如果设备ID是纯数字，直接返回，不需要查询注册表
            if device_id.isdigit():
                return device_id
            # 构造注册表路径
            reg_path = "SYSTEM\\CurrentControlSet\\Enum\\" + "\\".join(parts[:-1])

            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ) as key:
                # 获取实际设备ID - 修复设备ID大小写问题（性能优化版）
                # 首先尝试直接使用设备ID
                real_id = device_id

                try:
                    # 尝试直接打开设备键，这是最快的方法
                    try:
                        with winreg.OpenKey(key, device_id) as _:
                            pass  # 如果能打开，说明ID正确
                    except WindowsError:
                        # 如果直接打开失败，尝试大小写不敏感的匹配
                        # 使用有限的枚举来提高性能，大多数情况下只有几个键
                        device_id_upper = device_id.upper()
                        found_match = False

                        # 限制枚举的数量，避免遍历过多键
                        for i in range(5):  # 大多数情况下，设备键数量很少
                            try:
                                reg_key = winreg.EnumKey(key, i)
                                if reg_key.upper() == device_id_upper:
                                    real_id = reg_key  # 使用注册表中的实际大小写
                                    found_match = True
                                    break
                            except WindowsError:
                                break  # 没有更多的键
                        # 如果仍然没有找到匹配项，尝试使用第一个可用的键
                        if not found_match:
                            try:
                                real_id = winreg.EnumKey(key, 0)
                            except WindowsError:
                                return ''  # 如果无法获取任何键，返回空
                except WindowsError:
                    return ''  # 如果无法访问注册表，返回空

                return real_id
        except (WindowsError, ValueError, IndexError):
            return ''

    def _get_device_location(self, device_path: str, real_id: str) -> str:
        """只获取设备位置信息"""
        try:
            # 快速检查路径格式是否有效
            if not device_path or not real_id:
                return ''
            if device_path.count('&') != 1:
                logger.debug(f"无效的设备路径: {device_path}")
                return ''
            parts = device_path.split("\\")
            # 构造注册表路径
            reg_path = "SYSTEM\\CurrentControlSet\\Enum\\" + "\\".join(parts[:-1])

            # 获取位置信息
            try:
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ) as key:
                    with winreg.OpenKey(key, real_id) as dev_key:
                        try:
                            loc = winreg.QueryValueEx(dev_key, 'LocationInformation')[0]
                            # 使用更快的字符串处理方法
                            first_hash = loc.find('#') + 1
                            if first_hash > 0:
                                first_dot = loc.find('.', first_hash)
                                if first_dot > first_hash:
                                    last_hash = loc.rfind('#') + 1
                                    if last_hash > 0:
                                        # 直接使用切片和强制转换，避免异常
                                        try:
                                            hub = int(loc[first_hash:first_dot])
                                            port = int(loc[last_hash:])
                                            return f"{port}-{hub}"
                                        except (ValueError, IndexError):
                                            pass
                            # 如果上面的解析失败，返回原始位置信息
                            return loc
                        except WindowsError:
                            return ''  # 返回空位置信息
            except WindowsError:
                return ''  # 返回空位置信息
        except (WindowsError, ValueError, IndexError):
            return ''

    def _get_usb_location(self, device_path: str) -> tuple[str, str]:
        """获取USB设备ID和位置信息

        注意：这是一个兼容旧版接口的方法。对于新代码，建议使用以下方法：
        - _get_real_device_id(): 只获取实际设备ID
        - _get_device_location(): 只获取设备位置信息
        """
        # 首先获取实际设备ID
        real_id = self._get_real_device_id(device_path)
        if not real_id:
            return '', ''

        # 然后获取位置信息
        location = self._get_device_location(device_path, real_id)
        return real_id, location

    def _notify_event(self, info: Dict[str, Any], event_type: str) -> None:
        """通知事件（打印信息和调用回调）"""
        if self._enable_print:
            # 预先构建输出信息
            output_lines = [
                self.SEPARATOR,
                f"USB设备{event_type}",
                self.SEPARATOR
            ]

            # 添加基本信息
            for key in self._basic_fields:
                if value := info.get(key):
                    output_lines.append(f"{key:15}: {value}")

            # 添加其他信息
            other_info = sorted((k, v) for k, v in info.items()
                                if k not in self._basic_fields and v)
            if other_info:
                for key, value in other_info:
                    output_lines.append(f"{key:15}: {value}")

            output_lines.append(self.SEPARATOR)

            # 一次性打印所有信息
            logger.info('\n'.join(output_lines))

        # 调用回调函数
        callback = self._on_connect if event_type == "连接" else self._on_disconnect
        if callback is not None:
            try:
                callback(info)
            except Exception as e:
                if self._enable_print:
                    logger.error(f"回调函数执行出错: {e}")

    def _get_current_time(self) -> str:
        """获取当前时间的格式化字符串"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _handle_connect(self, device_id: str, device_obj: Any = None) -> None:
        """处理设备连接事件"""
        try:
            # 确保设备ID格式正确
            device_id = device_id.replace('\\\\', '\\')
            info = self._get_device_info(device_id, device_obj)
            info["状态"] = "已连接"
            info["添加时间"] = self._get_current_time()
            self._notify_event(info, "连接")
        except Exception as e:
            if self._enable_print:
                logger.error(f"处理设备事件时出错: {e}")

    def _extract_device_id(self, usb_info: str) -> str:
        """从USB信息字符串中提取设备ID"""
        try:
            if match := self._device_id_pattern.search(usb_info):
                device_id = match.group(1)
                # 确保设备ID格式正确
                return device_id.replace('\\\\', '\\')
            return ""
        except Exception:
            return ""

    def _handle_disconnect(self, usb_info: str) -> None:
        """处理设备断开事件"""
        try:
            device_id = self._extract_device_id(usb_info)
            # 确保设备ID格式正确
            device_id = device_id.replace('\\\\', '\\')
            if device_id in self._device_info_cache:
                info = self._device_info_cache[device_id].copy()
                info["状态"] = "已断开"
                info["断开时间"] = self._get_current_time()
                self._notify_event(info, "断开")
                self._device_info_cache.pop(device_id, None)
            else:
                info = {
                    "设备ID": device_id,
                    "状态": "已断开",
                    "断开时间": self._get_current_time()
                }
                self._notify_event(info, "断开")
        except Exception as e:
            if self._enable_print:
                logger.error(f"处理设备事件时出错: {e}")

    def start(self) -> None:
        """启动监控"""
        if self._is_running:
            return

        if self._enable_print:
            logger.info("USB监控已启动...\n按Ctrl+C停止监控...")

        self._is_running = True

        try:
            pythoncom.CoInitialize()
            wmi_obj = wmi.WMI()
            watcher = wmi_obj.watch_for(
                raw_wql=f"SELECT * FROM __InstanceOperationEvent WITHIN {self._check_interval} "
                        "WHERE TargetInstance ISA 'Win32_USBControllerDevice'"
            )
            logger.info('USB监控已启动')
            while self._is_running:
                try:
                    usb = watcher()
                    if not usb:
                        continue

                    if usb.event_type == 'creation' and hasattr(usb, 'Dependent'):
                        device_id = usb.Dependent.DeviceID
                        self._handle_connect(device_id, usb.Dependent)
                    elif usb.event_type == 'deletion':
                        self._handle_disconnect(str(usb))

                except Exception as e:
                    if self._enable_print:
                        logger.error(f"USB监控过程出错: {e}")
                    time.sleep(0.1)
        except Exception as e:
            if self._enable_print:
                logger.error(f"USB监控初始化错误: {e}")
        finally:
            self.stop()

    def stop(self) -> None:
        """停止监控"""
        if not self._is_running:
            return

        self._is_running = False
        self._device_info_cache.clear()  # 清除缓存

        if self._enable_print:
            logger.info("USB监控已停止")


def main():
    """演示使用方法"""

    def on_connect(info: Dict[str, Any]) -> None:
        """设备连接回调示例"""
        device_id = info.get('设备ID', '未知设备')
        logger.info(f"自定义处理 - 设备已连接: {device_id}")

    def on_disconnect(info: Dict[str, Any]) -> None:
        """设备断开回调示例"""
        device_id = info.get('设备ID', '未知设备')
        logger.info(f"自定义处理 - 设备已断开: {device_id}")

    # 创建监控器（启用打印功能）
    monitor = USBEventMonitor(
        on_connect=on_connect,
        on_disconnect=on_disconnect,
        check_interval=0.4,  # 使用0.4秒的检查间隔
        enable_print=True,  # 演示时启用打印
        enable_real_id=True,  # 启用实际设备ID获取
        enable_location=True  # 启用设备位置获取
    )

    # 不同配置的示例：
    # 只获取实际设备ID，不获取位置信息
    # monitor = USBEventMonitor(
    #     enable_real_id=True,
    #     enable_location=False
    # )

    # 不获取实际设备ID和位置信息，最高性能模式
    # monitor = USBEventMonitor(
    #     enable_real_id=False,
    #     enable_location=False
    # )
    
    try:
        monitor.start()
    except KeyboardInterrupt:
        logger.info("用户中断，停止监控")
    finally:
        monitor.stop()


if __name__ == "__main__":
    main()
