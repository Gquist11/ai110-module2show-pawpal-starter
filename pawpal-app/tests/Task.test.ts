import { Task } from '../src/classes/Task';

describe('Task Class', () => {
    let task: Task;

    beforeEach(() => {
        task = new Task('Walk the dog', 30, 'high', false);
    });

    test('should create a Task instance with correct properties', () => {
        expect(task.taskName).toBe('Walk the dog');
        expect(task.duration).toBe(30);
        expect(task.urgency).toBe('high');
        expect(task.isRecurring).toBe(false);
    });

    test('getTaskDetails should return correct task information', () => {
        const details = task.getTaskDetails();
        expect(details).toEqual({
            taskName: 'Walk the dog',
            duration: 30,
            urgency: 'high',
            isRecurring: false,
        });
    });

    test('markAsComplete should update task status', () => {
        task.markAsComplete();
        expect(task.isComplete).toBe(true);
    });
});