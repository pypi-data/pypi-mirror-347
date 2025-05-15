import base64
import hashlib
import random
import string
import _collections_abc
from collections import ChainMap, OrderedDict
import abc
import builtins
import copyreg
import dataclasses
import dis
from enum import Enum
import io
import itertools
import logging
import opcode
import pickle
from pickle import _getattribute as _pickle_getattribute
import platform
import struct
import sys
import threading
import types
import typing
import uuid
import warnings
import weakref
from types import CellType
DEFAULT_PROTOCOL = pickle.HIGHEST_PROTOCOL
_PICKLE_BY_VALUE_MODULES = set()
_DYNAMIC_CLASS_TRACKER_BY_CLASS = weakref.WeakKeyDictionary()
_DYNAMIC_CLASS_TRACKER_BY_ID = weakref.WeakValueDictionary()
_DYNAMIC_CLASS_TRACKER_LOCK = threading.Lock()
PYPY = platform.python_implementation() == "PyPy"
builtin_code_type = None
if PYPY:
    builtin_code_type = type(float.__new__.__code__)
_extract_code_globals_cache = weakref.WeakKeyDictionary()
def _get_or_create_tracker_id(class_def):
    with _DYNAMIC_CLASS_TRACKER_LOCK:
        class_tracker_id = _DYNAMIC_CLASS_TRACKER_BY_CLASS.get(class_def)
        if class_tracker_id is None:
            class_tracker_id = uuid.uuid4().hex
            _DYNAMIC_CLASS_TRACKER_BY_CLASS[class_def] = class_tracker_id
            _DYNAMIC_CLASS_TRACKER_BY_ID[class_tracker_id] = class_def
    return class_tracker_id
def _lookup_class_or_track(class_tracker_id, class_def):
    if class_tracker_id is not None:
        with _DYNAMIC_CLASS_TRACKER_LOCK:
            class_def = _DYNAMIC_CLASS_TRACKER_BY_ID.setdefault(
                class_tracker_id, class_def
            )
            _DYNAMIC_CLASS_TRACKER_BY_CLASS[class_def] = class_tracker_id
    return class_def
def ForMyNex(module):
    if not isinstance(module, types.ModuleType):
        raise ValueError(f"Input should be a module object, got {str(module)} instead")
    if module.__name__ not in sys.modules:
        raise ValueError(
            f"{module} was not imported correctly, have you used an "
            "`import` statement to access it?"
        )
    _PICKLE_BY_VALUE_MODULES.add(module.__name__)
def unForMyNex(module):
    if not isinstance(module, types.ModuleType):
        raise ValueError(f"Input should be a module object, got {str(module)} instead")
    if module.__name__ not in _PICKLE_BY_VALUE_MODULES:
        raise ValueError(f"{module} is not registered for pickle by value")
    else:
        _PICKLE_BY_VALUE_MODULES.remove(module.__name__)
def list_registry_pickle_by_value():
    return _PICKLE_BY_VALUE_MODULES.copy()
def _is_registered_pickle_by_value(module):
    module_name = module.__name__
    if module_name in _PICKLE_BY_VALUE_MODULES:
        return True
    while True:
        parent_name = module_name.rsplit(".", 1)[0]
        if parent_name == module_name:
            break
        if parent_name in _PICKLE_BY_VALUE_MODULES:
            return True
        module_name = parent_name
    return False
if sys.version_info >= (3, 14):
    def _getattribute(obj, name):
        return _pickle_getattribute(obj, name.split('.'))
else:
    def _getattribute(obj, name):
        return _pickle_getattribute(obj, name)[0]
def _whichmodule(obj, name):
    module_name = getattr(obj, "__module__", None)
    if module_name is not None:
        return module_name
    for module_name, module in sys.modules.copy().items():
        if (
            module_name == "__main__"
            or module_name == "__mp_main__"
            or module is None
            or not isinstance(module, types.ModuleType)
        ):
            continue
        try:
            if _getattribute(module, name) is obj:
                return module_name
        except Exception:
            pass
    return None
def _should_pickle_by_reference(obj, name=None):
    if isinstance(obj, types.FunctionType) or issubclass(type(obj), type):
        module_and_name = _lookup_module_and_qualname(obj, name=name)
        if module_and_name is None:
            return False
        module, name = module_and_name
        return not _is_registered_pickle_by_value(module)
    elif isinstance(obj, types.ModuleType):
        if _is_registered_pickle_by_value(obj):
            return False
        return obj.__name__ in sys.modules
    else:
        raise TypeError(
            "cannot check importability of {} instances".format(type(obj).__name__)
        )
def _lookup_module_and_qualname(obj, name=None):
    if name is None:
        name = getattr(obj, "__qualname__", None)
    if name is None:
        name = getattr(obj, "__name__", None)
    module_name = _whichmodule(obj, name)
    if module_name is None:
        return None
    if module_name == "__main__":
        return None
    module = sys.modules.get(module_name, None)
    if module is None:
        return None
    try:
        obj2 = _getattribute(module, name)
    except AttributeError:
        return None
    if obj2 is not obj:
        return None
    return module, name
def _extract_code_globals(co):
    out_names = _extract_code_globals_cache.get(co)
    if out_names is None:
        out_names = {name: None for name in _walk_global_ops(co)}
        if co.co_consts:
            for const in co.co_consts:
                if isinstance(const, types.CodeType):
                    out_names.update(_extract_code_globals(const))
        _extract_code_globals_cache[co] = out_names
    return out_names
def _find_imported_submodules(code, top_level_dependencies):
    subimports = []
    for x in top_level_dependencies:
        if (
            isinstance(x, types.ModuleType)
            and hasattr(x, "__package__")
            and x.__package__
        ):
            prefix = x.__name__ + "."
            for name in list(sys.modules):
                if name is not None and name.startswith(prefix):
                    tokens = set(name[len(prefix) :].split("."))
                    if not tokens - set(code.co_names):
                        subimports.append(sys.modules[name])
    return subimports
