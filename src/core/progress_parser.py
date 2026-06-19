import re


class RsyncProgressParser:
    _pattern = re.compile(r"^\s*[\d,.]+[KMGTPE]?\s+(\d+)%")

    @classmethod
    def parse(cls, line: str) -> int | None:
        match = cls._pattern.match(line)
        if match:
            return int(match.group(1))
        return None
