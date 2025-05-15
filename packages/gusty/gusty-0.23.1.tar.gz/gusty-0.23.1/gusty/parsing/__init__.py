import os
from copy import copy
from functools import partial
from absql.utils import get_function_arg_names
from gusty.parsing.loaders import generate_loader
from gusty.parsing.parsers import parse_generic, parse_py, parse_ipynb, parse_sql
from gusty.utils import nested_update

default_parsers = {
    ".yml": parse_generic,
    ".yaml": parse_generic,
    ".Rmd": parse_generic,
    ".py": parse_py,
    ".ipynb": parse_ipynb,
    ".sql": parse_sql,
}


def parse(
    file_path,
    parse_dict=default_parsers,
    loader=None,
    runner=None,
    render_on_create=False,
):
    """
    Reading in yaml specs / frontmatter.
    """

    if loader is None:
        loader = generate_loader()

    path, extension = os.path.splitext(file_path)

    parser = parse_dict[extension]
    if "loader" in get_function_arg_names(parser):
        parser = partial(parser, loader=loader)
    if "runner" in get_function_arg_names(parser):
        parser = partial(parser, runner=runner)
    if "render_on_create" in get_function_arg_names(parser):
        parser = partial(parser, render_on_create=render_on_create)

    yaml_file = parser(file_path)

    assert "operator" in yaml_file, "No operator specified in yaml spec " + file_path

    # gusty always supplies a task_id and a file_path in a spec
    yaml_file["task_id"] = (
        os.path.splitext(os.path.basename(file_path))[0].lower().strip()
    )
    assert (
        yaml_file["task_id"] != "all"
    ), "Task name 'all' is not allowed. Please change your task name."

    yaml_file["file_path"] = file_path

    # gusty will also attach the absql_runner
    yaml_file["absql_runner"] = copy(runner)

    # Check dependencies
    if "dependencies" in yaml_file.keys():
        assert isinstance(
            yaml_file["dependencies"], list
        ), "dependencies needs to be a list of strings in {file_path}".format(
            file_path=file_path
        )
        assert all(
            [isinstance(dep, str) for dep in yaml_file["dependencies"]]
        ), "dependencies needs to be a list of strings in {file_path}".format(
            file_path=file_path
        )

    # Handle multi_task
    multi_task_spec = yaml_file.get("multi_task_spec") or {}

    python_callable = yaml_file.get("python_callable")
    python_callable_partials = yaml_file.get("python_callable_partials")
    if python_callable and python_callable_partials:
        for task_id, partial_kwargs in python_callable_partials.items():
            callable_update = {
                "python_callable": partial(python_callable, **partial_kwargs)
            }
            if task_id in multi_task_spec.keys():
                multi_task_spec[task_id].update(callable_update)
            else:
                multi_task_spec.update({task_id: callable_update})

    multi_specs = []
    if len(multi_task_spec) > 0:
        for task_id, spec in multi_task_spec.items():
            base_spec = yaml_file.copy()
            base_spec["task_id"] = task_id
            base_spec = nested_update(base_spec, spec)
            multi_specs.append(base_spec)

    if len(multi_specs) > 0:
        return multi_specs

    return yaml_file
