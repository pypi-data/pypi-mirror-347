import concurrent.futures
import dataclasses
import enum
import math
import os
import pathlib
import random
import typing

import PIL.Image

from .extractor import (
	VIDEOS,
	Debug,
	Information,
	Order,
	Progress,
	Scale,
	Verbosity,
	extract_directory_frames,
	extract_directory_images,
	extract_directory_infos,
	extract_directory_videos,
	extract_frames,
	extract_information,
)
from .font import load as load_font
from .format import (
	format_information,
	format_information_ex,
	format_name_size,
	format_size,
	format_time,
)
from .histogram import (
	Distribution,
	extract_bands,
	extract_distribution,
	render_histogram,
	trim_distribution,
)
from .layout import Layout, layout, split
from .renderer import render
from .types import Color, Font
from .vignette import Alignment, Cell, Label, Vignette


class Header(enum.IntEnum):
	NONE = 0
	BASIC = 1
	ADVANCED = 2
	TECHNICAL = 3


@dataclasses.dataclass(eq=False, kw_only=True)
class Configuration:
	background: typing.Union[Color, PIL.Image.Image]
	foreground: Color
	accent: Color
	font0: Font
	header: Header
	size: int
	scale: Scale
	font1: Font
	layout: Layout
	columns: typing.Optional[int]
	count: int
	font2: Font
	padding: tuple[int, int]


def configure_video() -> Configuration:
	return Configuration(
		background='black',
		foreground='white',
		accent='white',
		font0=load_font('8x16b'),
		header=Header.ADVANCED,
		size=300,
		scale=Scale.WIDTH,
		font1=load_font('8x14n'),
		layout=Layout.TILED,
		columns=None,
		count=16,
		font2=load_font('8x16n'),
		padding=(8, 8),
	)


def configure_video_collage() -> Configuration:
	return Configuration(
		background='black',
		foreground='white',
		accent='white',
		font0=load_font('8x16b'),
		header=Header.NONE,
		size=192,
		scale=Scale.CROP,
		font1=load_font('8x14n'),
		layout=Layout.TILED,
		columns=5,
		count=30,
		font2=load_font('8x16n'),
		padding=(0, 0),
	)


def configure_image_collage() -> Configuration:
	return Configuration(
		background='black',
		foreground='white',
		accent='white',
		font0=load_font('8x16b'),
		header=Header.NONE,
		size=192,
		scale=Scale.HEIGHT,
		font1=load_font('8x14n'),
		layout=Layout.VARIABLE,
		columns=8,
		count=64,
		font2=load_font('8x16n'),
		padding=(0, 0),
	)


def configure_histogram() -> Configuration:
	return Configuration(
		background='black',
		foreground='white',
		accent='#00ff00',
		font0=load_font('8x16n'),
		header=Header.NONE,
		size=96,
		scale=Scale.HEIGHT,
		font1=load_font('8x14n'),
		layout=Layout.TILED,
		columns=None,
		count=94,
		font2=load_font('8x16b'),
		padding=(8, 2),
	)


def make_video_header(configuration: Configuration, information: Information) -> list[Label]:
	result: list[Label] = []

	if configuration.header == Header.BASIC:
		result.append(
			make_header_label(
				configuration,
				format_name_size(information.name, information.size),
				alignment=Alignment.NEAR,
			)
		)
		result.append(
			make_header_label(
				configuration,
				format_time(information.duration, converter=round),
				alignment=Alignment.FAR,
			)
		)

	elif configuration.header == Header.ADVANCED:
		result.append(make_header_label(configuration, information.name, alignment=Alignment.NEAR))
		result.append(
			make_header_label(configuration, format_size(information.size), alignment=Alignment.FAR)
		)
		result.append(
			make_header_label(
				configuration, format_information(information), alignment=Alignment.NEAR
			)
		)
		result.append(
			make_header_label(
				configuration,
				format_time(information.duration, converter=round),
				alignment=Alignment.FAR,
			)
		)

	elif configuration.header == Header.TECHNICAL:
		result.append(make_header_label(configuration, information.name, alignment=Alignment.NEAR))
		result.append(
			make_header_label(configuration, format_size(information.size), alignment=Alignment.FAR)
		)
		result.append(
			make_header_label(
				configuration, format_information_ex(information), alignment=Alignment.NEAR
			)
		)
		result.append(
			make_header_label(
				configuration,
				format_time(information.duration, converter=round),
				alignment=Alignment.FAR,
			)
		)

	return result


def make_histogram_footer(configuration: Configuration, distribution: Distribution) -> list[Label]:
	return [
		make_footer_label(
			configuration,
			format_time(distribution.minimum, converter=math.floor),
			alignment=Alignment.NEAR,
		),
		make_footer_label(
			configuration,
			format_time(distribution.maximum, converter=math.ceil),
			alignment=Alignment.FAR,
		),
	]


