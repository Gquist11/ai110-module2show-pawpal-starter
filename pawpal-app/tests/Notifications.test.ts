import { Notifications } from '../src/classes/Notifications';
import { Task } from '../src/classes/Task';

describe('Notifications', () => {
    let notifications: Notifications;

    beforeEach(() => {
        notifications = new Notifications();
    });

    test('should send a notification with the correct message', () => {
        const message = 'Time to walk your dog!';
        const spy = jest.spyOn(console, 'log');
        
        notifications.sendNotification(message);
        
        expect(spy).toHaveBeenCalledWith(message);
        spy.mockRestore();
    });

    test('should schedule a notification for a specific task', () => {
        const task = new Task('Walk the dog', 30, 'high', false);
        const spy = jest.spyOn(global, 'setTimeout');

        notifications.scheduleNotification(task);

        expect(spy).toHaveBeenCalled();
        spy.mockRestore();
    });
});