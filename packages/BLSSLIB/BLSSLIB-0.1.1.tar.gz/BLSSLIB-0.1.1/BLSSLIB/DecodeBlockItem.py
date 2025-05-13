from sharedInfo import BlockIDs
from base64Decode import base64Decode

def DecodeBlockItem(raw:str) -> dict[str:str|list|tuple]:
    return {
        "id": BlockIDs[raw[0]],
        "positon": tuple(base64Decode(raw[1:5])),
        "rotation": raw[5],
        "colour": tuple(base64Decode(raw[6:]))
    }
