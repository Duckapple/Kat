import { baseUrl } from '../url';

describe('baseUrl', () => {
    it('returns base url', () => {
        expect(baseUrl()).toEqual('https://open.kattis.com');
    });
    it('can append a suffix', () => {
        expect(baseUrl('/foo')).toEqual('https://open.kattis.com/foo');
    });
});