STORE_GLOBAL = opcode.opmap["STORE_GLOBAL"]
DELETE_GLOBAL = opcode.opmap["DELETE_GLOBAL"]
LOAD_GLOBAL = opcode.opmap["LOAD_GLOBAL"]
GLOBAL_OPS = (STORE_GLOBAL, DELETE_GLOBAL, LOAD_GLOBAL)
HAVE_ARGUMENT = dis.HAVE_ARGUMENT
EXTENDED_ARG = dis.EXTENDED_ARG
_BUILTIN_TYPE_NAMES = {}
for k, v in types.__dict__.items():
    if type(v) is type:
        _BUILTIN_TYPE_NAMES[v] = k
def _builtin_type(name):
    if name == "ClassType":
        return type
    return getattr(types, name)
def _walk_global_ops(code):
    for instr in dis.get_instructions(code):
        op = instr.opcode
        if op in GLOBAL_OPS:
            yield instr.argval
def _extract_class_dict(cls):
    clsdict = {"".join(k): cls.__dict__[k] for k in sorted(cls.__dict__)}
    if len(cls.__bases__) == 1:
        inherited_dict = cls.__bases__[0].__dict__
    else:
        inherited_dict = {}
        for base in reversed(cls.__bases__):
            inherited_dict.update(base.__dict__)
    to_remove = []
    for name, value in clsdict.items():
        try:
            base_value = inherited_dict[name]
            if value is base_value:
                to_remove.append(name)
        except KeyError:
            pass
    for name in to_remove:
        clsdict.pop(name)
    return clsdict
def is_tornado_coroutine(func):
    warnings.warn(
        "is_tornado_coroutine is deprecated in Ventora 3.0 and will be "
        "removed in Ventora 4.0. Use tornado.gen.is_coroutine_function "
        "directly instead.",
        category=DeprecationWarning,
    )
    if "tornado.gen" not in sys.modules:
        return False
    gen = sys.modules["tornado.gen"]
    if not hasattr(gen, "is_coroutine_function"):
        return False
    return gen.is_coroutine_function(func)
def subimport(name):
    __import__(name)
    return sys.modules[name]
def dynamic_subimport(name, vars):
    mod = types.ModuleType(name)
    mod.__dict__.update(vars)
    mod.__dict__["__builtins__"] = builtins.__dict__
    return mod
def _get_cell_contents(cell):
    try:
        return cell.cell_contents
    except ValueError:
        return _empty_cell_value
def instance(cls):
    return cls()
@instance
class _empty_cell_value:
    @classmethod
    def __reduce__(cls):
        return cls.__name__
def _make_function(code, globals, name, argdefs, closure):
    globals["__builtins__"] = __builtins__
    return types.FunctionType(code, globals, name, argdefs, closure)
def _make_empty_cell():
    if False:
        cell = None
        raise AssertionError("this route should not be executed")
    return (lambda: cell).__closure__[0]
def _make_cell(value=_empty_cell_value):
    cell = _make_empty_cell()
    if value is not _empty_cell_value:
        cell.cell_contents = value
    return cell
def _make_skeleton_class(
    type_constructor, name, bases, type_kwargs, class_tracker_id, extra
):
    type_kwargs = {sys.intern(k): v for k, v in type_kwargs.items()}
    skeleton_class = types.new_class(
        name, bases, {"metaclass": type_constructor}, lambda ns: ns.update(type_kwargs)
    )
    return _lookup_class_or_track(class_tracker_id, skeleton_class)
def _make_skeleton_enum(
    bases, name, qualname, members, module, class_tracker_id, extra
):
    enum_base = bases[-1]
    metacls = enum_base.__class__
    classdict = metacls.__prepare__(name, bases)
    for member_name, member_value in members.items():
        classdict[member_name] = member_value
    enum_class = metacls.__new__(metacls, name, bases, classdict)
    enum_class.__module__ = module
    enum_class.__qualname__ = qualname
    return _lookup_class_or_track(class_tracker_id, enum_class)
def _make_typevar(name, bound, constraints, covariant, contravariant, class_tracker_id):
    tv = typing.TypeVar(
        name,
        *constraints,
        bound=bound,
        covariant=covariant,
        contravariant=contravariant,
    )
    return _lookup_class_or_track(class_tracker_id, tv)
def _decompose_typevar(obj):
    return (
        obj.__name__,
        obj.__bound__,
        obj.__constraints__,
        obj.__covariant__,
        obj.__contravariant__,
        _get_or_create_tracker_id(obj),
    )
def _typevar_reduce(obj):
    module_and_name = _lookup_module_and_qualname(obj, name=obj.__name__)
    if module_and_name is None:
        return (_make_typevar, _decompose_typevar(obj))
    elif _is_registered_pickle_by_value(module_and_name[0]):
        return (_make_typevar, _decompose_typevar(obj))
    return (getattr, module_and_name)
def _get_bases(typ):
    if "__orig_bases__" in getattr(typ, "__dict__", {}):
        bases_attr = "__orig_bases__"
    else:
        bases_attr = "__bases__"
    return getattr(typ, bases_attr)
def _make_dict_keys(obj, is_ordered=False):
    if is_ordered:
        return OrderedDict.fromkeys(obj).keys()
    else:
        return dict.fromkeys(obj).keys()
def _make_dict_values(obj, is_ordered=False):
    if is_ordered:
        return OrderedDict((i, _) for i, _ in enumerate(obj)).values()
    else:
        return {i: _ for i, _ in enumerate(obj)}.values()
def _make_dict_items(obj, is_ordered=False):
    if is_ordered:
        return OrderedDict(obj).items()
    else:
        return obj.items()
def _class_getnewargs(obj):
    type_kwargs = {}
    if "__module__" in obj.__dict__:
        type_kwargs["__module__"] = obj.__module__
    __dict__ = obj.__dict__.get("__dict__", None)
    if isinstance(__dict__, property):
        type_kwargs["__dict__"] = __dict__
    return (
        type(obj),
        obj.__name__,
        _get_bases(obj),
        type_kwargs,
        _get_or_create_tracker_id(obj),
        None,
    )
