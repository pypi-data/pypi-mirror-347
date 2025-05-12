"""
YAML Config Processor

A package for processing configuration templates from YAML strings with JSON user configurations.
"""

from yaml_config_processor.processor import ConfigProcessor, TEMPLATE_META_SCHEMA

__version__ = '0.1.1'
__all__ = ['ConfigProcessor', 'TEMPLATE_META_SCHEMA']
