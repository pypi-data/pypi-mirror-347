from sharedInfo import IDBlocks
from .base64Encode import base64Encode


def EncodeBlockItem(block:dict[str:str|list|tuple]) -> str:
    return f"{IDBlocks[block['id']]}{base64Encode(bytes(block['position']))}{block['rotation']}{base64Encode(bytes(block['colour']))}"