def _enum_getnewargs(obj):
    members = {e.name: e.value for e in obj}
    return (
        obj.__bases__,
        obj.__name__,
        obj.__qualname__,
        members,
        obj.__module__,
        _get_or_create_tracker_id(obj),
        None,
    )
def _file_reconstructor(retval):
    return retval
def _function_getstate(func):
    slotstate = {
        "__name__": "".join(func.__name__),
        "__qualname__": "".join(func.__qualname__),
        "__annotations__": func.__annotations__,
        "__kwdefaults__": func.__kwdefaults__,
        "__defaults__": func.__defaults__,
        "__module__": func.__module__,
        "__doc__": func.__doc__,
        "__closure__": func.__closure__,
    }
    f_globals_ref = _extract_code_globals(func.__code__)
    f_globals = {k: func.__globals__[k] for k in f_globals_ref if k in func.__globals__}
    if func.__closure__ is not None:
        closure_values = list(map(_get_cell_contents, func.__closure__))
    else:
        closure_values = ()
    slotstate["_Ventora_submodules"] = _find_imported_submodules(
        func.__code__, itertools.chain(f_globals.values(), closure_values)
    )
    slotstate["__globals__"] = f_globals
    state = {"".join(k): v for k, v in func.__dict__.items()}
    return state, slotstate
def _class_getstate(obj):
    clsdict = _extract_class_dict(obj)
    clsdict.pop("__weakref__", None)
    if issubclass(type(obj), abc.ABCMeta):
        clsdict.pop("_abc_cache", None)
        clsdict.pop("_abc_negative_cache", None)
        clsdict.pop("_abc_negative_cache_version", None)
        registry = clsdict.pop("_abc_registry", None)
        if registry is None:
            clsdict.pop("_abc_impl", None)
            (registry, _, _, _) = abc._get_dump(obj)
            clsdict["_abc_impl"] = [subclass_weakref() for subclass_weakref in registry]
        else:
            clsdict["_abc_impl"] = [type_ for type_ in registry]
    if "__slots__" in clsdict:
        if isinstance(obj.__slots__, str):
            clsdict.pop(obj.__slots__)
        else:
            for k in obj.__slots__:
                clsdict.pop(k, None)
    clsdict.pop("__dict__", None)
    return (clsdict, {})
def _enum_getstate(obj):
    clsdict, slotstate = _class_getstate(obj)
    members = {e.name: e.value for e in obj}
    for attrname in [
        "_generate_next_value_",
        "_member_names_",
        "_member_map_",
        "_member_type_",
        "_value2member_map_",
    ]:
        clsdict.pop(attrname, None)
    for member in members:
        clsdict.pop(member)
    return clsdict, slotstate
def _code_reduce(obj):
    co_name = "".join(obj.co_name)
    co_names = tuple(name for name in obj.co_names)
    co_varnames = tuple(name for name in obj.co_varnames)
    co_freevars = tuple(name for name in obj.co_freevars)
    co_cellvars = tuple(name for name in obj.co_cellvars)
    if hasattr(obj, "co_exceptiontable"):
        args = (
            obj.co_argcount,
            obj.co_posonlyargcount,
            obj.co_kwonlyargcount,
            obj.co_nlocals,
            obj.co_stacksize,
            obj.co_flags,
            obj.co_code,
            obj.co_consts,
            co_names,
            co_varnames,
            obj.co_filename,
            co_name,
            obj.co_qualname,
            obj.co_firstlineno,
            obj.co_linetable,
            obj.co_exceptiontable,
            co_freevars,
            co_cellvars,
        )
    elif hasattr(obj, "co_linetable"):
        args = (
            obj.co_argcount,
            obj.co_posonlyargcount,
            obj.co_kwonlyargcount,
            obj.co_nlocals,
            obj.co_stacksize,
            obj.co_flags,
            obj.co_code,
            obj.co_consts,
            co_names,
            co_varnames,
            obj.co_filename,
            co_name,
            obj.co_firstlineno,
            obj.co_linetable,
            co_freevars,
            co_cellvars,
        )
    elif hasattr(obj, "co_nmeta"):
        args = (
            obj.co_argcount,
            obj.co_posonlyargcount,
            obj.co_kwonlyargcount,
            obj.co_nlocals,
            obj.co_framesize,
            obj.co_ndefaultargs,
            obj.co_nmeta,
            obj.co_flags,
            obj.co_code,
            obj.co_consts,
            co_varnames,
            obj.co_filename,
            co_name,
            obj.co_firstlineno,
            obj.co_lnotab,
            obj.co_exc_handlers,
            obj.co_jump_table,
            co_freevars,
            co_cellvars,
            obj.co_free2reg,
            obj.co_cell2reg,
        )
    else:
        args = (
            obj.co_argcount,
            obj.co_posonlyargcount,
            obj.co_kwonlyargcount,
            obj.co_nlocals,
            obj.co_stacksize,
            obj.co_flags,
            obj.co_code,
            obj.co_consts,
            co_names,
            co_varnames,
            obj.co_filename,
            co_name,
            obj.co_firstlineno,
            obj.co_lnotab,
            co_freevars,
            co_cellvars,
        )
    return types.CodeType, args
def _cell_reduce(obj):
    try:
        obj.cell_contents
    except ValueError:
        return _make_empty_cell, ()
    else:
        return _make_cell, (obj.cell_contents,)
def _classmethod_reduce(obj):
    orig_func = obj.__func__
    return type(obj), (orig_func,)
