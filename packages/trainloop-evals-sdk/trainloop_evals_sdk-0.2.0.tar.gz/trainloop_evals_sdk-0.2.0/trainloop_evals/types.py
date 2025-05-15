from __future__ import annotations
from typing import TypedDict, Dict, List, Optional


class LLMCallLocation(TypedDict):
    file: str
    lineNumber: str


class ParsedBody(TypedDict, total=False):
    content: List[Dict[str, str]]
    model: str
    modelParams: Dict[str, object]


class CollectedSample(TypedDict):
    durationMs: int
    tag: str
    input: List[Dict[str, str]]
    output: List[Dict[str, str]]
    model: str
    modelParams: Dict[str, object]
    startTimeMs: int
    endTime: int
    url: str
    location: LLMCallLocation


class LLMCallData(TypedDict, total=False):
    requestBodyStr: str
    responseBodyStr: str
    url: str
    tag: str
    location: LLMCallLocation
    startTimeMs: int
    endTimeMs: int
    durationMs: int
    isLLMRequest: bool
    headers: Dict[str, str]
    status: int


class TrainLoopConfigObject(TypedDict):
    data_folder: Optional[str]
    host_allowlist: Optional[List[str]]
    log_level: Optional[str]


class TrainloopConfig(TypedDict):
    trainloop: TrainLoopConfigObject


class RegistryEntry(TypedDict):
    lineNumber: str
    tag: str
    firstSeen: str  # ISO-8601 UTC
    lastSeen: str
    count: int


class Registry(TypedDict):
    schema: int  # always 1 for now
    files: Dict[str, Dict[str, RegistryEntry]]  # file → line → entry
