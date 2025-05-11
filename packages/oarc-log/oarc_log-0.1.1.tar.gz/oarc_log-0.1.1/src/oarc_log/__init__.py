"""
   Copyright [2025] [OARC]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

==========================================================================

OARC Crawlers Utilities

This package provides essential utilities for the OARC Crawlers project, including:

- Centralized, context-aware logging for consistent and informative output across all modules
- Standardized error classes to facilitate robust exception handling
- Path management and helper functions to simplify crawler development and maintenance

Import this package to access the `log` object for logging, error types, and utility classes that streamline building and operating OARC crawlers.
"""

from .log import (
    log,
    ContextAwareLogger,
    get_logger,
    redirect_external_loggers,
    enable_debug_logging,
)

__all__ = [
    "log",
    "ContextAwareLogger",
    "get_logger",
    "redirect_external_loggers",
    "enable_debug_logging"
]