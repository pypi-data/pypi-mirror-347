import importlib
import sys
import time
import typing


class ConsoleProgress:
	def __init__(self, stream: typing.TextIO) -> None:
		if sys.platform == 'win32':
			colorama = importlib.import_module('colorama')
			colorama.just_fix_windows_console()

		self.stream: typing.Optional[typing.TextIO] = stream
		self.last: typing.Optional[float] = None

	def __call__(self, text: str, position: int, total: int) -> None:
		if self.stream is None:
			return

		now = time.monotonic()
		pct = min(max((position / total) * 100.0, 0.0), 100.0) if total else 0.0
		update = self.last is None or now - self.last >= 0.1 or pct >= 100.0

		if not update:
			return

		self.stream.write('\r\x1b[2K\x1b[1m[{:5.1f}%]\x1b[0m {}'.format(pct, text))
		self.stream.flush()
		self.last = now

	def close(self) -> None:
		if self.stream is None:
			return

		if self.last is not None:
			self.stream.write('\r\x1b[2K')
			self.stream.flush()

		self.last = None
		self.stream = None