def make_collage_header(
	configuration: Configuration,
	path: typing.Union[os.PathLike[str], str],
	page_index: int,
	page_count: int,
) -> list[Label]:
	if configuration.header == Header.NONE:
		return []

	return [
		make_header_label(configuration, os.path.basename(path), alignment=Alignment.NEAR),
		make_header_label(
			configuration, '{}/{}'.format(page_index + 1, page_count), alignment=Alignment.FAR
		),
	]


def make_header_label(
	configuration: Configuration, text: typing.Optional[str], *, alignment: Alignment
) -> Label:
	return Label(
		text=text,
		font=configuration.font0,
		halignment=alignment,
		valignment=Alignment.MIDDLE,
		color=configuration.foreground,
		border='black' if isinstance(configuration.background, PIL.Image.Image) else None,
	)


def make_footer_label(
	configuration: Configuration, text: typing.Optional[str], *, alignment: Alignment
) -> Label:
	return Label(
		text=text,
		font=configuration.font2,
		halignment=alignment,
		valignment=Alignment.MIDDLE,
		color=configuration.foreground,
		border='black' if isinstance(configuration.background, PIL.Image.Image) else None,
	)


def make_frame_cell(
	configuration: Configuration, timestamp: float, image: typing.Optional[PIL.Image.Image]
) -> Cell:
	return Cell(
		image=image,
		label=Label(
			text=format_time(timestamp, converter=math.floor),
			font=configuration.font1,
			halignment=Alignment.FAR,
			valignment=Alignment.FAR,
			color=configuration.accent,
			border='black',
		),
	)


def make_video_cell(
	configuration: Configuration,
	duration: typing.Optional[float],
	image: typing.Optional[PIL.Image.Image],
) -> Cell:
	if duration is None:
		return Cell(image=image)

	return Cell(
		image=image,
		label=Label(
			text=format_time(duration, converter=round),
			font=configuration.font1,
			halignment=Alignment.FAR,
			valignment=Alignment.FAR,
			color=configuration.accent,
			border='black',
		),
	)


def make_histogram_cell(configuration: Configuration, distribution: Distribution) -> Cell:
	bands = extract_bands(distribution, configuration.count)

	if configuration.columns is None:
		width = configuration.count * (8 + configuration.padding[1]) + 1
	else:
		width = configuration.columns * configuration.size

	background: Color
	if isinstance(configuration.background, PIL.Image.Image):
		background = 'black'
	else:
		background = configuration.background

	return Cell(
		image=render_histogram(
			bands,
			width=width,
			height=configuration.size,
			background=background,
			axis=configuration.foreground,
			bar_color=configuration.accent,
			spacing=configuration.padding[1],
		)
	)


def generate_video(
	configuration: Configuration,
	path: typing.Union[os.PathLike[str], str],
	*,
	progress: typing.Optional[Progress] = None,
	debug: typing.Optional[Debug] = None,
	verbosity: typing.Optional[Verbosity] = None,
	executor: typing.Optional[concurrent.futures.Executor] = None,
) -> Vignette:
	information = extract_information(
		path, debug=debug, verbosity=Verbosity.QUIET if verbosity is None else verbosity
	)
	frames = extract_frames(
		path,
		count=configuration.count,
		duration=information.duration,
		size=configuration.size,
		scale=configuration.scale,
		progress=progress,
		debug=debug,
		verbosity=verbosity,
		executor=executor,
	)

	headers = make_video_header(configuration, information)
	cells = [make_frame_cell(configuration, timestamp, image) for timestamp, image in frames]

	return Vignette(
		background=configuration.background,
		border=configuration.foreground,
		headers=headers,
		cells=cells,
	)


def generate_video_recursive(
	configuration: Configuration,
	path: typing.Union[os.PathLike[str], str],
	*,
	follow_symlinks: bool = False,
	ignore_patterns: typing.Optional[typing.Iterable[str]] = None,
	order: Order = Order.DEFAULT,
	window: typing.Optional[slice] = None,
	progress: typing.Optional[Progress] = None,
	debug: typing.Optional[Debug] = None,
	verbosity: typing.Optional[Verbosity] = None,
	executor: typing.Optional[concurrent.futures.Executor] = None,
	randomizer: typing.Optional[random.Random] = None,
) -> typing.Iterator[tuple[pathlib.Path, Vignette]]:
	result = extract_directory_frames(
		path,
		count=configuration.count,
		follow_symlinks=follow_symlinks,
		ignore_patterns=ignore_patterns,
		order=order,
		window=window,
		size=configuration.size,
		scale=configuration.scale,
		progress=progress,
		debug=debug,
		verbosity=verbosity,
		executor=executor,
		randomizer=randomizer,
	)

	for vpath, information, frames in result:
		headers = make_video_header(configuration, information)
		cells = [make_frame_cell(configuration, timestamp, image) for timestamp, image in frames]

		yield (
			vpath,
			Vignette(
				background=configuration.background,
				border=configuration.foreground,
				headers=headers,
				cells=cells,
			),
		)