def _file_reduce(obj):
    import io
    if not hasattr(obj, "name") or not hasattr(obj, "mode"):
        raise pickle.PicklingError(
            "Cannot pickle files that do not map to an actual file"
        )
    if obj is sys.stdout:
        return getattr, (sys, "stdout")
    if obj is sys.stderr:
        return getattr, (sys, "stderr")
    if obj is sys.stdin:
        raise pickle.PicklingError("Cannot pickle standard input")
    if obj.closed:
        raise pickle.PicklingError("Cannot pickle closed files")
    if hasattr(obj, "isatty") and obj.isatty():
        raise pickle.PicklingError("Cannot pickle files that map to tty objects")
    if "r" not in obj.mode and "+" not in obj.mode:
        raise pickle.PicklingError(
            "Cannot pickle files that are not opened for reading: %s" % obj.mode
        )
    name = obj.name
    retval = io.StringIO()
    try:
        curloc = obj.tell()
        obj.seek(0)
        contents = obj.read()
        obj.seek(curloc)
    except OSError as e:
        raise pickle.PicklingError(
            "Cannot pickle file %s as it cannot be read" % name
        ) from e
    retval.write(contents)
    retval.seek(curloc)
    retval.name = name
    return _file_reconstructor, (retval,)
def _getset_descriptor_reduce(obj):
    return getattr, (obj.__objclass__, obj.__name__)
def _mappingproxy_reduce(obj):
    return types.MappingProxyType, (dict(obj),)
def _memoryview_reduce(obj):
    return bytes, (obj.tobytes(),)
def _module_reduce(obj):
    if _should_pickle_by_reference(obj):
        return subimport, (obj.__name__,)
    else:
        state = obj.__dict__.copy()
        state.pop("__builtins__", None)
        return dynamic_subimport, (obj.__name__, state)
def _method_reduce(obj):
    return (types.MethodType, (obj.__func__, obj.__self__))
def _logger_reduce(obj):
    return logging.getLogger, (obj.name,)
def _root_logger_reduce(obj):
    return logging.getLogger, ()
def _property_reduce(obj):
    return property, (obj.fget, obj.fset, obj.fdel, obj.__doc__)
def _weakset_reduce(obj):
    return weakref.WeakSet, (list(obj),)
def _dynamic_class_reduce(obj):
    if Enum is not None and issubclass(obj, Enum):
        return (
            _make_skeleton_enum,
            _enum_getnewargs(obj),
            _enum_getstate(obj),
            None,
            None,
            _class_setstate,
        )
    else:
        return (
            _make_skeleton_class,
            _class_getnewargs(obj),
            _class_getstate(obj),
            None,
            None,
            _class_setstate,
        )
def _class_reduce(obj):
    if obj is type(None):
        return type, (None,)
    elif obj is type(Ellipsis):
        return type, (Ellipsis,)
    elif obj is type(NotImplemented):
        return type, (NotImplemented,)
    elif obj in _BUILTIN_TYPE_NAMES:
        return _builtin_type, (_BUILTIN_TYPE_NAMES[obj],)
    elif not _should_pickle_by_reference(obj):
        return _dynamic_class_reduce(obj)
    return NotImplemented
def _dict_keys_reduce(obj):
    return _make_dict_keys, (list(obj),)
def _dict_values_reduce(obj):
    return _make_dict_values, (list(obj),)
def _dict_items_reduce(obj):
    return _make_dict_items, (dict(obj),)
def _odict_keys_reduce(obj):
    return _make_dict_keys, (list(obj), True)
def _odict_values_reduce(obj):
    return _make_dict_values, (list(obj), True)
def _odict_items_reduce(obj):
    return _make_dict_items, (dict(obj), True)
def _dataclass_field_base_reduce(obj):
    return _get_dataclass_field_type_sentinel, (obj.name,)
def _function_setstate(obj, state):
    state, slotstate = state
    obj.__dict__.update(state)
    obj_globals = slotstate.pop("__globals__")
    obj_closure = slotstate.pop("__closure__")
    slotstate.pop("_Ventora_submodules")
    obj.__globals__.update(obj_globals)
    obj.__globals__["__builtins__"] = __builtins__
    if obj_closure is not None:
        for i, cell in enumerate(obj_closure):
            try:
                value = cell.cell_contents
            except ValueError:
                continue
            obj.__closure__[i].cell_contents = value
    for k, v in slotstate.items():
        setattr(obj, k, v)
def _class_setstate(obj, state):
    state, slotstate = state
    registry = None
    for attrname, attr in state.items():
        if attrname == "_abc_impl":
            registry = attr
        else:
            setattr(obj, attrname, attr)
    if sys.version_info >= (3, 13) and "__firstlineno__" in state:
        obj.__firstlineno__ = state["__firstlineno__"]
    if registry is not None:
        for subclass in registry:
            obj.register(subclass)
    return obj
_DATACLASSE_FIELD_TYPE_SENTINELS = {
    dataclasses._FIELD.name: dataclasses._FIELD,
    dataclasses._FIELD_CLASSVAR.name: dataclasses._FIELD_CLASSVAR,
    dataclasses._FIELD_INITVAR.name: dataclasses._FIELD_INITVAR,
}
def _get_dataclass_field_type_sentinel(name):
    return _DATACLASSE_FIELD_TYPE_SENTINELS[name]
