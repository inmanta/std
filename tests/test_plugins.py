def test_select_attr(project):
    project.compile(
        """
    entity Container:
        string field
    end

    implement Container using std::none

    entity Out:
        string[] fields
    end
    implement Out using std::none

    entity Collector:

    end
    implement Collector using std::none

    Collector.containers [0:] -- Container

    c = Collector()
    c.containers += Container(field="A")
    c.containers += Container(field="B")
    c.containers += Container(field="C")

    Out(fields = std::select(c.containers,"field"))

    """
    )

    assert sorted(project.get_instances("__config__::Out")[0].fields) == ["A", "B", "C"]
