# ZhipuAI Web Search Dify Plugin

[中文文档](./README.zh.md)

A Dify plugin for powerful web search powered by ZhipuAI's advanced search API with filtering and content control.

## About ZhipuAI Web Search

This plugin is based on [ZhipuAI's Web Search API](https://open.bigmodel.cn), a comprehensive web search solution that provides intelligent search results with rich metadata and content summaries.

The system uses:
- **ZhipuAI Search Pro**: Advanced search engine optimized for accuracy and relevance
- **Smart Content Extraction**: Automatic summarization and content extraction from web pages
- **Domain & Time Filtering**: Precise control over search scope with domain and date range filters
- **Configurable Content Size**: Adjustable summary length for different use cases
- **High Performance**: Fast search results with up to 50 results per query

The plugin connects directly to ZhipuAI's API using your API key for authenticated access to the search service.

## Usage

### Install

You can download [the latest release](https://github.com/bdim404/zhipuai-web-search-dify-plugin/releases/latest) and upload it to the Dify platform. For detailed instructions, please refer to [Install and Use Plugins: Local File Upload](https://docs.dify.ai/plugins/quick-start/install-plugins#local-file-upload).

### Packing (Optional)

If you want to pack this plugin yourself, make sure you have [dify-plugin-daemon](https://github.com/langgenius/dify-plugin-daemon/releases) installed, and then download or `git clone` this repository. After that, you can pack it using the following command:

```
dify-plugin-daemon plugin package ./zhipuai-web-search-dify-plugin
```

For more information, please refer to [Tool Plugin: Packing Plugin](https://docs.dify.ai/plugins/quick-start/develop-plugins/tool-plugin#packing-plugin).

### Set Up Configuration

This plugin requires a ZhipuAI API key to access the web search service.

You need to provide the following configuration:

- **ZhipuAI API Key**: Your authentication key from ZhipuAI platform

**Getting Your API Key:**

1. Visit [ZhipuAI Open Platform](https://open.bigmodel.cn)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create or copy your API key
5. Paste it into the plugin configuration in Dify

During setup, the plugin will validate your API key to ensure successful authentication with ZhipuAI's services.

### Features

This plugin supports the following features:

1. **Intelligent Web Search**: Access to comprehensive web search powered by ZhipuAI's search engine

2. **Advanced Filtering Options**:
   - Domain filtering to restrict searches to specific websites
   - Time-based filtering (past day, week, month, year)
   - Configurable result count (1-50 results)

3. **Content Size Control**: Adjustable summary length (low, medium, high) for different use cases

4. **Rich Metadata**: Returns title, URL, content summary, icon, and media information for each result

5. **Dual Format Output**: Results provided in both structured JSON and formatted text for maximum compatibility

6. **Multiple Search Engines**: Support for different ZhipuAI search engines (default: search_pro)

You can call this plugin in Dify workflows or elsewhere. Simply provide your search query and optional filters, and the plugin will return relevant web search results with summaries and metadata in both JSON and text format.

### Parameters

- **search_query** (required): The search query or question to be processed
- **search_engine** (optional): Search engine to use (default: search_pro)
- **count** (optional): Number of search results to return (1-50, default: 10)
- **search_domain_filter** (optional): Only access content from specified domain (e.g., www.example.com)
- **search_recency_filter** (optional): Filter results by date range (noLimit, day, week, month, year)
- **content_size** (optional): Control the length of returned summaries (low, medium, high)

## Author

**Author:** bdim 
**Version:** 0.1.0 
**Type:** tool
