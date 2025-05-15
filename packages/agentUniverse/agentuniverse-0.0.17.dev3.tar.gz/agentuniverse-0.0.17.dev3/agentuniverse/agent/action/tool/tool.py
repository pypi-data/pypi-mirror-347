# !/usr/bin/env python3
# -*- coding:utf-8 -*-
import asyncio
# @Time    : 2024/3/13 14:29
# @Author  : wangchongshi
# @Email   : wangchongshi.wcs@antgroup.com
# @FileName: tool.py
from abc import abstractmethod
import json
from typing import List, Optional

from pydantic import BaseModel
from langchain.tools import Tool as LangchainTool

from agentuniverse.agent.action.tool.enum import ToolTypeEnum
from agentuniverse.base.annotation.trace import trace_tool
from agentuniverse.base.component.component_base import ComponentBase
from agentuniverse.base.component.component_enum import ComponentEnum
from agentuniverse.base.config.application_configer.application_config_manager import ApplicationConfigManager
from agentuniverse.base.config.component_configer.configers.tool_configer import ToolConfiger


class ToolInput(BaseModel):
    """The basic class for tool input."""

    def __init__(self, params: dict, **kwargs):
        super().__init__(**kwargs)
        self.__origin_params = params
        for k, v in params.items():
            self.__dict__[k] = v

    def to_dict(self):
        return self.__origin_params

    def to_json_str(self):
        return json.dumps(self.__origin_params, ensure_ascii=False)

    def add_data(self, key, value):
        self.__origin_params[key] = value
        self.__dict__[key] = value

    def get_data(self, key, default=None):
        return self.__origin_params.get(key, default)


class Tool(ComponentBase):
    """
    The basic class for tool model.

    Attributes:
        name (str): The name of the tool.
        description (str): The description of the tool.
        tool_type (ToolTypeEnum): The type of the tool.
        input_keys (Optional[List]): The input keys of the tool, e.g. ['input1', 'input2']
    """

    name: str = ""
    description: Optional[str] = None
    tool_type: ToolTypeEnum = ToolTypeEnum.FUNC
    input_keys: Optional[List] = None
    tracing: Optional[bool] = None

    def __init__(self, **kwargs):
        super().__init__(component_type=ComponentEnum.TOOL, **kwargs)

    @trace_tool
    def run(self, **kwargs):
        """The callable method that runs the tool."""
        self.input_check(kwargs)
        tool_input = ToolInput(kwargs)
        return self.execute(tool_input)

    @trace_tool
    async def async_run(self, **kwargs):
        """The callable method that runs the tool."""
        self.input_check(kwargs)
        tool_input = ToolInput(kwargs)
        return await self.async_execute(tool_input)

    def input_check(self, kwargs: dict) -> None:
        """Check whether the input parameters of the tool contain input keys of the tool"""
        if self.input_keys:
            for key in self.input_keys:
                if key not in kwargs.keys():
                    raise Exception(f'{self.get_instance_code()} - The input must include key: {key}.')

    @trace_tool
    def langchain_run(self, *args, callbacks=None, **kwargs):
        """The callable method that runs the tool."""
        kwargs["callbacks"] = callbacks
        tool_input = ToolInput(kwargs)
        parse_result = self.parse_react_input(args[0])
        for key in self.input_keys:
            tool_input.add_data(key, parse_result[key])
        return self.execute(tool_input)

    @trace_tool
    async def async_langchain_run(self, *args, callbacks=None, **kwargs):
        kwargs["callbacks"] = callbacks
        tool_input = ToolInput(kwargs)
        parse_result = self.parse_react_input(args[0])
        for key in self.input_keys:
            tool_input.add_data(key, parse_result[key])
        return await self.async_execute(tool_input)

    def parse_react_input(self, input_str: str):
        """
            parse react string to you input
            you can define your own logic here by override this function
        """
        return {
            self.input_keys[0]: input_str
        }

    @abstractmethod
    def execute(self, tool_input: ToolInput):
        raise NotImplementedError

    async def async_execute(self, tool_input: ToolInput):
        """The callable method that runs the tool."""
        return await asyncio.to_thread(self.execute, tool_input)

    def as_langchain(self) -> LangchainTool:
        """Convert the agentUniverse(aU) tool class to the langchain tool class."""
        return LangchainTool(name=self.name,
                             func=self.langchain_run,
                             description=self.description)

    async def async_as_langchain(self) -> LangchainTool:
        return LangchainTool(name=self.name,
                             func=self.run,
                             coroutine=self.async_langchain_run,
                             description=self.description)

    def get_instance_code(self) -> str:
        """Return the full name of the tool."""
        appname = ApplicationConfigManager().app_configer.base_info_appname
        return f'{appname}.{self.component_type.value.lower()}.{self.name}'

    def initialize_by_component_configer(self, component_configer: ToolConfiger) -> 'Tool':
        """Initialize the LLM by the ComponentConfiger object.
        Args:
            component_configer(LLMConfiger): the ComponentConfiger object
        Returns:
            Tool: the Tool object
        """
        try:
            # First handle the main configuration values
            for key, value in component_configer.configer.value.items():
                if key != 'metadata' and key != 'meta_class':  # Skip metadata field
                    setattr(self, key, value)
        except Exception as e:
            print(f"Error during configuration initialization: {str(e)}")
        if component_configer.name:
            self.name = component_configer.name
        if component_configer.description:
            self.description = component_configer.description
        if component_configer.tool_type:
            self.tool_type = next((member for member in ToolTypeEnum if member.value == component_configer.tool_type))
        if component_configer.input_keys:
            self.input_keys = component_configer.input_keys
        if hasattr(component_configer, "tracing"):
            self.tracing = component_configer.tracing
        return self

    def create_copy(self):
        copied = self.model_copy()
        if self.input_keys is not None:
            copied.input_keys = self.input_keys.copy()
        return copied
