# ZhipuAI 网页搜索 Dify 插件

[English Documentation](./README.md)

一个由智谱AI高级搜索API驱动的Dify插件，支持过滤和内容控制的强大网页搜索功能。

## 关于智谱AI网页搜索

本插件基于[智谱AI网页搜索API](https://open.bigmodel.cn)，这是一个全面的网页搜索解决方案，提供智能搜索结果以及丰富的元数据和内容摘要。

系统使用：
- **智谱AI Search Pro**：针对准确性和相关性优化的高级搜索引擎
- **智能内容提取**：自动从网页中进行摘要和内容提取
- **域名与时间过滤**：通过域名和日期范围过滤器精确控制搜索范围
- **可配置内容大小**：针对不同使用场景的可调整摘要长度
- **高性能**：快速搜索结果，每次查询最多支持50个结果

插件使用您的API密钥直接连接到智谱AI的API，实现对搜索服务的身份验证访问。

## 使用方法

### 安装

您可以下载[最新版本](https://github.com/bdim404/zhipuai-web-search-dify-plugin/releases/latest)并上传到Dify平台。详细说明请参考[安装和使用插件：本地文件上传](https://docs.dify.ai/zh-hans/plugins/quick-start/install-plugins#ben-di-wen-jian-shang-chuan)。

### 打包（可选）

如果您想自己打包此插件，请确保已安装[dify-plugin-daemon](https://github.com/langgenius/dify-plugin-daemon/releases)，然后下载或`git clone`此仓库。之后，您可以使用以下命令进行打包：

```
dify-plugin-daemon plugin package ./zhipuai-web-search-dify-plugin
```

更多信息请参考[工具插件：打包插件](https://docs.dify.ai/zh-hans/plugins/quick-start/develop-plugins/tool-plugin#da-bao-cha-jian)。

### 配置设置

此插件需要智谱AI API密钥才能访问网页搜索服务。

您需要提供以下配置：

- **智谱AI API密钥**：来自智谱AI平台的身份验证密钥

**获取您的API密钥：**

1. 访问[智谱AI开放平台](https://open.bigmodel.cn)
2. 注册或登录您的账户
3. 导航至API密钥部分
4. 创建或复制您的API密钥
5. 将其粘贴到Dify中的插件配置中

在设置期间，插件将验证您的API密钥，以确保与智谱AI服务成功进行身份验证。

### 功能特性

此插件支持以下功能：

1. **智能网页搜索**：访问由智谱AI搜索引擎提供的全面网页搜索

2. **高级过滤选项**：
   - 域名过滤，将搜索限制在特定网站
   - 基于时间的过滤（过去一天、一周、一个月、一年）
   - 可配置的结果数量（1-50个结果）

3. **内容大小控制**：可调整的摘要长度（简短、中等、详细），适用于不同使用场景

4. **丰富的元数据**：为每个结果返回标题、URL、内容摘要、图标和媒体信息

5. **双格式输出**：以结构化JSON和格式化文本提供结果，实现最大兼容性

6. **多种搜索引擎**：支持不同的智谱AI搜索引擎（默认：search_pro）

您可以在Dify工作流或其他地方调用此插件。只需提供您的搜索查询和可选过滤器，插件将返回相关的网页搜索结果，包含JSON和文本格式的摘要和元数据。

### 参数

- **search_query**（必需）：要处理的搜索查询或问题
- **search_engine**（可选）：要使用的搜索引擎（默认：search_pro）
- **count**（可选）：要返回的搜索结果数量（1-50，默认：10）
- **search_domain_filter**（可选）：仅访问指定域名的内容（例如：www.example.com）
- **search_recency_filter**（可选）：按日期范围过滤结果（无限制、过去一天、一周、一个月、一年）
- **content_size**（可选）：控制返回摘要的长度（简短、中等、详细）

## 作者

**作者：** bdim 
**版本：** 0.1.0 
**类型：** 工具 
