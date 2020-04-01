from inmanta.export import DynamicProxy


def test_mutable_string(project):
    model = """
    attr_a = std::MutableString()
    if true:
        attr_a.value = "a"
    else:
        attr_a.value = "b"
    end

    a = attr_a.value
    """

    project.compile(model)
    root = project._root_scope.get_child("__config__")
    a = root.lookup("a")
    assert a.value == "a"


def test_mutable_number(project):
    model = """
    attr_a = std::MutableNumber()
    if true:
        attr_a.value = 3
    else:
        attr_a.value = 4
    end

    a = attr_a.value
    """

    project.compile(model)
    root = project._root_scope.get_child("__config__")
    a = root.lookup("a")
    assert a.value == 3


def test_mutable_bool(project):
    model = """
    attr_a = std::MutableBool()
    if true:
        attr_a.value = null
    else:
        attr_a.value = true
    end

    a = attr_a.value
    """

    project.compile(model)
    root = project._root_scope.get_child("__config__")
    a = root.lookup("a")
    assert DynamicProxy.return_value(a.value) is None
