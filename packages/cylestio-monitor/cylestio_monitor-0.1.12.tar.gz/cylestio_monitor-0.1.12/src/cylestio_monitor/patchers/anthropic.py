"""Anthropic patcher for monitoring Anthropic API calls."""

import functools
import inspect
import json
import logging
import time
import traceback
from datetime import datetime
from typing import Any, Dict, List, Optional

# Try to import Anthropic but don't fail if not available
try:
    from anthropic import Anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from ..utils.event_logging import log_event
from ..utils.event_utils import format_timestamp
from ..utils.trace_context import TraceContext
from .base import BasePatcher

# Track patched clients to prevent duplicate patching
_patched_clients = set()
_is_module_patched = False

# Store original methods for restoration
_original_methods = {}


class AnthropicPatcher(BasePatcher):
    """Patcher for monitoring Anthropic API calls."""

    def __init__(
        self, client: Optional[Any] = None, config: Optional[Dict[str, Any]] = None
    ):
        """Initialize Anthropic patcher.

        Args:
            client: Optional Anthropic client instance to patch
            config: Optional configuration dictionary
        """
        super().__init__(config)
        self.client = client
        self.original_funcs = {}
        self.logger = logging.getLogger("CylestioMonitor.Anthropic")
        self.debug_mode = config.get("debug", False) if config else False

    def patch(self) -> None:
        """Apply monitoring patches to Anthropic client."""
        if not self.client:
            self.logger.warning("No Anthropic client provided, skipping instance patch")
            return

        # Check if this client is already patched
        client_id = id(self.client)
        if client_id in _patched_clients:
            self.logger.warning("Anthropic client already patched, skipping")
            return

        if self.is_patched:
            return

        self.logger.debug("Starting to patch Anthropic client...")

        # Get the underlying create method (accessing the wrapped method if possible)
        if hasattr(self.client.messages, "create"):
            self.logger.debug("Found messages.create method to patch")
            original_create = self.client.messages.create
            # Store the original for unpatch
            self.original_funcs["messages.create"] = original_create

            # Get signature of the original function to ensure compatibility
            sig = inspect.signature(original_create)

            def wrapped_create(*args, **kwargs):
                """Wrapper for Anthropic messages.create that logs but doesn't modify behavior."""
                self.logger.debug("Patched messages.create method called!")

                # Generate a unique span ID for this operation
                span_id = TraceContext.start_span("llm.call")["span_id"]
                trace_id = TraceContext.get_current_context().get("trace_id")

                # Record start time for performance measurement
                start_time = time.time()

                # Extract the complete request data for logging, with error handling
                try:
                    # Get messages from kwargs or args
                    messages = kwargs.get("messages", args[0] if args else [])

                    # Extract all model configuration parameters
                    model = kwargs.get("model", "unknown")
                    max_tokens = kwargs.get("max_tokens")
                    temperature = kwargs.get("temperature")
                    top_p = kwargs.get("top_p")
                    top_k = kwargs.get("top_k")
                    stop_sequences = kwargs.get("stop_sequences")
                    system = kwargs.get("system")

                    # Prepare complete request data
                    request_data = {
                        "messages": self._safe_serialize(messages),
                        "model": model,
                    }

                    # Add optional parameters if present
                    if max_tokens is not None:
                        request_data["max_tokens"] = max_tokens
                    if temperature is not None:
                        request_data["temperature"] = temperature
                    if top_p is not None:
                        request_data["top_p"] = top_p
                    if top_k is not None:
                        request_data["top_k"] = top_k
                    if stop_sequences is not None:
                        request_data["stop_sequences"] = stop_sequences
                    if system is not None:
                        request_data["system"] = system

                    # Security content scanning
                    security_info = self._scan_content_security(messages)

                    # Prepare attributes for the request event
                    request_attributes = {
                        "llm.vendor": "anthropic",
                        "llm.model": model,
                        "llm.request.type": "completion",
                        "llm.request.data": request_data,
                        "llm.request.timestamp": format_timestamp(),
                    }

                    # Add model configuration
                    if max_tokens is not None:
                        request_attributes["llm.request.max_tokens"] = max_tokens
                    if temperature is not None:
                        request_attributes["llm.request.temperature"] = temperature
                    if top_p is not None:
                        request_attributes["llm.request.top_p"] = top_p
                    if top_k is not None:
                        request_attributes["llm.request.top_k"] = top_k

                    # Add security details if something was detected
                    if security_info["alert_level"] != "none":
                        request_attributes["security.alert_level"] = security_info[
                            "alert_level"
                        ]
                        request_attributes["security.keywords"] = security_info[
                            "keywords"
                        ]

                        # Log security event separately
                        self._log_security_event(security_info, request_data)

                    # Log the request with debug mode info if enabled
                    if self.debug_mode:
                        self.logger.debug(
                            f"Request data: {json.dumps(request_data)[:500]}..."
                        )

                    # Log the request event
                    log_event(
                        name="llm.call.start",
                        attributes=request_attributes,
                        level="INFO",
                        span_id=span_id,
                        trace_id=trace_id,
                    )

                except Exception as e:
                    # If logging fails, log the error but don't disrupt the actual API call
                    self.logger.error(f"Error logging request: {e}")
                    if self.debug_mode:
                        self.logger.error(f"Traceback: {traceback.format_exc()}")

                # Call the original function and get the result
                try:
                    self.logger.debug("Calling original messages.create method")
                    result = original_create(*args, **kwargs)
                    self.logger.debug("Original messages.create method returned")

                    # Calculate duration
                    duration_ms = int((time.time() - start_time) * 1000)

                    # Log the response safely
                    try:
                        # Extract structured data from the response
                        response_data = self._extract_response_data(result)

                        # Extract model and token usage if available
                        usage = response_data.get("usage", {})

                        # Prepare attributes for the response event
                        response_attributes = {
                            "llm.vendor": "anthropic",
                            "llm.model": response_data.get("model", model),
                            "llm.response.id": response_data.get("id", ""),
                            "llm.response.type": "completion",
                            "llm.response.timestamp": format_timestamp(),
                            "llm.response.duration_ms": duration_ms,
                            "llm.response.stop_reason": response_data.get(
                                "stop_reason"
                            ),
                        }

                        # Add content data as a sanitized field
                        safe_content = self._safe_serialize(
                            response_data.get("content", [])
                        )
                        response_attributes["llm.response.content"] = safe_content

                        # Add usage statistics if available
                        if "usage" in response_data:
                            usage = response_data["usage"]
                            if "input_tokens" in usage:
                                response_attributes["llm.usage.input_tokens"] = usage["input_tokens"]
                            if "output_tokens" in usage:
                                response_attributes["llm.usage.output_tokens"] = usage["output_tokens"]

                        # Scan response content for security concerns
                        extracted_text = ""
                        # Extract text from content blocks
                        for item in response_data.get("content", []):
                            if isinstance(item, dict) and "text" in item:
                                extracted_text += item["text"] + " "

                        if extracted_text:
                            # Security scanning for response content
                            from cylestio_monitor.security_detection import SecurityScanner
                            scanner = SecurityScanner.get_instance()
                            security_info = scanner.scan_text(extracted_text)

                            # If security issues found, add to attributes and log a separate event
                            if security_info["alert_level"] != "none":
                                response_attributes["security.alert_level"] = security_info["alert_level"]
                                response_attributes["security.keywords"] = security_info["keywords"]
                                response_attributes["security.category"] = security_info["category"]
                                response_attributes["security.severity"] = security_info["severity"]
                                response_attributes["security.description"] = security_info["description"]

                                # Log security event for response content
                                self._log_security_event(security_info, {"content": extracted_text[:100] + "..."})

                                # Log warning
                                self.logger.warning(
                                    f"SECURITY ALERT in LLM RESPONSE: {security_info['alert_level'].upper()} content "
                                    f"detected: {security_info['keywords']}"
                                )

                        # Debug logging
                        if self.debug_mode:
                            self.logger.debug(
                                f"Response data: {json.dumps(safe_content)[:500]}..."
                            )

                        # Log the completion of the operation
                        log_event(
                            name="llm.call.finish",
                            attributes=response_attributes,
                            level="INFO",
                            span_id=span_id,
                            trace_id=trace_id,
                        )
                    except Exception as e:
                        # If response logging fails, log the error but don't disrupt the response
                        error_msg = f"Error logging response: {e}"
                        self.logger.error(error_msg)
                        if self.debug_mode:
                            self.logger.error(f"Traceback: {traceback.format_exc()}")

                        # Log a simplified response event to ensure the span is completed
                        log_event(
                            name="llm.call.finish",
                            attributes={
                                "llm.vendor": "anthropic",
                                "llm.model": model,
                                "llm.response.duration_ms": duration_ms,
                                "error": error_msg,
                            },
                            level="INFO",
                            span_id=span_id,
                            trace_id=trace_id,
                        )

                    # End the span
                    TraceContext.end_span()

                    # Important: Return the original result unchanged
                    return result

                except Exception as e:
                    # Calculate duration up to the error
                    duration_ms = int((time.time() - start_time) * 1000)

                    # If the API call fails, log detailed error information
                    try:
                        error_type = type(e).__name__
                        error_message = str(e)
                        error_traceback = (
                            traceback.format_exc() if self.debug_mode else None
                        )

                        # Prepare attributes for the error event
                        error_attributes = {
                            "llm.vendor": "anthropic",
                            "llm.model": model,
                            "llm.request.type": "completion",
                            "llm.response.duration_ms": duration_ms,
                            "error.type": error_type,
                            "error.message": error_message,
                        }

                        # Add detailed traceback in debug mode
                        if error_traceback:
                            error_attributes["error.traceback"] = error_traceback

                        # Log the error event
                        log_event(
                            name="llm.call.error",
                            attributes=error_attributes,
                            level="ERROR",
                            span_id=span_id,
                            trace_id=trace_id,
                        )
                    except Exception as log_error:
                        # If error logging fails, log basic error info
                        self.logger.error(f"Error logging API error: {log_error}")

                    # End the span
                    TraceContext.end_span()

                    # Re-raise the original exception
                    raise

            # Apply signature from original function (helps with IDE hints/autocomplete)
            wrapped_create.__signature__ = sig
            wrapped_create.__doc__ = original_create.__doc__
            wrapped_create.__name__ = original_create.__name__

            # Replace the method
            self.logger.debug("Replacing original messages.create with wrapped version")
            self.client.messages.create = wrapped_create

            # Mark as patched
            self.is_patched = True
            _patched_clients.add(client_id)
            self.logger.info("Successfully patched Anthropic client")
        else:
            self.logger.warning(
                "Anthropic client doesn't have messages.create method, skipping patch"
            )

    def _safe_serialize(self, obj: Any, depth: int = 0, max_depth: int = 10) -> Any:
        """Safely serialize any object to ensure JSON compatibility.

        Args:
            obj: Object to serialize
            depth: Current recursion depth
            max_depth: Maximum recursion depth to prevent infinite recursion

        Returns:
            JSON-serializable representation of the object
        """
        # Check recursion depth to prevent infinite recursion with circular references
        if depth > max_depth:
            return {"type": "max_depth_reached", "value": str(obj)[:100]}

        # For basic types that are normally JSON serializable, just return them
        if obj is None or isinstance(obj, (str, int, float, bool)):
            return obj

        # Handle custom class objects (detect by checking type name)
        if hasattr(obj, "__class__") and obj.__class__.__module__ != "builtins":
            # Try standard conversion methods first
            if hasattr(obj, "to_dict"):
                try:
                    dict_result = obj.to_dict()
                    return self._safe_serialize(dict_result, depth + 1, max_depth)
                except Exception:
                    pass  # Fall through

            # Try using __dict__ if it exists
            if hasattr(obj, "__dict__"):
                try:
                    attrs = {
                        k: v for k, v in obj.__dict__.items() if not k.startswith("_")
                    }
                    if attrs:  # Only use if there are attributes
                        return self._safe_serialize(attrs, depth + 1, max_depth)
                except Exception:
                    pass  # Fall through

            # For user-defined classes, always use the type/string fallback
            return {
                "type": obj.__class__.__name__,
                "string_value": str(obj)[:1000],  # Limit string length
            }

        # Handle dictionary with special case for circular reference
        if isinstance(obj, dict):
            try:
                # Detect circular reference in the immediate key/value
                if any(k is obj or v is obj for k, v in obj.items()):
                    return {
                        "type": "circular_dict",
                        "keys": list(str(k) for k in obj.keys()),
                    }

                # Process each key/value separately, so one bad value doesn't fail the whole dict
                result = {}
                for k, v in obj.items():
                    try:
                        # Skip entries where key isn't hashable or string convertible
                        str_key = str(k)
                        result[str_key] = self._safe_serialize(v, depth + 1, max_depth)
                    except Exception as e:
                        if self.debug_mode:
                            self.logger.debug(f"Error serializing dict key/value: {e}")

                return result
            except Exception as e:
                if self.debug_mode:
                    self.logger.debug(f"Error in dict serialization: {e}")
                # Fall through to fallback
                return {
                    "type": "dict",
                    "string_value": str(obj)[:1000],  # Limit string length
                }

        # Handle list
        if isinstance(obj, list):
            try:
                return [
                    self._safe_serialize(item, depth + 1, max_depth) for item in obj
                ]
            except Exception as e:
                if self.debug_mode:
                    self.logger.debug(f"Error in list serialization: {e}")
                # Fall through to fallback
                return {
                    "type": "list",
                    "string_value": str(obj)[:1000],  # Limit string length
                }

        # Handle set and tuple (convert to list)
        if isinstance(obj, (set, tuple)):
            try:
                return [
                    self._safe_serialize(item, depth + 1, max_depth) for item in obj
                ]
            except Exception as e:
                if self.debug_mode:
                    self.logger.debug(f"Error in set/tuple serialization: {e}")
                # Fall through to fallback
                return {
                    "type": type(obj).__name__,
                    "string_value": str(obj)[:1000],  # Limit string length
                }

        # Try JSON serialization as a last check before fallback
        try:
            json.dumps(obj)
            return obj
        except (TypeError, OverflowError, ValueError, RecursionError) as e:
            if self.debug_mode:
                self.logger.debug(f"JSON serialization error: {e}")
            # Final fallback
            return {
                "type": type(obj).__name__,
                "string_value": str(obj)[:1000],  # Limit string length
            }

    def _scan_content_security(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Scan content for security concerns.

        Args:
            messages: List of message objects

        Returns:
            Dict with security scan results
        """
        from cylestio_monitor.security_detection import SecurityScanner

        # Get the scanner instance
        scanner = SecurityScanner.get_instance()

        # Find the last user message in the conversation - avoid rescanning history
        last_user_message = None
        if isinstance(messages, list):
            for message in reversed(messages):
                if isinstance(message, dict) and message.get("role") == "user":
                    last_user_message = message
                    break

        # If we found a last user message, only scan that
        if last_user_message:
            scan_result = scanner.scan_text(last_user_message.get("content", ""))
        else:
            # Fallback to scanning the entire conversation if we can't identify the last user message
            scan_result = scanner.scan_event(messages)

        # Map the scanner result to the expected format
        result = {
            "alert_level": scan_result["alert_level"],
            "keywords": scan_result.get("keywords", []),
            "category": scan_result.get("category"),
            "severity": scan_result.get("severity"),
            "description": scan_result.get("description")
        }

        # Log the result if it's not "none"
        if result["alert_level"] != "none":
            self.logger.warning(
                f"Security scan detected {result['alert_level']} content: "
                f"category={result['category']}, severity={result['severity']}, "
                f"description='{result['description']}', keywords={result['keywords']}"
            )

        return result

    def _log_security_event(
        self, security_info: Dict[str, Any], request_data: Dict[str, Any]
    ) -> None:
        """Log a security event for suspicious or dangerous content.

        Args:
            security_info: Security scan results
            request_data: Original request data
        """
        # Only log if there's something to report
        if security_info["alert_level"] == "none" or not security_info["keywords"]:
            return

        # Extract a sample of content for logging
        content_sample = (
            str(request_data)[:100] + "..."
            if len(str(request_data)) > 100
            else str(request_data)
        )

        # Mask sensitive data in the content sample
        from cylestio_monitor.security_detection import SecurityScanner
        scanner = SecurityScanner.get_instance()
        masked_content_sample = scanner._pattern_registry.mask_text_in_place(content_sample)

        # Generate a unique timestamp for this alert
        detection_timestamp = format_timestamp()

        # Generate a unique message ID based on timestamp and keywords
        import hashlib
        alert_hash = hashlib.sha256(f"{detection_timestamp}-{'-'.join(security_info['keywords'])}".encode()).hexdigest()[:8]
        message_id = f"security-{alert_hash}"

        # Create event attributes
        security_attributes = {
            "llm.vendor": "anthropic",
            "security.alert_level": security_info["alert_level"],
            "security.keywords": security_info["keywords"],
            "security.content_sample": masked_content_sample,
            "security.detection_time": detection_timestamp,
            "security.message_id": message_id,
        }

        # Add new security attributes if available
        if "category" in security_info and security_info["category"]:
            security_attributes["security.category"] = security_info["category"]

        if "severity" in security_info and security_info["severity"]:
            security_attributes["security.severity"] = security_info["severity"]

        if "description" in security_info and security_info["description"]:
            security_attributes["security.description"] = security_info["description"]

        # Log appropriate event based on severity
        event_name = f"security.content.{security_info['alert_level']}"

        # Use SECURITY_ALERT level for dangerous content, WARNING for suspicious
        event_level = (
            "SECURITY_ALERT" if security_info["alert_level"] == "dangerous" else "WARNING"
        )

        log_event(name=event_name, attributes=security_attributes, level=event_level)

        # Log to console as well
        self.logger.warning(
            f"SECURITY ALERT {message_id}: {security_info['alert_level'].upper()} content detected: {security_info['keywords']}"
        )

    def _extract_response_data(self, result: Any) -> Dict[str, Any]:
        """Extract structured data from an Anthropic API response.

        Args:
            result: Anthropic API response

        Returns:
            Dict: Structured response data
        """
        if not result:
            return {}

        data = {
            "id": "",
            "model": "unknown",
            "usage": {},
            "type": "text",
            "content": [],
            "role": "assistant",
            "stop_reason": None,
        }

        try:
            # Extract ID
            if hasattr(result, "id"):
                data["id"] = result.id

            # Extract model
            if hasattr(result, "model"):
                data["model"] = result.model

            # Extract stop reason
            if hasattr(result, "stop_reason"):
                data["stop_reason"] = result.stop_reason

            # Extract type
            if hasattr(result, "type"):
                data["type"] = result.type
            elif hasattr(result, "content_type"):
                data["type"] = result.content_type

            # Extract content
            content = ""
            if hasattr(result, "content"):
                for block in result.content:
                    if hasattr(block, "text") and block.text:
                        content += block.text
                        data["content"].append({"type": "text", "text": block.text})
                    elif hasattr(block, "type") and block.type == "text" and hasattr(block, "text"):
                        content += block.text
                        data["content"].append({"type": "text", "text": block.text})

            # Extract usage information - try multiple approaches
            usage = {}

            # Direct attribute access
            if hasattr(result, "usage"):
                usage_obj = result.usage

                # Check if usage is an object with attributes or a dict
                if hasattr(usage_obj, "input_tokens"):
                    usage["input_tokens"] = usage_obj.input_tokens
                    usage["output_tokens"] = getattr(usage_obj, "output_tokens", 0)
                elif isinstance(usage_obj, dict):
                    usage = usage_obj
                elif hasattr(usage_obj, "model_dump"):
                    # Pydantic model
                    usage = usage_obj.model_dump()
                elif hasattr(usage_obj, "dict") and callable(usage_obj.dict):
                    # Legacy pydantic v1
                    usage = usage_obj.dict()
                elif hasattr(usage_obj, "to_dict") and callable(usage_obj.to_dict):
                    # Anthropic-style conversion
                    usage = usage_obj.to_dict()

            # If we don't have usage data, estimate from content length
            if not usage and content:
                # Anthropic has good token usage reporting, but as fallback:
                output_tokens = max(1, len(content) // 4)  # Rough estimate
                input_tokens = max(1, len(content) // 4)  # Rough estimate
                usage = {
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens
                }

                # Log that we're using estimated values
                if self.debug_mode:
                    self.logger.debug(f"Using estimated token counts for Anthropic: {usage}")

            data["usage"] = usage

            # Extract custom fields
            if self.debug_mode:
                self.logger.debug(f"Extracted Anthropic response data: {data}")

            return data
        except Exception as e:
            self.logger.error(f"Error extracting response data: {e}")
            if self.debug_mode:
                import traceback
                self.logger.error(f"Traceback: {traceback.format_exc()}")
            return data

    def unpatch(self) -> None:
        """Restore original methods."""
        if not self.is_patched:
            return

        self.logger.debug("Unpatching Anthropic client...")

        # Restore original methods
        for name, original_func in self.original_funcs.items():
            if name == "messages.create" and hasattr(self.client.messages, "create"):
                self.client.messages.create = original_func

        # Clear stored functions
        self.original_funcs = {}

        # Remove from patched clients
        client_id = id(self.client)
        if client_id in _patched_clients:
            _patched_clients.remove(client_id)

        self.is_patched = False
        self.logger.info("Successfully unpatched Anthropic client")

    @classmethod
    def patch_module(cls) -> None:
        """Apply patching to the Anthropic module itself."""
        global _is_module_patched

        if _is_module_patched:
            return

        # Check if Anthropic is available
        if not ANTHROPIC_AVAILABLE:
            logger = logging.getLogger("CylestioMonitor.Anthropic")
            logger.debug("Anthropic module not available for patching")
            return

        logger = logging.getLogger("CylestioMonitor.Anthropic")
        logger.debug("Patching Anthropic module...")

        try:
            # Patch the Anthropic client class constructor to intercept instance creation
            # This ensures all new instances are automatically patched
            original_init = Anthropic.__init__

            @functools.wraps(original_init)
            def patched_init(self, *args, **kwargs):
                # Call original init
                original_init(self, *args, **kwargs)

                # Patch this instance automatically
                logger.debug("Auto-patching new Anthropic client instance")
                patcher = cls(client=self)
                patcher.patch()

            # Apply our patched constructor
            Anthropic.__init__ = patched_init

            # Store original method for restoration
            _original_methods["Anthropic.__init__"] = original_init

            _is_module_patched = True
            logger.info("Anthropic module patched - all new client instances will be automatically monitored")

        except Exception as e:
            logger.error(f"Failed to patch Anthropic module: {e}")
            if logger.level <= logging.DEBUG:
                import traceback
                logger.debug(f"Traceback: {traceback.format_exc()}")

    @classmethod
    def unpatch_module(cls) -> None:
        """Restore original Anthropic module methods."""
        global _is_module_patched

        if not ANTHROPIC_AVAILABLE or not _is_module_patched:
            return

        # Restore the original __init__ method
        if "Anthropic.__init__" in _original_methods:
            Anthropic.__init__ = _original_methods["Anthropic.__init__"]
            del _original_methods["Anthropic.__init__"]

        _is_module_patched = False
        logger = logging.getLogger("CylestioMonitor.Anthropic")
        logger.info("Unpatched Anthropic module")


def patch_anthropic_module():
    """Patch the Anthropic module."""
    AnthropicPatcher.patch_module()


def unpatch_anthropic_module():
    """Unpatch the Anthropic module."""
    AnthropicPatcher.unpatch_module()