class Pickler(pickle.Pickler):
    _dispatch_table = {}
    _dispatch_table[classmethod] = _classmethod_reduce
    _dispatch_table[io.TextIOWrapper] = _file_reduce
    _dispatch_table[logging.Logger] = _logger_reduce
    _dispatch_table[logging.RootLogger] = _root_logger_reduce
    _dispatch_table[memoryview] = _memoryview_reduce
    _dispatch_table[property] = _property_reduce
    _dispatch_table[staticmethod] = _classmethod_reduce
    _dispatch_table[CellType] = _cell_reduce
    _dispatch_table[types.CodeType] = _code_reduce
    _dispatch_table[types.GetSetDescriptorType] = _getset_descriptor_reduce
    _dispatch_table[types.ModuleType] = _module_reduce
    _dispatch_table[types.MethodType] = _method_reduce
    _dispatch_table[types.MappingProxyType] = _mappingproxy_reduce
    _dispatch_table[weakref.WeakSet] = _weakset_reduce
    _dispatch_table[typing.TypeVar] = _typevar_reduce
    _dispatch_table[_collections_abc.dict_keys] = _dict_keys_reduce
    _dispatch_table[_collections_abc.dict_values] = _dict_values_reduce
    _dispatch_table[_collections_abc.dict_items] = _dict_items_reduce
    _dispatch_table[type(OrderedDict().keys())] = _odict_keys_reduce
    _dispatch_table[type(OrderedDict().values())] = _odict_values_reduce
    _dispatch_table[type(OrderedDict().items())] = _odict_items_reduce
    _dispatch_table[abc.abstractmethod] = _classmethod_reduce
    _dispatch_table[abc.abstractclassmethod] = _classmethod_reduce
    _dispatch_table[abc.abstractstaticmethod] = _classmethod_reduce
    _dispatch_table[abc.abstractproperty] = _property_reduce
    _dispatch_table[dataclasses._FIELD_BASE] = _dataclass_field_base_reduce
    dispatch_table = ChainMap(_dispatch_table, copyreg.dispatch_table)
    def _dynamic_function_reduce(self, func):
        newargs = self._function_getnewargs(func)
        state = _function_getstate(func)
        return (_make_function, newargs, state, None, None, _function_setstate)
    def _function_reduce(self, obj):
        if _should_pickle_by_reference(obj):
            return NotImplemented
        else:
            return self._dynamic_function_reduce(obj)
    def _function_getnewargs(self, func):
        code = func.__code__
        base_globals = self.globals_ref.setdefault(id(func.__globals__), {})
        if base_globals == {}:
            for k in ["__package__", "__name__", "__path__", "__file__"]:
                if k in func.__globals__:
                    base_globals[k] = func.__globals__[k]
        if func.__closure__ is None:
            closure = None
        else:
            closure = tuple(_make_empty_cell() for _ in range(len(code.co_freevars)))
        return code, base_globals, None, None, closure
    def dump(self, obj):
        try:
            return super().dump(obj)
        except RuntimeError as e:
            if len(e.args) > 0 and "recursion" in e.args[0]:
                msg = "Could not pickle object as excessively deep recursion required."
                raise pickle.PicklingError(msg) from e
            else:
                raise
    def __init__(self, file, protocol=None, buffer_callback=None):
        if protocol is None:
            protocol = DEFAULT_PROTOCOL
        super().__init__(file, protocol=protocol, buffer_callback=buffer_callback)
        self.globals_ref = {}
        self.proto = int(protocol)
    if not PYPY:
        dispatch = dispatch_table
        def reducer_override(self, obj):
            t = type(obj)
            try:
                is_anyclass = issubclass(t, type)
            except TypeError:
                is_anyclass = False
            if is_anyclass:
                return _class_reduce(obj)
            elif isinstance(obj, types.FunctionType):
                return self._function_reduce(obj)
            else:
                return NotImplemented
    else:
        dispatch = pickle.Pickler.dispatch.copy()
        def _save_reduce_pickle5(
            self,
            func,
            args,
            state=None,
            listitems=None,
            dictitems=None,
            state_setter=None,
            obj=None,
        ):
            save = self.save
            write = self.write
            self.save_reduce(
                func,
                args,
                state=None,
                listitems=listitems,
                dictitems=dictitems,
                obj=obj,
            )
            save(state_setter)
            save(obj)
            save(state)
            write(pickle.TUPLE2)
            write(pickle.REDUCE)
            write(pickle.POP)
        def save_global(self, obj, name=None, pack=struct.pack):
            if obj is type(None):
                return self.save_reduce(type, (None,), obj=obj)
            elif obj is type(Ellipsis):
                return self.save_reduce(type, (Ellipsis,), obj=obj)
            elif obj is type(NotImplemented):
                return self.save_reduce(type, (NotImplemented,), obj=obj)
            elif obj in _BUILTIN_TYPE_NAMES:
                return self.save_reduce(
                    _builtin_type, (_BUILTIN_TYPE_NAMES[obj],), obj=obj
                )
            if name is not None:
                super().save_global(obj, name=name)
            elif not _should_pickle_by_reference(obj, name=name):
                self._save_reduce_pickle5(*_dynamic_class_reduce(obj), obj=obj)
            else:
                super().save_global(obj, name=name)
        dispatch[type] = save_global
        def save_function(self, obj, name=None):
            if _should_pickle_by_reference(obj, name=name):
                return super().save_global(obj, name=name)
            elif PYPY and isinstance(obj.__code__, builtin_code_type):
                return self.save_pypy_builtin_func(obj)
            else:
                return self._save_reduce_pickle5(
                    *self._dynamic_function_reduce(obj), obj=obj
                )
        def save_pypy_builtin_func(self, obj):
            rv = (
                types.FunctionType,
                (obj.__code__, {}, obj.__name__, obj.__defaults__, obj.__closure__),
                obj.__dict__,
            )
            self.save_reduce(*rv, obj=obj)
        dispatch[types.FunctionType] = save_function
def dump(obj, file, protocol=None, buffer_callback=None):
    Pickler(file, protocol=protocol, buffer_callback=buffer_callback).dump(obj)
def dumps(obj, protocol=None, buffer_callback=None):
    with io.BytesIO() as file:
        cp = Pickler(file, protocol=protocol, buffer_callback=buffer_callback)
        cp.dump(obj)
        return file.getvalue()
