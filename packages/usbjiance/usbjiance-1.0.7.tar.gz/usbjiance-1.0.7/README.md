# USB设备监控工具 v1.0.7

一个高性能的Windows USB设备监控工具，用于实时检测USB设备的插入和移除。

## 功能特点

- 实时监测USB设备的插拔事件
- 获取USB设备的详细信息，包括设备ID、制造商、设备名称等
- 支持获取设备的实际ID和物理位置信息
- 支持自定义事件回调函数
- 高性能设计，占用系统资源少
- 标准日志输出，方便集成到其他系统
- 可排除特定类型的设备服务（如磁盘等）

## 安装方法

```bash
pip install usbjiance
```

## 快速开始

基本用法示例：

```python
from usbjiance import USBEventMonitor
import time

# 定义回调函数
def on_connect(info):
    print(f"设备已连接: {info.get('设备ID')}")
    
def on_disconnect(info):
    print(f"设备已断开: {info.get('设备ID')}")

# 创建监控器实例
monitor = USBEventMonitor(
    on_connect=on_connect,
    on_disconnect=on_disconnect,
    enable_print=True  # 启用日志打印
)

# 在主线程中启动监控
try:
    monitor.start()
except KeyboardInterrupt:
    # 处理Ctrl+C中断
    pass
finally:
    # 确保正确停止监控
    monitor.stop()
```

## 配置选项

`USBEventMonitor`类接受以下参数：

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| on_connect | Callable | None | USB设备连接时的回调函数 |
| on_disconnect | Callable | None | USB设备断开时的回调函数 |
| check_interval | float | 0.2 | 检查间隔时间(秒) |
| enable_print | bool | False | 是否打印设备信息到日志 |
| enable_real_id | bool | True | 是否获取实际设备ID |
| enable_location | bool | True | 是否获取设备位置信息 |
| exclude_services | List[str] | ['disk', 'USBSTOR'] | 要排除的服务列表 |

## 回调函数

回调函数接收一个包含设备信息的字典参数：

```python
def on_connect(info: Dict[str, Any]) -> None:
    """
    当USB设备连接时调用
    
    参数:
        info: 包含设备信息的字典，至少包含'设备ID'键
    """
    device_id = info.get('设备ID')
    # 处理设备连接事件
```

设备信息字典包含以下常见字段：

- `设备ID`: 原始设备ID
- `实际设备ID`: 从注册表获取的实际设备ID（如果enable_real_id=True）
- `设备位置`: 设备的物理位置信息（如果enable_location=True）
- `状态`: 设备当前状态，"已连接"或"已断开"
- `添加时间`/`断开时间`: 事件发生的时间
- `Service`: 设备服务名称，可用于识别设备类型
- 其他设备属性: 如制造商、设备名称等（当可用时）

## 高级用法

### 以不同配置运行

**最高性能模式**（不获取额外信息）:
```python
monitor = USBEventMonitor(
    on_connect=on_connect,
    on_disconnect=on_disconnect,
    enable_real_id=False,
    enable_location=False
)
```

**获取完整信息模式**:
```python
monitor = USBEventMonitor(
    on_connect=on_connect,
    on_disconnect=on_disconnect,
    enable_print=True,
    enable_real_id=True,
    enable_location=True
)
```

**自定义排除服务**:
```python
# 排除磁盘、存储设备和打印机
monitor = USBEventMonitor(
    on_connect=on_connect,
    on_disconnect=on_disconnect,
    exclude_services=['disk', 'USBSTOR', 'usbprint']
)

# 排除特定MTP设备
monitor = USBEventMonitor(
    on_connect=on_connect,
    on_disconnect=on_disconnect,
    exclude_services=['disk', 'USBSTOR', 'WUDFWpdMtp']
)

# 不排除任何服务
monitor = USBEventMonitor(
    on_connect=on_connect,
    on_disconnect=on_disconnect,
    exclude_services=[]
)
```

### 在线程中运行

```python
import threading

def monitor_thread():
    monitor = USBEventMonitor(
        on_connect=on_connect,
        on_disconnect=on_disconnect
    )
    monitor.start()  # 阻塞调用

# 创建并启动线程
thread = threading.Thread(target=monitor_thread)
thread.daemon = True  # 设置为守护线程
thread.start()

# 主程序继续执行其他任务
# ...
```

## API文档

### USBEventMonitor类

```python
class USBEventMonitor:
    def __init__(self,
                 on_connect=None,
                 on_disconnect=None,
                 check_interval=0.2,
                 enable_print=False,
                 enable_real_id=True,
                 enable_location=True,
                 exclude_services=None):
        """初始化USB监控器"""
        # ...
        
    def start(self):
        """启动监控（阻塞方法）"""
        # ...
        
    def stop(self):
        """停止监控"""
        # ...
```

## 版本历史

### v1.07
- 使用Python标准库logging模块替代自定义logger
- 正则表达式模式预编译优化
- 改进异常处理，支持优雅退出
- 默认启用设备位置信息获取
- 添加exclude_services参数，支持排除特定服务类型的设备
- 将WUDFWpdMtp从默认排除服务列表中移除
- 其他性能和稳定性改进

### v1.06
- 添加设备位置信息获取功能
- 性能优化

### v1.05
- 支持获取实际设备ID
- 增强错误处理

### v1.04
- 支持Windows注册表查询
- 添加事件回调机制

### v1.03
- 初始功能实现

## 系统要求

- Windows 7/8/10/11
- Python 3.8+
- 依赖库: wmi, pythoncom

## 许可证

MIT许可证

## 贡献

欢迎提交问题报告和功能请求。如果您想贡献代码，请先开issue讨论您想要改变的内容。 