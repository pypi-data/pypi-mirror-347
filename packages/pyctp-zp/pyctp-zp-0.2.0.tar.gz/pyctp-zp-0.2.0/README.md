# pyctp-zp

## 项目简介

`pyctp-zp` 是一个基于 CTP 官方 API 和 SWIG 封装的 Python 接口，支持 Windows 平台，兼容 Python 3.12 及以上版本。该项目包含两个主要包：

- `PyCTP`：CTP Python 接口实现
- `CPPyCTP`：测评版 CTP Python 接口

本项目适用于需要在 Python 中调用 CTP（中国金融期货交易所交易接口）相关功能的开发者。

---

## 安装方法

1. **通过 PyPI 安装（推荐）**

   ```bash
   pip install pyctp-zp
   ```
2. **本地源码安装**

   在项目根目录下执行：

   ```bash
   python setup.py install
   ```

---

## 使用方法

安装完成后，可以直接在 Python 中导入并使用：

```python
import PyCTP
import CPPyCTP
```

### 示例

```python
from PyCTP import *
# 或
from CPPyCTP import *
```

具体接口和用法请参考各包下的源码和注释。

---

## 包结构说明

```
Pypiupload/
  CPPyCTP/         # C++ 封装的 CTP Python 接口
    __init__.py
    ...其它文件...
  PyCTP/           # CTP Python 接口实现
    __init__.py
    ...其它文件...
  setup.py         # 安装脚本
  README.md        # 项目说明
```

- 每个包下都应有 `__init__.py` 文件，确保可以被 Python 识别为包。
- 包含的二进制文件（如 `.pyd`, `.dll`）和 `.py` 文件会自动被打包。

---

## 常见问题

1. **安装失败或找不到模块？**

   - 请确保你的 Python 版本为 3.12 及以上。
   - 检查是否有 `__init__.py` 文件。
   - Windows 平台下请使用 64 位 Python。
2. **如何查看包内文件？**

   - 安装后可在 `site-packages` 目录下找到 `PyCTP` 和 `CPPyCTP` 文件夹。
3. **依赖问题？**

   - 本项目主要依赖官方 CTP API 和 SWIG 生成的接口文件。

---

## 联系方式

- 作者：luochenyeling
- 邮箱：zhaokehan86@163.com

如有问题或建议，欢迎通过邮箱联系。

---

## 版本历史

- v0.1.0 首次发布，支持 PyCTP 和 CPPyCTP 两个包的安装与使用。

---

## 接口文档与示例

### 主要接口说明

#### 1. 交易接口（CThostFtdcTraderApi）

- **创建交易API对象**
  ```python
  from PyCTP.thosttraderapi import CThostFtdcTraderApi
  api = CThostFtdcTraderApi.CreateFtdcTraderApi()
  ```
- **注册前置机地址**
  ```python
  api.RegisterFront("tcp://180.168.146.187:10000")
  ```
- **注册回调（SPI）对象**
  ```python
  api.RegisterSpi(my_spi_instance)
  ```
- **初始化连接**
  ```python
  api.Init()
  ```
- **用户登录**
  ```python
  api.ReqUserLogin(login_field, request_id)
  ```
- **下单**
  ```python
  api.ReqOrderInsert(order_field, request_id)
  ```
- **查询资金、持仓等**
  ```python
  api.ReqQryTradingAccount(query_field, request_id)
  api.ReqQryInvestorPosition(query_field, request_id)
  ```

#### 2. 行情接口（CThostFtdcMdApi）

- **创建行情API对象**
  ```python
  from PyCTP.thostmduserapi import CThostFtdcMdApi
  mdapi = CThostFtdcMdApi.CreateFtdcMdApi()
  ```
- **注册前置机地址**
  ```python
  mdapi.RegisterFront("tcp://180.168.146.187:10010")
  ```
- **注册回调（SPI）对象**
  ```python
  mdapi.RegisterSpi(my_mdspi_instance)
  ```
- **初始化连接**
  ```python
  mdapi.Init()
  ```
- **用户登录**
  ```python
  mdapi.ReqUserLogin(login_field, request_id)
  ```
- **订阅行情**
  ```python
  mdapi.SubscribeMarketData(["IF2406"], 1)
  ```

---

### 示例代码

#### 交易API快速入门

