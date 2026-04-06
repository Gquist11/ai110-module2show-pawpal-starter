// src/index.ts
import { Profile } from './classes/Profile';
import { Task } from './classes/Task';
import { SmartScheduler } from './classes/SmartScheduler';
import { Notifications } from './classes/Notifications';

// Initialize the application
const initApp = () => {
    // Example profile and tasks
    const profile = new Profile('George', 'Buddy', 'Dog', 5);
    const tasks = [
        new Task('Walk Buddy', 30, 'High', false),
        new Task('Feed Buddy', 15, 'Medium', true)
    ];

    // Create an instance of SmartScheduler
    const scheduler = new SmartScheduler();
    const schedule = scheduler.scheduleTasks(profile, tasks);

    // Create an instance of Notifications
    const notifications = new Notifications();

    // Send notifications for scheduled tasks
    schedule.forEach(task => {
        notifications.scheduleNotification(task);
    });

    console.log('App initialized and notifications scheduled.');
};

// Start the application
initApp();