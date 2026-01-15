from typing import Any
from dify_plugin.errors.tool import ToolProviderCredentialValidationError
from dify_plugin import ToolProvider
import requests


class ZhipuAIProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        api_key = credentials.get("zhipuai_api_key")
        if not api_key:
            raise ToolProviderCredentialValidationError("ZhipuAI API key is missing")

        url = "https://open.bigmodel.cn/api/paas/v4/tools"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "tool": "web-search-pro",
            "messages": [{"role": "user", "content": "test"}],
            "stream": False,
            "search_query": "test",
            "count": 1
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)

            if response.status_code == 401:
                raise ToolProviderCredentialValidationError("Invalid ZhipuAI API key")
            elif response.status_code == 403:
                raise ToolProviderCredentialValidationError("ZhipuAI API key does not have access")
            elif response.status_code >= 400:
                try:
                    error_data = response.json()
                    if "error" in error_data:
                        error_msg = error_data["error"].get("message", "")
                        error_code = error_data["error"].get("code", "")
                        if error_code == "1113" or "余额不足" in error_msg:
                            raise ToolProviderCredentialValidationError("账户余额不足，请充值")
                        raise ToolProviderCredentialValidationError(f"API error: {error_msg}")
                except (ValueError, KeyError):
                    pass
                if response.status_code == 429:
                    raise ToolProviderCredentialValidationError("Rate limit exceeded - Too many requests, please try again later")
                raise ToolProviderCredentialValidationError(f"API validation failed: {response.status_code}")

        except requests.exceptions.Timeout:
            raise ToolProviderCredentialValidationError("Request timeout during validation")
        except requests.exceptions.RequestException as e:
            raise ToolProviderCredentialValidationError(f"Network error during validation: {str(e)}")
