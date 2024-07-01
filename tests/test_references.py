
import os

def test_reference(project) -> None:
    """ Test the use of reference
    """
    project.compile("""
env_ref = std::EnvironmentReference(variable_name="USER")

file = std::ConfigFile(
    host=std::Host(name="test", os=std::linux),
    owner="bart",
    group="bart",
    path="/tmp/reference",
    content=env_ref.value
)
""")

    project.deploy_all().assert_all()


    with open("/tmp/reference", "r") as fd:
        assert fd.read() == os.getenv("USER")
