from dataclasses import dataclass, field


DEFAULT_RSYNC_OPTIONS = ["-avh", "--progress"]


@dataclass
class RsyncConfig:
    source: str = ""
    destination: str = ""
    extra_options: str = ""
    dry_run: bool = False
    delete: bool = False
    compress: bool = False
    partial: bool = False
    bwlimit: str = ""

    def build_args(self) -> list[str]:
        args = list(DEFAULT_RSYNC_OPTIONS)
        if self.dry_run:
            args.append("--dry-run")
        if self.delete:
            args.append("--delete")
        if self.compress:
            args.append("-z")
        if self.partial:
            args.append("--partial")
        if self.bwlimit:
            args.extend(["--bwlimit", self.bwlimit.strip()])
        if self.extra_options:
            args.extend(self.extra_options.strip().split())
        args.append(self.source.rstrip("/") + "/")
        args.append(self.destination)
        return args