```python
from PyCTP.thosttraderapi import CThostFtdcTraderApi, CThostFtdcTraderSpi, CThostFtdcReqUserLoginField

class MyTraderSpi(CThostFtdcTraderSpi):
    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        print("登录回报", pRspUserLogin, pRspInfo)

api = CThostFtdcTraderApi.CreateFtdcTraderApi()
spi = MyTraderSpi()
api.RegisterSpi(spi)
api.RegisterFront("tcp://180.168.146.187:10000")
api.Init()

login_field = CThostFtdcReqUserLoginField()
login_field.BrokerID = "9999"
login_field.UserID = "你的账号"
login_field.Password = "你的密码"
api.ReqUserLogin(login_field, 1)
```

#### 行情API快速入门

```python
from PyCTP.thostmduserapi import CThostFtdcMdApi, CThostFtdcMdSpi, CThostFtdcReqUserLoginField

class MyMdSpi(CThostFtdcMdSpi):
    def OnRtnDepthMarketData(self, pDepthMarketData):
        print("行情数据", pDepthMarketData)

mdapi = CThostFtdcMdApi.CreateFtdcMdApi()
mdspi = MyMdSpi()
mdapi.RegisterSpi(mdspi)
mdapi.RegisterFront("tcp://180.168.146.187:10010")
mdapi.Init()

login_field = CThostFtdcReqUserLoginField()
login_field.BrokerID = "9999"
login_field.UserID = "你的账号"
login_field.Password = "你的密码"
mdapi.ReqUserLogin(login_field, 1)
mdapi.SubscribeMarketData(["IF2406"], 1)
```

---

### 适用范围

- PyCTP 和 CPPyCTP 的接口和用法基本一致，均支持交易和行情功能。
- 你可以根据需要选择 import PyCTP 或 import CPPyCTP，示例代码同样适用。

---

## 进阶接口说明与实战案例

### 1. 常用参数详细说明

#### 1.1 登录参数（CThostFtdcReqUserLoginField）

| 字段名      | 说明         | 示例值      |
| ----------- | ------------ | ---------- |
| BrokerID    | 经纪公司代码 | "9999"     |
| UserID      | 用户名       | "123456"   |
| Password    | 密码         | "abcdef"   |
| UserProductInfo | 用户端产品信息 | 可选 |

#### 1.2 下单参数（CThostFtdcInputOrderField）

| 字段名         | 说明           | 示例值         |
| -------------- | -------------- | -------------- |
| BrokerID       | 经纪公司代码   | "9999"         |
| InvestorID     | 投资者账号     | "123456"       |
| InstrumentID   | 合约代码       | "IF2406"       |
| OrderRef       | 报单引用       | "1"            |
| UserID         | 用户代码       | "123456"       |
| Direction      | 买卖方向       | "0"=买 "1"=卖  |
| CombOffsetFlag | 开平标志       | "0"=开 "1"=平  |
| CombHedgeFlag  | 投机套保标志   | "1"=投机       |
| LimitPrice     | 价格           | 3500           |
| VolumeTotalOriginal | 数量       | 1              |
| OrderPriceType | 价格类型       | "2"=限价单      |
| TimeCondition  | 有效期类型     | "3"=当日有效    |
| VolumeCondition| 成交量类型     | "1"=任何数量    |
| MinVolume      | 最小成交量     | 1              |
| ContingentCondition | 触发条件   | "1"=立即       |
| ForceCloseReason   | 强平原因   | "0"=非强平     |

#### 1.3 行情订阅参数

- 合约代码列表（如 `["IF2406", "rb2406"]`）
- 数量（如 `2`）

---

### 2. 主要回调事件说明

#### 2.1 交易SPI常用回调（CThostFtdcTraderSpi）

| 回调函数名                | 触发时机/说明                         |
|--------------------------|----------------------------------------|
| OnFrontConnected         | 与前置机建立连接时                     |
| OnFrontDisconnected      | 与前置机断开连接时                     |
| OnRspUserLogin           | 登录请求响应                           |
| OnRspUserLogout          | 登出请求响应                           |
| OnRspOrderInsert         | 报单录入请求响应（下单回报）           |
| OnRtnOrder               | 有报单状态变化时（如已报、已成交等）   |
| OnRtnTrade               | 成交回报                               |
| OnRspQryTradingAccount   | 查询资金账户响应                       |
| OnRspQryInvestorPosition | 查询持仓响应                           |
| OnRspError               | 请求错误时                             |

#### 2.2 行情SPI常用回调（CThostFtdcMdSpi）