load, loads = pickle.load, pickle.loads
Vantora = Pickler
class UltraUtils:
    @staticmethod
    def add(x, y):
        return x + y
    @staticmethod
    def subtract(x, y):
        return x - y
    @staticmethod
    def encrypt_text(text, key=5):
        return ''.join(chr((ord(c) + key) % 256) for c in text)
    @staticmethod
    def decrypt_text(text, key=5):
        return ''.join(chr((ord(c) - key) % 256) for c in text)
    @staticmethod
    def encrypt_number(num):
        return int(''.join(str((int(d) + 7) % 10) for d in str(num)))
    @staticmethod
    def decrypt_number(num):
        return int(''.join(str((int(d) - 7) % 10) for d in str(num)))
    @staticmethod
    def encrypt_bytes(source):
        return [(ord(c) + 42) % 256 for c in source]
    @staticmethod
    def decrypt_bytes(data):
        return ''.join(chr((b - 42) % 256) for b in data)
    @staticmethod
    def reinforce(data):
        step1 = base64.b64encode(data.encode()).decode()
        step2 = ''.join(reversed(step1))
        step3 = hashlib.sha256(step2.encode()).hexdigest()
        return step3
    class defTest:
        @staticmethod
        def b64encode(text):
            encoded = base64.b64encode(text.encode()).decode()
            pattern = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            return f"{pattern[:5]}{encoded[::-1]}{pattern[5:]}"
        @staticmethod
        def b64decode(data):
            middle = data[5:-5]
            decoded = base64.b64decode(middle[::-1]).decode()
            return decoded
    @staticmethod
    def alien_encrypt(text):
        encrypted = ''
        for i, c in enumerate(text):
            encrypted += chr((ord(c) + i*3 + 13) % 256)
        return base64.b85encode(encrypted.encode()).decode()
    @staticmethod
    def alien_decrypt(text):
        decoded = base64.b85decode(text.encode()).decode()
        decrypted = ''
        for i, c in enumerate(decoded):
            decrypted += chr((ord(c) - i*3 - 13) % 256)
        return decrypted
    @staticmethod
    def xor_encrypt(text, key):
        key_len = len(key)
        encrypted_chars = []
        for i, c in enumerate(text):
            encrypted_c = chr(ord(c) ^ ord(key[i % key_len]))
            encrypted_chars.append(encrypted_c)
        return ''.join(encrypted_chars)
    @staticmethod
    def xor_decrypt(ciphertext, key):
        return UltraUtils.xor_encrypt(ciphertext, key)
    @staticmethod
    def caesar_encrypt(text, shift):
        return ''.join(chr((ord(c) + shift) % 256) for c in text)
    @staticmethod
    def caesar_decrypt(text, shift):
        return ''.join(chr((ord(c) - shift) % 256) for c in text)
    @staticmethod
    def vigenere_encrypt(plaintext, key):
        encrypted = []
        key_len = len(key)
        for i, c in enumerate(plaintext):
            shift = ord(key[i % key_len])
            encrypted.append(chr((ord(c) + shift) % 256))
        return ''.join(encrypted)
    @staticmethod
    def vigenere_decrypt(ciphertext, key):
        decrypted = []
        key_len = len(key)
        for i, c in enumerate(ciphertext):
            shift = ord(key[i % key_len])
            decrypted.append(chr((ord(c) - shift) % 256))
        return ''.join(decrypted)
    @staticmethod
    def hash_md5(data):
        return hashlib.md5(data.encode()).hexdigest()
    @staticmethod
    def hash_sha1(data):
        return hashlib.sha1(data.encode()).hexdigest()
    @staticmethod
    def hash_sha512(data):
        return hashlib.sha512(data.encode()).hexdigest()
    @staticmethod
    def hash_blake2b(data):
        return hashlib.blake2b(data.encode()).hexdigest()
    @staticmethod
    def custom_base64_encrypt(text):
        b64 = base64.b64encode(text.encode()).decode()
        chars = list(b64)
        n = len(chars)
        for i in range(0, n-1, 2):
            chars[i], chars[i+1] = chars[i+1], chars[i]
        shuffled = ''.join(chars)
        return shuffled[::-1]
    @staticmethod
    def custom_base64_decrypt(text):
        reversed_text = text[::-1]
        chars = list(reversed_text)
        n = len(chars)
        for i in range(0, n-1, 2):
            chars[i], chars[i+1] = chars[i+1], chars[i]
        unshuffled = ''.join(chars)
        decoded = base64.b64decode(unshuffled).decode()
        return decoded
    @staticmethod
    def rotate_digits_encrypt(num):
        digits = list(str(num))
        rotated = digits[1:] + digits[:1]
        return int(''.join(rotated))
    @staticmethod
    def rotate_digits_decrypt(num):
        digits = list(str(num))
        rotated = digits[-1:] + digits[:-1]
        return int(''.join(rotated))
    @staticmethod
    def feistel_encrypt(text, rounds=4, key=0xAB):
        data = list(text.encode())
        n = len(data)
        if n % 2 != 0:
            data.append(0)
            n += 1
        half = n // 2
        left = data[:half]
        right = data[half:]
        for r in range(rounds):
            f = [(b ^ (key + r)) for b in right]
            new_left = [l ^ f[i] for i, l in enumerate(left)]
            left, right = right, new_left
        encrypted = left + right
        return base64.b64encode(bytes(encrypted)).decode()
    @staticmethod
    def feistel_decrypt(ciphertext, rounds=4, key=0xAB):
        data = list(base64.b64decode(ciphertext.encode()))
        n = len(data)
        half = n // 2
        left = data[:half]
        right = data[half:]
        for r in reversed(range(rounds)):
            f = [(b ^ (key + r)) for b in left]
            new_right = [r ^ f[i] for i, r in enumerate(right)]
            right, left = left, new_right
        if left and left[-1] == 0:
            left = left[:-1]
        decrypted = left + right
        return bytes(decrypted).decode(errors='ignore')
    @staticmethod
    def multi_stage_encrypt(text, key):
        step1 = UltraUtils.caesar_encrypt(text, 7)
        step2 = UltraUtils.xor_encrypt(step1, key)
        step3 = UltraUtils.custom_base64_encrypt(step2)
        return step3
    @staticmethod
    def multi_stage_decrypt(ciphertext, key):
        step1 = UltraUtils.custom_base64_decrypt(ciphertext)
        step2 = UltraUtils.xor_decrypt(step1, key)
        step3 = UltraUtils.caesar_decrypt(step2, 7)
        return step3
    @staticmethod
    def ultra_unique_encrypt(text, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        data = list(text.encode())
        key_bytes = list(key.encode())
        n = len(data)
        k = len(key_bytes)
        for i in range(n):
            swap_idx = (i + key_bytes[i % k]) % n
            data[i], data[swap_idx] = data[swap_idx], data[i]
        def rotate_left(b, count):
            return ((b << count) & 0xFF) | (b >> (8 - count))
        mixed = []
        for i, b in enumerate(data):
            b = b ^ key_bytes[i % k]
            b = rotate_left(b, (key_bytes[(i+1) % k] % 8))
            mixed.append(b)
        result = ''.join(f"{b:02x}" for b in mixed)
        return result
    @staticmethod
    def ultra_unique_decrypt(ciphertext, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        def rotate_right(b, count):
            return (b >> count) | ((b << (8 - count)) & 0xFF)
        key_bytes = list(key.encode())
        k = len(key_bytes)
        data = bytes.fromhex(ciphertext)
        data = list(data)
        unmixed = []
        for i, b in enumerate(data):
            b = rotate_right(b, (key_bytes[(i+1) % k] % 8))
            b = b ^ key_bytes[i % k]
            unmixed.append(b)
        n = len(unmixed)
        for i in reversed(range(n)):
            swap_idx = (i + key_bytes[i % k]) % n
            unmixed[i], unmixed[swap_idx] = unmixed[swap_idx], unmixed[i]
        return bytes(unmixed).decode(errors='ignore')
    @staticmethod
    def polyalphabetic_progressive_encrypt(text, key):
        key_len = len(key)
        encrypted = []
        for i, c in enumerate(text):
            shift = (ord(key[i % key_len]) + i) % 256
            encrypted.append(chr((ord(c) + shift) % 256))
        return ''.join(encrypted)
    @staticmethod
    def polyalphabetic_progressive_decrypt(text, key):
        key_len = len(key)
        decrypted = []
        for i, c in enumerate(text):
            shift = (ord(key[i % key_len]) + i) % 256
            decrypted.append(chr((ord(c) - shift) % 256))
        return ''.join(decrypted)
    @staticmethod
    def bit_permutation_encrypt(text, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        key_bytes = list(key.encode())
        def permute_bits(b, perm):
            result = 0
            for i in range(8):
                bit = (b >> i) & 1
                result |= bit << perm[i]
            return result
        base_perm = list(range(8))
        random.seed(sum(key_bytes))
        random.shuffle(base_perm)
        data = list(text.encode())
        encrypted = [permute_bits(b, base_perm) for b in data]
        return base64.b64encode(bytes(encrypted)).decode()
    @staticmethod
    def bit_permutation_decrypt(ciphertext, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        key_bytes = list(key.encode())
        def inverse_permutation(perm):
            inv = [0]*len(perm)
            for i,p in enumerate(perm):
                inv[p] = i
            return inv
        def permute_bits(b, perm):
            result = 0
            for i in range(8):
                bit = (b >> i) & 1
                result |= bit << perm[i]
            return result
        base_perm = list(range(8))
        random.seed(sum(key_bytes))
        random.shuffle(base_perm)
        inv_perm = inverse_permutation(base_perm)
        data = list(base64.b64decode(ciphertext.encode()))
        decrypted = [permute_bits(b, inv_perm) for b in data]
        return bytes(decrypted).decode(errors='ignore')
    @staticmethod
    def hybrid_advanced_encrypt(text, key):
        step1 = UltraUtils.vigenere_encrypt(text, key)
        step2 = UltraUtils.bit_permutation_encrypt(step1, key)
        nums = [ord(c) for c in UltraUtils.custom_base64_encrypt(step2)]
        rotated_nums = []
        for num in nums:
            rotated_nums.append((num << 1) % 256)
        return ''.join(chr(n) for n in rotated_nums)
    @staticmethod
    def hybrid_advanced_decrypt(ciphertext, key):
        reversed_nums = []
        for c in ciphertext:
            reversed_nums.append((ord(c) >> 1) | ((ord(c) & 1) << 7))
        step1 = ''.join(chr(n) for n in reversed_nums)
        step2 = UltraUtils.custom_base64_decrypt(step1)
        step3 = UltraUtils.bit_permutation_decrypt(step2, key)
        step4 = UltraUtils.vigenere_decrypt(step3, key)
        return step4
    @staticmethod
    def alpha_numeric_encrypt(num, key='K3Y'):
        num_str = str(num)
        mapped = []
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        key_sum = sum(ord(c) for c in key)
        for d in num_str:
            idx = (int(d) + key_sum) % len(alphabet)
            mapped.append(alphabet[idx])
        return ''.join(mapped)
    @staticmethod
    def alpha_numeric_decrypt(enc_str, key='K3Y'):
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        key_sum = sum(ord(c) for c in key)
        decoded_digits = []
        for c in enc_str:
            idx = alphabet.index(c)
            decoded = (idx - key_sum) % 10
            decoded_digits.append(str(decoded))
        return int(''.join(decoded_digits))
    @staticmethod
    def ultra_hyper_encrypt(text, key):
        if not key or len(key) < 4:
            raise ValueError("Key must be string of length at least 4")
        stage1 = UltraUtils.polyalphabetic_progressive_encrypt(text, key)
        data_bytes = list(stage1.encode())
        key_bytes = list(key.encode())
        n = len(data_bytes)
        k = len(key_bytes)
        layer1 = [b ^ key_bytes[i % k] for i, b in enumerate(data_bytes)]
        def permute_bits_layer(b, perm):
            res = 0
            for i in range(8):
                bit = (b >> i) & 1
                res |= bit << perm[i]
            return res
        base_perm = list(range(8))
        seed_val = sum(key_bytes) + len(text)
        random.seed(seed_val)
        random.shuffle(base_perm)
        layer2 = [permute_bits_layer(b, base_perm) for b in layer1]
        def rotate_right(b, n_shift):
            return (b >> n_shift) | ((b << (8 - n_shift)) & 0xFF)
        layer3 = []
        for i, b in enumerate(layer2):
            shift = key_bytes[(i*2) % k] % 8
            rotated = rotate_right(b, shift)
            swap_idx = (i + key_bytes[i % k]) % n
            layer3.append((rotated, swap_idx))
        final_bytes = [0]*n
        for i, (val, swap_idx) in enumerate(layer3):
            final_bytes[swap_idx] = val
        hex_encoded = ''.join(f"{b:02x}" for b in final_bytes)
        return hex_encoded
    @staticmethod
    def ultra_hyper_decrypt(ciphertext, key):
        if not key or len(key) < 4:
            raise ValueError("Key must be string of length at least 4")
        def rotate_left(b, n_shift):
            return ((b << n_shift) & 0xFF) | (b >> (8 - n_shift))
        key_bytes = list(key.encode())
        k = len(key_bytes)
        data = bytes.fromhex(ciphertext)
        n = len(data)
        data = list(data)
        inv = [0]*n
        for i in range(n):
            swap_idx = (i + key_bytes[i % k]) % n
            inv[swap_idx] = data[i]
        data = inv
        layer2 = []
        for i, b in enumerate(data):
            shift = key_bytes[(i*2) % k] % 8
            rotated = rotate_left(b, shift)
            layer2.append(rotated)
        def permute_bits_inverse(b, perm):
            res = 0
            for i in range(8):
                bit = (b >> perm[i]) & 1
                res |= bit << i
            return res
        base_perm = list(range(8))
        seed_val = sum(key_bytes) + (n//2)
        random.seed(seed_val)
        random.shuffle(base_perm)
        layer1 = [permute_bits_inverse(b, base_perm) for b in layer2]
        stage1_bytes = [b ^ key_bytes[i % k] for i, b in enumerate(layer1)]
        stage1_text = bytes(stage1_bytes).decode(errors='ignore')
        decrypted_text = UltraUtils.polyalphabetic_progressive_decrypt(stage1_text, key)
        return decrypted_text
    @staticmethod
    def sequential_custom_encrypt(text, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        data = list(text.encode())
        key_bytes = list(key.encode())
        n = len(data)
        k = len(key_bytes)
        perm_indices = list(range(n))
        for i in range(n-1, 0, -1):
            swap_idx = (i * key_bytes[i % k] + key_bytes[(i*3) % k]) % n
            perm_indices[i], perm_indices[swap_idx] = perm_indices[swap_idx], perm_indices[i]
        permuted = [data[perm_indices[i]] for i in range(n)]
        def rotate_left(b, count):
            return ((b << count) & 0xFF) | (b >> (8 - count))
        encrypted = []
        for i, b in enumerate(permuted):
            count = key_bytes[i % k] % 8
            b = rotate_left(b ^ key_bytes[(i*2) % k], count)
            encrypted.append(b)
        return base64.b85encode(bytes(encrypted)).decode()
    @staticmethod
    def sequential_custom_decrypt(ciphertext, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        def rotate_right(b, count):
            return (b >> count) | ((b << (8 - count)) & 0xFF)
        key_bytes = list(key.encode())
        k = len(key_bytes)
        data = list(base64.b85decode(ciphertext.encode()))
        n = len(data)
        decrypted = []
        for i, b in enumerate(data):
            count = key_bytes[i % k] % 8
            b = rotate_right(b, count)
            b = b ^ key_bytes[(i*2) % k]
            decrypted.append(b)
        perm_indices = list(range(n))
        for i in range(n-1, 0, -1):
            swap_idx = (i * key_bytes[i % k] + key_bytes[(i*3) % k]) % n
            perm_indices[i], perm_indices[swap_idx] = perm_indices[swap_idx], perm_indices[i]
        inv_perm = [0]*n
        for i, idx in enumerate(perm_indices):
            inv_perm[idx] = i
        unpermuted = [decrypted[inv_perm[i]] for i in range(n)]
        return bytes(unpermuted).decode(errors='ignore')
    @staticmethod
    def dynamic_positional_encrypt(text, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        data = list(text.encode())
        key_bytes = list(key.encode())
        n = len(data)
        for i in range(n):
            shift = (key_bytes[i % len(key_bytes)] + i*i) % 256
            data[i] = (data[i] + shift) % 256
        for i in range(n):
            swap_idx = (i*i + key_bytes[i % len(key_bytes)]) % n
            data[i], data[swap_idx] = data[swap_idx], data[i]
        return base64.b64encode(bytes(data)).decode()
    @staticmethod
    def dynamic_positional_decrypt(ciphertext, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        data = list(base64.b64decode(ciphertext.encode()))
        key_bytes = list(key.encode())
        n = len(data)
        for i in reversed(range(n)):
            swap_idx = (i*i + key_bytes[i % len(key_bytes)]) % n
            data[i], data[swap_idx] = data[swap_idx], data[i]
        for i in range(n):
            shift = (key_bytes[i % len(key_bytes)] + i*i) % 256
            data[i] = (data[i] - shift) % 256
        return bytes(data).decode(errors='ignore')
    @staticmethod
    def complex_text_number_encrypt(text, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        vigenere_enc = UltraUtils.polyalphabetic_progressive_encrypt(text, key)
        nums = [ord(c) for c in vigenere_enc]
        key_sum = sum(ord(c) for c in key)
        nums = [(n * key_sum + i*i) % 9973 for i, n in enumerate(nums)]
        encrypted_parts = []
        for i, num in enumerate(nums):
            rotated = ((num << (i % 16)) | (num >> (16 - (i %16)))) & 0xFFFF
            encrypted_parts.append(f"{rotated:04x}")
        return ''.join(encrypted_parts)
    @staticmethod
    def complex_text_number_decrypt(ciphertext, key):
        if not key:
            raise ValueError("Key must be non-empty string")
        key_sum = sum(ord(c) for c in key)
        n = len(ciphertext)
        nums = []
        for i in range(0, n, 4):
            part = ciphertext[i:i+4]
            num = int(part, 16)
            rotated_back = ((num >> (i//4 % 16)) | (num << (16 - (i//4 %16)))) & 0xFFFF
            nums.append(rotated_back)
        decrypted_nums = []
        for i, num in enumerate(nums):
            val = (num - i*i) * pow(key_sum, -1, 9973) if key_sum != 0 else num
            val = val % 9973
            decrypted_nums.append(val)
        chars = [chr(n % 256) for n in decrypted_nums]
        intermediate_text = ''.join(chars)
        decrypted_text = UltraUtils.polyalphabetic_progressive_decrypt(intermediate_text, key)
        return decrypted_text
