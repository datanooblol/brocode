import importlib.util
from pathlib import Path
from brocode.data_specs.tool import Tool, Arg
from typing import Any

DTYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
}

def load_tool_schema(path:Path)->Tool:
    """create a tool schema based on the execution file
    Args:
        path (Path): a path to a python script
    Returns:
        Tool: abc
    """
    if not path.is_file():
        raise ValueError(f"{path} not found")

    filename = path.stem

    # 1. Build a module spec from the file path
    spec = importlib.util.spec_from_file_location(filename, path)

    # 2. Create an empty module object from that spec
    module = importlib.util.module_from_spec(spec)

    # 3. Actually run the file's top-level code, populating the module
    spec.loader.exec_module(module)

    parser = module.get_args()
    description = parser.description
    actions = parser._actions[1:]
    args = []
    for action in actions:
        args.append(
            Arg(
                name=action.dest,
                type=DTYPE_MAP[action.type],
                description=action.help,
                required=action.required
            )
        )
    return Tool(
        name=filename,
        description=description,
        args=args,
        path=path
    )

def to_args(args:dict)->list[Any]:
    if not args:
        return []
    args_list = []
    for k,v in args.items():
        args_list.extend([f"--{k}", v])
    return args_list