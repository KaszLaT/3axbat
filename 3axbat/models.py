from dataclasses import dataclass
from typing import Optional

@dataclass
class Profile:
    user_id: str
    nickname: str
    level: int
    description: str
    country: str
    language: str
    vip_level: int
    raw_data: dict

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            user_id=str(data.get('userId', 'N/A')),
            nickname=data.get('nickName', 'Unknown'),
            level=data.get('level', 0),
            description=data.get('details', ''),
            country=data.get('country', 'N/A'),
            language=data.get('language', 'N/A'),
            vip_level=data.get('vipLv', 0),
            raw_data=data
        )

@dataclass
class Friend:
    user_id: str
    nickname: str
    status: int
    status_text: str
    raw_data: dict

    @classmethod
    def from_dict(cls, data: dict):
        status_code = data.get('status', 0)
        if status_code == 10: status_text = "Online"
        elif status_code == 20: status_text = "In Game"
        elif status_code == 30: status_text = "Offline"
        else: status_text = f"Status {status_code}"
        
        return cls(
            user_id=str(data.get('userId', 'N/A')),
            nickname=data.get('nickName', 'Unknown'),
            status=status_code,
            status_text=status_text,
            raw_data=data
        )