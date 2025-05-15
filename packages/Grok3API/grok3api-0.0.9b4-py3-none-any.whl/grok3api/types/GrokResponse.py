from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict, Union

from grok3api.logger import logger
from grok3api.types.GeneratedImage import GeneratedImage


@dataclass
class ModelResponse:
    responseId: str
    message: str
    sender: str
    createTime: str
    parentResponseId: str
    manual: bool
    partial: bool
    shared: bool
    query: str
    queryType: str
    webSearchResults: List[Any] = field(default_factory=list)
    xpostIds: List[Any] = field(default_factory=list)
    xposts: List[Any] = field(default_factory=list)
    generatedImages: List[GeneratedImage] = field(default_factory=list)
    imageAttachments: List[Any] = field(default_factory=list)
    fileAttachments: List[Any] = field(default_factory=list)
    cardAttachmentsJson: List[Any] = field(default_factory=list)
    fileUris: List[Any] = field(default_factory=list)
    fileAttachmentsMetadata: List[Any] = field(default_factory=list)
    isControl: bool = False
    steps: List[Any] = field(default_factory=list)
    mediaTypes: List[Any] = field(default_factory=list)

    def __init__(self, data: Dict[str, Any]):
        try:
            self.responseId = data.get("responseId", "")
            self.message = data.get("message", "")
            self.sender = data.get("sender", "")
            self.createTime = data.get("createTime", "")
            self.parentResponseId = data.get("parentResponseId", "")
            self.manual = data.get("manual", False)
            self.partial = data.get("partial", False)
            self.shared = data.get("shared", False)
            self.query = data.get("query", "")
            self.queryType = data.get("queryType", "")
            self.webSearchResults = data.get("webSearchResults", [])
            self.xpostIds = data.get("xpostIds", [])
            self.xposts = data.get("xposts", [])

            self.generatedImages = []
            for url in data.get("generatedImageUrls", []):
                self.generatedImages.append(GeneratedImage(url=url))

            self.imageAttachments = data.get("imageAttachments", [])
            self.fileAttachments = data.get("fileAttachments", [])
            self.cardAttachmentsJson = data.get("cardAttachmentsJson", [])
            self.fileUris = data.get("fileUris", [])
            self.fileAttachmentsMetadata = data.get("fileAttachmentsMetadata", [])
            self.isControl = data.get("isControl", False)
            self.steps = data.get("steps", [])
            self.mediaTypes = data.get("mediaTypes", [])
        except Exception as e:
            logger.error(f"В ModelResponse.__init__: {str(e)}")


@dataclass
class GrokResponse:
    modelResponse: ModelResponse
    isThinking: bool
    isSoftStop: bool
    responseId: str

    conversationId: Optional[str] = None
    title: Optional[str] = None
    conversationCreateTime: Optional[str] = None
    conversationModifyTime: Optional[str] = None
    temporary: Optional[bool] = None

    error: Optional[str] = None
    error_code: Optional[Union[int, str]] = None

    def __init__(self, data: Dict[str, Any]):
        try:
            self.error = data.get("error", None)
            self.error_code = data.get("error_code", None)
            result = data.get("result", {})
            response_data = result.get("response", {})

            self.modelResponse = ModelResponse(response_data.get("modelResponse", {}))
            self.isThinking = response_data.get("isThinking", False)
            self.isSoftStop = response_data.get("isSoftStop", False)
            self.responseId = response_data.get("responseId", "")

            self.conversationId = response_data.get("conversationId")
            self.title = result.get("newTitle") or result.get("title") or self.title
            self.conversationCreateTime = response_data.get("createTime")
            self.conversationModifyTime = response_data.get("modifyTime")
            self.temporary = response_data.get("temporary")
        except Exception as e:
            self.error = str(e) if self.error is None else self.error + ' ' + str(e)
            logger.error(f"В GrokResponse.__init__: {e}")
