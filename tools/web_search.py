from collections.abc import Generator
from typing import Any
import requests
import sys

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


def log_info(msg):
    print(f"[INFO] {msg}", file=sys.stderr, flush=True)


def log_error(msg):
    print(f"[ERROR] {msg}", file=sys.stderr, flush=True)


def validate_parameters(parameters: dict) -> dict:
    validated = {}

    search_query = parameters.get("search_query", "").strip()
    if not search_query:
        raise ValueError("search_query is required and cannot be empty")
    validated["search_query"] = search_query

    search_engine = parameters.get("search_engine", "search_pro")
    validated["search_engine"] = search_engine

    count = parameters.get("count", 10)
    try:
        count = int(count)
        if count < 1:
            count = 1
        elif count > 50:
            count = 50
        validated["count"] = count
    except (ValueError, TypeError):
        validated["count"] = 10

    if parameters.get("search_domain_filter"):
        domain = parameters["search_domain_filter"].strip()
        if domain:
            validated["search_domain_filter"] = domain

    recency = parameters.get("search_recency_filter", "noLimit")
    valid_recency = ["noLimit", "day", "week", "month", "year"]
    if recency in valid_recency:
        validated["search_recency_filter"] = recency
    else:
        validated["search_recency_filter"] = "noLimit"

    content_size = parameters.get("content_size", "medium")
    valid_sizes = ["low", "medium", "high"]
    if content_size in valid_sizes:
        validated["content_size"] = content_size
    else:
        validated["content_size"] = "medium"

    return validated


def build_request(api_key: str, parameters: dict) -> tuple[str, dict, dict]:
    url = "https://open.bigmodel.cn/api/paas/v4/tools"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "Dify-Plugin-ZhipuAI-WebSearch/0.1.0"
    }

    payload = {
        "tool": "web-search-pro",
        "messages": [{"role": "user", "content": parameters.get("search_query")}],
        "stream": False
    }

    if parameters.get("search_engine"):
        payload["search_engine"] = parameters["search_engine"]

    if "count" in parameters:
        payload["count"] = int(parameters["count"])

    if parameters.get("search_domain_filter"):
        payload["search_domain_filter"] = parameters["search_domain_filter"]

    if parameters.get("search_recency_filter") and parameters["search_recency_filter"] != "noLimit":
        payload["search_recency_filter"] = parameters["search_recency_filter"]

    if parameters.get("content_size"):
        payload["content_size"] = parameters["content_size"]

    return url, headers, payload


def handle_api_errors(response: requests.Response) -> None:
    if response.status_code == 200:
        return

    error_messages = {
        400: "Bad request - Invalid parameters",
        401: "Authentication failed - Invalid API key",
        403: "Access denied - API key does not have permission",
        404: "Endpoint not found",
        429: "Rate limit exceeded - Too many requests",
        500: "Internal server error",
        503: "Service unavailable"
    }

    status_code = response.status_code
    error_message = error_messages.get(status_code, f"API error {status_code}")

    try:
        error_data = response.json()
        if "error" in error_data:
            error_message = f"{error_message}: {error_data['error']}"
        elif "message" in error_data:
            error_message = f"{error_message}: {error_data['message']}"
    except Exception:
        pass

    raise Exception(error_message)


def safe_api_call(url: str, headers: dict, payload: dict, timeout: int = 30) -> dict:
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout)
        handle_api_errors(response)
        return response.json()
    except requests.exceptions.Timeout:
        raise Exception("Request timeout - API took too long to respond")
    except requests.exceptions.ConnectionError:
        raise Exception("Connection error - Unable to reach ZhipuAI API")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Invalid JSON response: {str(e)}")


def format_search_results(response_data: dict) -> dict:
    formatted = {
        "success": True,
        "results": []
    }

    if "choices" in response_data and len(response_data["choices"]) > 0:
        choice = response_data["choices"][0]

        if "message" in choice and "tool_calls" in choice["message"]:
            tool_calls = choice["message"]["tool_calls"]

            for tool_call in tool_calls:
                if "search_result" in tool_call:
                    search_results = tool_call["search_result"]

                    for result in search_results:
                        formatted_result = {
                            "title": result.get("title", ""),
                            "link": result.get("link", ""),
                            "content": result.get("content", ""),
                            "icon": result.get("icon", ""),
                            "media": result.get("media", "")
                        }
                        formatted["results"].append(formatted_result)

    formatted["total_results"] = len(formatted["results"])
    return formatted


def format_text_output(results: dict) -> str:
    output_lines = []
    output_lines.append(f"Found {results['total_results']} results:\n")

    for idx, result in enumerate(results["results"], 1):
        title = result.get("title", "No Title")
        link = result.get("link", "")
        content = result.get("content", "")

        output_lines.append(f"## Result {idx}: {title}")
        output_lines.append(f"**URL:** {link}")
        if content:
            output_lines.append(f"\n{content}\n")
        output_lines.append("---\n")

    return "\n".join(output_lines)


class ZhipuAIWebSearchTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.runtime.credentials.get("zhipuai_api_key")
        if not api_key:
            yield self.create_text_message("ZhipuAI API key is missing")
            return

        try:
            validated_params = validate_parameters(tool_parameters)
            log_info(f"Search query: {validated_params['search_query']}")

            url, headers, payload = build_request(api_key, validated_params)
            response_data = safe_api_call(url, headers, payload)

            formatted_results = format_search_results(response_data)

            if formatted_results["total_results"] == 0:
                yield self.create_text_message("No results found for the search query")
                return

            yield self.create_json_message(formatted_results)

            text_output = format_text_output(formatted_results)
            yield self.create_text_message(text_output)

            log_info(f"Successfully returned {formatted_results['total_results']} results")

        except ValueError as e:
            log_error(f"Validation error: {str(e)}")
            yield self.create_text_message(f"Parameter error: {str(e)}")
        except Exception as e:
            log_error(f"Error during search: {str(e)}")
            yield self.create_text_message(f"Search failed: {str(e)}")
