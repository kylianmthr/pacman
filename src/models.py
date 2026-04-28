from pydantic import BaseModel, ConfigDict, Field


class LevelType(BaseModel):
    model_config = ConfigDict(extra="forbid")
    width: int
    height: int


class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")
    highscore_filename: str
    level: list[LevelType]
    lives: int = Field(ge=1)
    pacgum: int = Field(ge=0)
    points_per_pacgum: int = Field(ge=0)
    points_per_super_pacgum: int = Field(ge=0)
    points_per_ghost: int = Field(ge=0)
    seed: int
    level_max_time: int = Field(ge=0)
