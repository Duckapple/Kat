import { mocked } from 'ts-jest/utils';
import render, { pe } from '../handler';
import UserError from '../UserError';

describe('render', () => {
    let output: string;
    jest.spyOn(console, 'error').mockImplementation((...args) => {
        args.forEach((arg) => (output += arg));
    });

    beforeEach(() => {
        output = '';
    });

    it('simply prints UserError to stderr', () => {
        const err = new UserError('Test error');
        render(err);
        expect(output).toEqual(err.message);
    });

    it('prints formatted error to stderr', () => {
        const err = new Error('Test error');
        render(err);
        expect(output).toEqual(pe.render(err));
    });
});
