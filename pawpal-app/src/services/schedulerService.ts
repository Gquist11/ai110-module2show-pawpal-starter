import { Profile } from '../classes/Profile';
import { Task } from '../classes/Task';
import { SmartScheduler } from '../classes/SmartScheduler';
import { Notifications } from '../classes/Notifications';
import { Schedule } from '../types';

export function createSchedule(profile: Profile, tasks: Task[]): Schedule[] {
    const scheduler = new SmartScheduler();
    return scheduler.scheduleTasks(profile, tasks);
}

export function notifyUser(notification: Notifications, message: string): void {
    notification.sendNotification(message);
}