import { Profile } from '../src/classes/Profile';

describe('Profile Class', () => {
    let profile: Profile;

    beforeEach(() => {
        profile = new Profile('John Doe', 'Buddy', 'Dog', 5);
    });

    test('should create a profile with correct properties', () => {
        expect(profile.ownerName).toBe('John Doe');
        expect(profile.petName).toBe('Buddy');
        expect(profile.petType).toBe('Dog');
        expect(profile.petAge).toBe(5);
    });

    test('getProfileInfo should return correct profile details', () => {
        const expectedInfo = 'Owner: John Doe, Pet: Buddy, Type: Dog, Age: 5';
        expect(profile.getProfileInfo()).toBe(expectedInfo);
    });
});