from pathlib import Path
from typing import Union

import json


class JSONFile:

    def __init__(self, path: Union[str, Path], auto_create=True) -> None:
        path = Path(path)
        if path.suffix != ".json":
            raise Exception("The file extension must be .json")
        self._path = path
        if auto_create and not self.exists():
            self.write(None)

    @property
    def path(self) -> Path:
        return self._path

    def exists(self) -> bool:
        return self._path.exists()

    def read(self) -> Union[dict, list, None]:
        with open(self._path, "r", encoding="utf-8") as file:
            return json.load(file)

    def write(self, data: Union[dict, list, None]) -> None:
        with open(self._path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def delete(self) -> None:
        self._path.unlink()