| 回调函数名                | 触发时机/说明                         |
|--------------------------|----------------------------------------|
| OnFrontConnected         | 与行情前置建立连接时                   |
| OnFrontDisconnected      | 与行情前置断开连接时                   |
| OnRspUserLogin           | 登录请求响应                           |
| OnRspUserLogout          | 登出请求响应                           |
| OnRspSubMarketData       | 订阅行情响应                           |
| OnRtnDepthMarketData     | 行情推送（每次有新行情都会触发）       |
| OnRspError               | 请求错误时                             |

---

### 3. 更复杂的实战案例

#### 3.1 自动登录+自动下单+自动查询资金

```python
from PyCTP.thosttraderapi import CThostFtdcTraderApi, CThostFtdcTraderSpi, CThostFtdcReqUserLoginField, CThostFtdcInputOrderField

class MyTraderSpi(CThostFtdcTraderSpi):
    def __init__(self, api):
        super().__init__()
        self.api = api

    def OnFrontConnected(self):
        print("已连接交易前置，开始登录")
        login = CThostFtdcReqUserLoginField()
        login.BrokerID = "9999"
        login.UserID = "123456"
        login.Password = "abcdef"
        self.api.ReqUserLogin(login, 1)

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        print("登录回报", pRspUserLogin, pRspInfo)
        # 登录成功后自动下单
        order = CThostFtdcInputOrderField()
        order.BrokerID = "9999"
        order.InvestorID = "123456"
        order.InstrumentID = "IF2406"
        order.OrderRef = "1"
        order.UserID = "123456"
        order.Direction = "0"  # 买
        order.CombOffsetFlag = "0"  # 开仓
        order.CombHedgeFlag = "1"  # 投机
        order.LimitPrice = 3500
        order.VolumeTotalOriginal = 1
        order.OrderPriceType = "2"  # 限价
        order.TimeCondition = "3"  # 当日有效
        order.VolumeCondition = "1"
        order.MinVolume = 1
        order.ContingentCondition = "1"
        order.ForceCloseReason = "0"
        self.api.ReqOrderInsert(order, 2)
        # 查询资金
        self.api.ReqQryTradingAccount({}, 3)

    def OnRspOrderInsert(self, pInputOrder, pRspInfo, nRequestID, bIsLast):
        print("下单回报", pInputOrder, pRspInfo)

    def OnRspQryTradingAccount(self, pTradingAccount, pRspInfo, nRequestID, bIsLast):
        print("资金查询回报", pTradingAccount)

api = CThostFtdcTraderApi.CreateFtdcTraderApi()
spi = MyTraderSpi(api)
api.RegisterSpi(spi)
api.RegisterFront("tcp://180.168.146.187:10000")
api.Init()
```

#### 3.2 自动登录+自动订阅行情+自动打印行情

```python
from PyCTP.thostmduserapi import CThostFtdcMdApi, CThostFtdcMdSpi, CThostFtdcReqUserLoginField

class MyMdSpi(CThostFtdcMdSpi):
    def __init__(self, api):
        super().__init__()
        self.api = api

    def OnFrontConnected(self):
        print("已连接行情前置，开始登录")
        login = CThostFtdcReqUserLoginField()
        login.BrokerID = "9999"
        login.UserID = "123456"
        login.Password = "abcdef"
        self.api.ReqUserLogin(login, 1)

    def OnRspUserLogin(self, pRspUserLogin, pRspInfo, nRequestID, bIsLast):
        print("行情登录回报", pRspUserLogin, pRspInfo)
        # 登录成功后自动订阅行情
        self.api.SubscribeMarketData(["IF2406", "rb2406"], 2)

    def OnRtnDepthMarketData(self, pDepthMarketData):
        print("实时行情：", pDepthMarketData.InstrumentID, pDepthMarketData.LastPrice)

mdapi = CThostFtdcMdApi.CreateFtdcMdApi()
mdspi = MyMdSpi(mdapi)
mdapi.RegisterSpi(mdspi)
mdapi.RegisterFront("tcp://180.168.146.187:10010")
mdapi.Init()
```

---

### 4. 进阶建议

- 所有结构体字段和回调函数都可以通过`dir(对象)`查看，或查阅官方CTP开发文档。
- 建议先用模拟账号和测试环境练习，避免资金风险。
- 如需更详细的字段说明或特殊用法，可以随时告诉我你关心的接口或场景！
