from pawpal_system import Task, Pet


def test_task_completion():
    """Calling complete() on a Task should change completed to True."""
    task = Task(title="Morning walk", duration_minutes=30, priority="high")

    assert task.completed is False  # starts incomplete

    task.complete()

    assert task.completed is True


def test_task_addition_increases_count():
    """Adding a Task to a Pet should increase that pet's task count by one."""
    pet = Pet(name="Mochi", species="dog")

    assert len(pet.get_tasks()) == 0  # starts empty

    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))

    assert len(pet.get_tasks()) == 1
