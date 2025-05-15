import pytest
from gusty import create_dag
from gusty.building import GustyBuilder

###############
## FIXTURES ##
###############


@pytest.fixture(scope="session")
def with_metadata_dir():
    return "tests/dags/with_metadata"


@pytest.fixture(scope="session")
def builder(with_metadata_dir):
    def env_var(x):
        return x + x

    return GustyBuilder(
        with_metadata_dir,
        dag_constructors=[env_var],
        task_group_defaults={},
        wait_for_defaults={},
        latest_only=True,
        parse_hooks={},
    )


@pytest.fixture(scope="session")
def dag(with_metadata_dir):
    def simple_constructor(hello=True):
        if hello:
            return "hello"
        else:
            return "goodbye"

    def env_var(x):
        return x + x

    dag = create_dag(
        with_metadata_dir,
        default_args={"email": "default@gusty.com", "retries": 5},
        task_group_defaults={"prefix_group_id": True},
        wait_for_defaults={"poke_interval": 12},
        dag_constructors=[env_var, simple_constructor],
        extra_tags=["extra"],
        render_on_create=True,
    )
    return dag


###########
## TESTS ##
###########


def test_default_args_provided(dag):
    """
    create_dag default_args should be implemented on top of
    METADATA.yml-provided default_args when a default arg (e.g. retries)
    is not provided METADATA.yml but is provided by create_dag default_args
    """
    top_level_task = dag.task_dict["top_level_task"]
    assert top_level_task.__dict__["retries"] == 5
    pass


def test_default_args_overridden(dag):
    """
    create_dag default_args should be overridden by METADATA.yml-provided default_args
    when a default arg (e.g. retries) exists in both create_dag default_args and
    METADATA.yml default_args
    """
    top_level_task = dag.task_dict["top_level_task"]
    assert top_level_task.__dict__["email"] == "meta@gusty.com"
    pass


def test_latest_only_false(dag):
    assert "latest_only" not in dag.roots


def test_prefixes(dag):
    assert "prefixes.prefixes_check" in dag.task_dict.keys()


def test_suffixes(dag):
    assert "suffixes.check_suffixes" in dag.task_dict.keys()


def test_noffixes(dag):
    assert "plain_name" in dag.task_dict.keys()


def test_deeper(dag):
    # even though this is deep, it drops all tags when prefix is dropped
    # even though it still lives in the taskgroup deeper.first...
    # maybe an airflow bug?
    assert "first" in dag.task_dict.keys()
    assert "deeper.second.second_second" in dag.task_dict.keys()


def test_wait_for_defaults(dag):
    wait_for_tasks = [
        task
        for task_id, task in dag.task_dict.items()
        if task_id.startswith("wait_for_")
    ]

    wait_for_tasks_adjusted = [
        task.__dict__["poke_interval"] == 12 for task in wait_for_tasks
    ]

    assert all(wait_for_tasks_adjusted)


def test_metadata_wait_for_defaults(dag):
    wait_for_task = [
        task
        for task_id, task in dag.task_dict.items()
        if task_id.startswith("wait_for_")
    ][0]

    assert wait_for_task.__dict__["timeout"] == 1234


def test_prefixed_dependencies_work(dag):
    # if a user turns task group prefixes/suffixes on, gusty should proactively check
    # for prefixed/suffixed dependencies in addition to whatever is provided in a task's spec
    # e.g. in a task group "tg" with prefixes turned on, the dependency to look for is "tg_task",
    #      but the user only specified "task" in the depedencies block.
    assert (
        "prefixes.prefixes_check"
        in dag.task_dict["prefixes.prefixes_dep_check"].__dict__["upstream_task_ids"]
    )


def test_root_level_external_dependency(dag):
    root_dict = [dep.__dict__["task_id"] for dep in dag.roots]
    assert "wait_for_DAG_top_level_external" in root_dict
    assert len(root_dict) == 1


def test_root_dependency(dag):
    # The root_task_sensor task is not depended on by anything, nor does it depend on anything
    root_sensor_task = dag.task_dict["root_sensor_task"]
    assert len(root_sensor_task.__dict__["downstream_task_ids"]) > 0


def test_leaf_tasks(dag):
    assert len(dag.leaves) == 1
    leaf_task = dag.leaves[0].__dict__
    assert len(leaf_task["downstream_task_ids"]) == 0
    assert leaf_task["task_id"] == "final_task"


def test_absql_override(builder, dag):
    runner_func = builder.runner.__dict__["extra_context"]["env_var"]
    loader_results = dag.task_dict["final_task"].bash_command
    assert runner_func("hey") == "heyhey"
    assert loader_results == "finalfinal"


def test_metadata_renders(dag):
    assert dag.description == "For making the most important meal of the day."


def test_extra_tags(dag):
    tags = dag.__dict__["tags"]
    assert "delicious" in tags
    assert "nutritious" in tags
    assert "important" in tags
    assert "extra" in tags


def test_constructors(dag):
    assert dag.task_dict["sensor_task"].__dict__["email"] == "goodbye"
    assert dag.task_dict["sensor_task"].__dict__["owner"] == "hello"
    # Below is generated a default func available in absql
    assert dag.task_dict["sensor_task"].__dict__["doc"] == "default_absql_func"


def test_context_rendering_omits_sql(dag):
    sql_task = dag.task_dict["sql_task"]
    assert sql_task.__dict__["doc"] == "hello"
    assert (
        sql_task.__dict__["sql"] == "SELECT date FROM my_table WHERE date = {{ date }}"
    )


def test_context_rendering_py(dag):
    assert dag.task_dict["py_task"].__dict__["python_callable"]() == "hey"


def test_gusty_ignored_folder(dag):
    assert "ignored.ignored_ignored" not in dag.task_dict.keys()
