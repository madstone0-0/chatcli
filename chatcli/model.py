from dataclasses import dataclass


@dataclass()
class Model:
    """
    Dataclass describing the details of AI Models
    """

    name: str
    nickname: str
    maxTokens: int

    def __post_init__(self):
        self.maxTokens = self.maxTokens or 2048
        self.nickname = self.nickname or self.name

    def __repr__(self) -> str:
        return f"{self.name} ({self.nickname}) - {self.maxTokens} tokens"
