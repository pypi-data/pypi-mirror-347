"""
Event monitoring and processing package for Cylestio Monitor.

This package provides modules for:
- Event processing with the EventProcessor
- Event converters for standardized output
- Schema definitions
- OpenTelemetry integration
"""

# Re-export converters
from cylestio_monitor.events.converters import (BaseEventConverter,
                                                EventConverterFactory)
# Re-export processing functionality
from cylestio_monitor.events.processing import (  # Core event processing; Security; Hooks; MCP
    EventProcessor, check_security_concerns, contains_dangerous,
    contains_suspicious, hook_decorator, langchain_input_hook,
    langchain_output_hook, langgraph_state_update_hook, llm_call_hook,
    llm_response_hook, log_event, log_mcp_agent_status_change,
    log_mcp_authentication_event, log_mcp_command_event,
    log_mcp_connection_event, log_mcp_file_transfer, log_mcp_heartbeat,
    mask_sensitive_data, process_standardized_event, register_framework_patch)
# Re-export schema
from cylestio_monitor.events.schema import StandardizedEvent
# Re-export OpenTelemetry utilities
from cylestio_monitor.utils.otel import (create_child_span, generate_span_id,
                                         generate_trace_id,
                                         get_or_create_agent_trace_context)
# Re-export event creation and logging functions
from cylestio_monitor.utils.event_logging import log_event, log_error, log_info, log_warning

# Define __all__ to control what's imported with "from events import *"
__all__ = [
    # Processing core
    "EventProcessor",
    "log_event",
    "process_standardized_event",
    # Event logging
    "log_info",
    "log_warning",
    "log_error",
    # Security
    "contains_suspicious",
    "contains_dangerous",
    "mask_sensitive_data",
    "check_security_concerns",
    # Hooks
    "llm_call_hook",
    "llm_response_hook",
    "langchain_input_hook",
    "langchain_output_hook",
    "langgraph_state_update_hook",
    "register_framework_patch",
    "hook_decorator",
    # MCP
    "log_mcp_connection_event",
    "log_mcp_command_event",
    "log_mcp_heartbeat",
    "log_mcp_file_transfer",
    "log_mcp_agent_status_change",
    "log_mcp_authentication_event",
    # Schema
    "StandardizedEvent",
    # Converters
    "BaseEventConverter",
    "EventConverterFactory",
    # OpenTelemetry
    "generate_trace_id",
    "generate_span_id",
    "create_child_span",
    "get_or_create_agent_trace_context",
]
