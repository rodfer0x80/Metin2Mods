from pathlib import Path
import json

class Config:
    def __init__(self, filename: Path = Path(".config")):
        self.filename = Path(filename)
        self._data = self._load_config()

    def _load_config(self) -> dict:
        if not self.filename.exists() or self.filename.stat().st_size == 0:
            return self._default_config()

        try:
            with self.filename.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            # fallback to defaults if config is corrupted
            return self._default_config()

    def _default_config(self) -> dict:
        return {
            "spiritStoneCost": 3,
            "profitMargin": 10,
        }

    def save(self):
        with self.filename.open("w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=4)

    @property
    def spiritStoneCost(self) -> int:
        return self._data.get("spiritStoneCost", 3)

    @spiritStoneCost.setter
    def spiritStoneCost(self, value: int):
        self._data["spiritStoneCost"] = value

    @property
    def profitMargin(self) -> float:
        return self._data.get("profitMargin", 10)

    @profitMargin.setter
    def profitMargin(self, value: float):
        self._data["profitMargin"] = value