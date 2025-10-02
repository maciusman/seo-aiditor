# ai_engine.py - Centralny moduł AI (Gemini 2.5 Flash)
import json
from typing import Dict, Any, Optional

class AIAnalyzer:
    """Centralna klasa do analizy AI używając Gemini 2.5 Flash"""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        """
        Initialize AI Analyzer

        Args:
            api_key: Google Gemini API key
            model: Model name (default: gemini-2.5-flash)
        """
        self.api_key = api_key
        self.model = model
        self.client = None
        self.tools = [{"url_context": {}}]  # URL Context enabled!

        # Initialize client
        self._initialize_client()

    def _initialize_client(self):
        """Initialize Gemini client"""
        try:
            from google import genai
            from google.genai.types import GenerateContentConfig

            self.client = genai.Client(api_key=self.api_key)
            self.GenerateContentConfig = GenerateContentConfig
            print("[OK] Gemini AI Engine initialized successfully")
        except ImportError:
            print("[ERROR] google-genai library not installed")
            print("Run: pip install google-genai")
            self.client = None
        except Exception as e:
            print(f"[ERROR] Initializing Gemini: {e}")
            self.client = None

    def is_available(self) -> bool:
        """Check if AI is available"""
        return self.client is not None and self.api_key != "YOUR_GEMINI_API_KEY_HERE"

    def analyze_url(self, url: str, prompt: str, use_url_context: bool = True) -> str:
        """
        Analyze URL with full page context using Gemini URL Context

        Args:
            url: URL to analyze (can be single URL or multiple URLs separated by commas)
            prompt: Analysis prompt
            use_url_context: Enable URL context tool (default: True)

        Returns:
            AI response text
        """
        if not self.is_available():
            return json.dumps({"error": "AI not available - check API key"})

        try:
            config_tools = self.tools if use_url_context else []

            # NOTE: response_mime_type cannot be used with tools (URL Context)
            # So we rely on prompt instructions for JSON formatting
            config_params = {
                'temperature': 0.7,
            }

            if config_tools:
                config_params['tools'] = config_tools
            else:
                # Only use response_mime_type if NOT using tools
                config_params['response_mime_type'] = "application/json"

            response = self.client.models.generate_content(
                model=self.model,
                contents=f"{prompt}\n\nURL to analyze: {url}",
                config=self.GenerateContentConfig(**config_params)
            )

            return response.text
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] AI Error: {error_msg}")
            return json.dumps({"error": error_msg})

    def analyze_multiple_urls(self, urls: list, prompt: str) -> str:
        """
        Analyze multiple URLs together using URL Context (for holistic analysis)

        Args:
            urls: List of URLs to analyze together
            prompt: Analysis prompt

        Returns:
            AI response text
        """
        if not self.is_available():
            return json.dumps({"error": "AI not available - check API key"})

        try:
            # Format URLs for the prompt
            urls_formatted = '\n'.join([f"- {url}" for url in urls])

            # Use URL Context tool
            config_params = {
                'temperature': 0.7,
                'tools': self.tools
            }

            # Include all URLs in the request
            full_prompt = f"""{prompt}

**URLS TO ANALYZE HOLISTICALLY:**
{urls_formatted}

Fetch and analyze ALL these URLs together. Look for patterns across pages.
"""

            response = self.client.models.generate_content(
                model=self.model,
                contents=full_prompt,
                config=self.GenerateContentConfig(**config_params)
            )

            return response.text
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] AI Error analyzing multiple URLs: {error_msg}")
            return json.dumps({"error": error_msg})

    def analyze_text(self, text: str, prompt: str, json_output: bool = True) -> str:
        """
        Analyze text without URL context

        Args:
            text: Text to analyze
            prompt: Analysis prompt
            json_output: Request JSON formatted response

        Returns:
            AI response text
        """
        if not self.is_available():
            return json.dumps({"error": "AI not available - check API key"})

        try:
            mime_type = "application/json" if json_output else "text/plain"

            response = self.client.models.generate_content(
                model=self.model,
                contents=f"{prompt}\n\nText to analyze:\n{text[:10000]}",  # Limit text to 10k chars
                config=self.GenerateContentConfig(
                    temperature=0.7,
                    response_mime_type=mime_type
                )
            )

            return response.text
        except Exception as e:
            error_msg = str(e)
            print(f"[ERROR] AI Error: {error_msg}")
            return json.dumps({"error": error_msg})

    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Parse JSON response from AI

        Args:
            response: AI response text

        Returns:
            Parsed JSON dict or error dict
        """
        try:
            # Remove markdown code blocks if present
            if response.startswith("```json"):
                response = response.replace("```json", "").replace("```", "").strip()
            elif response.startswith("```"):
                response = response.replace("```", "").strip()

            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON Parse Error: {e}")
            print(f"Response: {response[:200]}...")
            return {"error": "Invalid JSON response", "raw": response}

    def analyze_with_retry(self, url: str, prompt: str, max_retries: int = 2) -> Dict[str, Any]:
        """
        Analyze with retry logic for better reliability

        Args:
            url: URL to analyze
            prompt: Analysis prompt
            max_retries: Maximum retry attempts

        Returns:
            Parsed JSON response
        """
        for attempt in range(max_retries + 1):
            try:
                response = self.analyze_url(url, prompt)
                parsed = self.parse_json_response(response)

                if "error" not in parsed:
                    return parsed

                if attempt < max_retries:
                    print(f"[WARN] Retry {attempt + 1}/{max_retries}...")
                    continue

                return parsed
            except Exception as e:
                if attempt < max_retries:
                    print(f"⚠️ Retry {attempt + 1}/{max_retries} after error: {e}")
                    continue
                return {"error": str(e)}

        return {"error": "Max retries exceeded"}


# Factory function for easy initialization
def create_ai_analyzer(api_key: str, model: str = "gemini-2.5-flash") -> Optional[AIAnalyzer]:
    """
    Create AI Analyzer instance

    Args:
        api_key: Gemini API key
        model: Model name

    Returns:
        AIAnalyzer instance or None if initialization fails
    """
    try:
        analyzer = AIAnalyzer(api_key, model)
        if analyzer.is_available():
            return analyzer
        return None
    except Exception as e:
        print(f"[ERROR] Failed to create AI Analyzer: {e}")
        return None


# Convenience class for backward compatibility
class AIEngine:
    """Backward compatibility wrapper for AIAnalyzer"""

    def __init__(self):
        from config import GEMINI_API_KEY, GEMINI_MODEL
        self.analyzer = create_ai_analyzer(GEMINI_API_KEY, GEMINI_MODEL)

    def is_available(self):
        return self.analyzer is not None and self.analyzer.is_available()

    def analyze_url(self, url: str, prompt: str, use_url_context: bool = True):
        if not self.analyzer:
            return json.dumps({"error": "AI not available"})
        return self.analyzer.analyze_url(url, prompt, use_url_context)

    def analyze_multiple_urls(self, urls: list, prompt: str):
        if not self.analyzer:
            return json.dumps({"error": "AI not available"})
        return self.analyzer.analyze_multiple_urls(urls, prompt)

    def analyze_text(self, text: str, prompt: str, json_output: bool = True):
        if not self.analyzer:
            return json.dumps({"error": "AI not available"})
        return self.analyzer.analyze_text(text, prompt, json_output)

    def parse_json_response(self, response: str):
        if not self.analyzer:
            return {"error": "AI not available"}
        return self.analyzer.parse_json_response(response)


# Test function
if __name__ == "__main__":
    import os
    from config import GEMINI_API_KEY

    print("Testing AI Engine...")

    ai = create_ai_analyzer(GEMINI_API_KEY)

    if ai and ai.is_available():
        print("[OK] AI Engine is ready!")

        # Test simple text analysis
        test_prompt = "Analyze this text and return JSON with: {sentiment: 'positive'|'negative', summary: 'brief summary'}"
        test_text = "This is an amazing SEO tool that helps users optimize their websites!"

        result = ai.analyze_text(test_text, test_prompt)
        print(f"\nTest Result: {result}")
    else:
        print("[ERROR] AI Engine not available - check API key in config_local.py")
