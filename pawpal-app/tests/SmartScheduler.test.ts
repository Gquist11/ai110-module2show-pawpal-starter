import { SmartScheduler } from '../src/classes/SmartScheduler';
import { Profile } from '../src/classes/Profile';
import { Task } from '../src/classes/Task';

describe('SmartScheduler', () => {
    let scheduler: SmartScheduler;
    let profile: Profile;
    let tasks: Task[];

    beforeEach(() => {
        scheduler = new SmartScheduler();
        profile = new Profile('John Doe', 'Buddy', 'Dog', 5);
        tasks = [
            new Task('Walk the dog', 30, 'high', false),
            new Task('Feed the dog', 15, 'medium', true),
            new Task('Groom the dog', 45, 'low', false)
        ];
    });

    test('should schedule tasks based on profile and tasks', () => {
        const schedule = scheduler.scheduleTasks(profile, tasks);
        expect(schedule).toBeDefined();
        expect(schedule.length).toBeGreaterThan(0);
    });

    test('should explain scheduling decisions', () => {
        const explanation = scheduler.explainSchedule(profile, tasks);
        expect(explanation).toContain('Scheduled tasks for');
    });
});