def generate_video_collage(
	configuration: Configuration,
	path: typing.Union[os.PathLike[str], str],
	*,
	follow_symlinks: bool = False,
	ignore_patterns: typing.Optional[typing.Iterable[str]] = None,
	order: Order = Order.DEFAULT,
	window: typing.Optional[slice] = None,
	receiver: typing.Optional[typing.Callable[[typing.Optional[int]], None]] = None,
	progress: typing.Optional[Progress] = None,
	debug: typing.Optional[Debug] = None,
	verbosity: typing.Optional[Verbosity] = None,
	executor: typing.Optional[concurrent.futures.Executor] = None,
	randomizer: typing.Optional[random.Random] = None,
) -> typing.Iterator[Vignette]:
	frames = [
		f
		for f in extract_directory_videos(
			path,
			follow_symlinks=follow_symlinks,
			ignore_patterns=ignore_patterns,
			order=order,
			window=window,
			size=configuration.size,
			scale=configuration.scale,
			progress=progress,
			debug=debug,
			verbosity=verbosity,
			executor=executor,
			randomizer=randomizer,
		)
		if f[2] is not None
	]

	chunks, width = split(
		frames,
		lambda f: None if f[2] is None else f[2].width,
		chunk_size=configuration.count,
		mode=configuration.layout,
		columns=configuration.columns,
		spacing=configuration.padding,
	)

	if receiver is not None:
		receiver(width)

	for index, chunk in enumerate(chunks):
		headers = make_collage_header(configuration, path, index, len(chunks))
		cells = [make_video_cell(configuration, info.duration, image) for _, info, image in chunk]

		yield Vignette(
			background=configuration.background,
			border=configuration.foreground,
			headers=headers,
			cells=cells,
		)


def generate_image_collage(
	configuration: Configuration,
	path: typing.Union[os.PathLike[str], str],
	*,
	follow_symlinks: bool = False,
	ignore_patterns: typing.Optional[typing.Iterable[str]] = None,
	order: Order = Order.DEFAULT,
	window: typing.Optional[slice] = None,
	receiver: typing.Optional[typing.Callable[[typing.Optional[int]], None]] = None,
	progress: typing.Optional[Progress] = None,
	debug: typing.Optional[Debug] = None,
	verbosity: typing.Optional[Verbosity] = None,
	executor: typing.Optional[concurrent.futures.Executor] = None,
	randomizer: typing.Optional[random.Random] = None,
) -> typing.Iterator[Vignette]:
	frames = [
		f
		for f in extract_directory_images(
			path,
			follow_symlinks=follow_symlinks,
			ignore_patterns=ignore_patterns,
			order=order,
			window=window,
			size=configuration.size,
			scale=configuration.scale,
			progress=progress,
			debug=debug,
			verbosity=verbosity,
			executor=executor,
			randomizer=randomizer,
		)
		if f[1] is not None
	]

	chunks, width = split(
		frames,
		lambda f: None if f[1] is None else f[1].width,
		chunk_size=configuration.count,
		mode=configuration.layout,
		columns=configuration.columns,
		spacing=configuration.padding,
	)

	if receiver is not None:
		receiver(width)

	for index, chunk in enumerate(chunks):
		headers = make_collage_header(configuration, path, index, len(chunks))
		cells = [Cell(image=image) for _, image in chunk]

		yield Vignette(
			background=configuration.background,
			border=configuration.foreground,
			headers=headers,
			cells=cells,
		)


def generate_histogram(
	configuration: Configuration,
	path: typing.Union[os.PathLike[str], str],
	*,
	follow_symlinks: bool = False,
	ignore_patterns: typing.Optional[typing.Iterable[str]] = None,
	order: Order = Order.DEFAULT,
	window: typing.Optional[slice] = None,
	progress: typing.Optional[Progress] = None,
	debug: typing.Optional[Debug] = None,
	verbosity: typing.Optional[Verbosity] = None,
	executor: typing.Optional[concurrent.futures.Executor] = None,
	randomizer: typing.Optional[random.Random] = None,
) -> Vignette:
	informations = [
		f[1]
		for f in extract_directory_infos(
			path,
			VIDEOS,
			follow_symlinks=follow_symlinks,
			ignore_patterns=ignore_patterns,
			recurse=True,
			order=order,
			window=window,
			progress=progress,
			debug=debug,
			verbosity=verbosity,
			executor=executor,
			randomizer=randomizer,
		)
	]

	distribution_raw = extract_distribution(informations)
	distribution = trim_distribution(distribution_raw)

	footers = make_histogram_footer(configuration, distribution)
	cells = [make_histogram_cell(configuration, distribution)]

	return Vignette(background=configuration.background, border=None, cells=cells, footers=footers)


def compose(
	configuration: Configuration,
	vignette: Vignette,
	*,
	width: typing.Optional[int] = None,
	debug: bool = False,
) -> PIL.Image.Image:
	items = layout(
		vignette,
		mode=configuration.layout,
		columns=configuration.columns,
		width=width,
		spacing=configuration.padding,
	)

	return render(background=configuration.background, items=items, debug=debug)
