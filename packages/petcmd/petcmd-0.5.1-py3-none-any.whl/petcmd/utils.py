
import os
import sys
import inspect
from types import GenericAlias
from typing import Callable, Iterable

from petcmd.exceptions import CommandException

type shell_complete_t = dict[str, Iterable | Callable[[], Iterable | str] | str]

def get_signature(func: Callable):
	"""Returns positionals, keyword, defaults, spec"""
	spec = inspect.getfullargspec(func)
	positionals = spec.args if spec.defaults is None else spec.args[:-len(spec.defaults)]
	keyword = spec.kwonlyargs
	if spec.defaults is not None:
		keyword.extend(spec.args[-len(spec.defaults):])
	defaults = spec.kwonlydefaults or {}
	if spec.defaults is not None:
		defaults.update(dict(zip(spec.args[-len(spec.defaults):], spec.defaults)))
	return positionals, keyword, defaults, spec

class PipeOutput(str):
	pass

class FilePath(str):
	pass

allowed_type_hints = (str, int, float, bool, list, tuple, set, dict, PipeOutput, FilePath)

def validate_type_hints(func: Callable, shell_complete: shell_complete_t = None):
	shell_complete = shell_complete if shell_complete is not None else {}
	pipe_argument = None
	spec = inspect.getfullargspec(func)
	for arg, typehint in spec.annotations.items():
		origin = typehint.__origin__ if isinstance(typehint, GenericAlias) else typehint
		generics = typehint.__args__ if isinstance(typehint, GenericAlias) else []
		if origin not in allowed_type_hints:
			raise CommandException("Unsupported typehint: petcmd supports only basic types: "
				+ ", ".join(map(lambda t: t.__name__, allowed_type_hints)))
		if any(generic not in allowed_type_hints for generic in generics):
			raise CommandException("Unsupported typehint generic: petcmd supports only basic generics: "
				+ ", ".join(map(lambda t: t.__name__, allowed_type_hints)))
		if arg in (spec.varargs, spec.varkw) and origin in (list, tuple, set, dict):
			raise CommandException("Unsupported typehint generic: petcmd doesn't support "
				+ "iterable typehints for *args and **kwargs")
		if origin == bool and shell_complete.get(arg):
			raise CommandException("Unsupported shell complete: bool typehint can't be used with shell completion")
		if origin in (list, set) and generics and generics[0] == bool and shell_complete.get(arg):
			raise CommandException("Unsupported shell complete: bool generic can't be used with shell completion")
		if typehint == PipeOutput and pipe_argument is not None:
			raise CommandException("Invalid typehints: you can't specify more than one PipeOutput argument")
		if typehint == PipeOutput and pipe_argument is None:
			pipe_argument = arg
	if pipe_argument is not None and pipe_argument in (spec.varargs, spec.varkw):
		raise CommandException("Invalid typehints: you can't specify PipeOutput argument as varargs or varkw")

def detect_program_name() -> str:
	_main = sys.modules.get("__main__")
	if _main is not None:
		path = getattr(_main, "__file__", "")
		if path:
			name = os.path.splitext(os.path.basename(path))[0]
			if name and name != "__main__":
				return name
		package = getattr(_main, "__package__", "")
		if package:
			return package.lstrip('.')

	path = sys.argv[0]
	if path and path not in ("-c", "-m"):
		name = os.path.splitext(os.path.basename(path))[0]
		if name and name != "__main__":
			return name

	return "cli"
