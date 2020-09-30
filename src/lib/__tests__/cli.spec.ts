import yargs from 'yargs';
import { mocked } from 'ts-jest/utils';
import render from '../../errors/handler';
import { onYargsFail } from '../cli';

jest.mock('../../errors/handler');

const mockedRender = mocked(render, true);

const _nop = (() => {
    /**/
}) as () => never;

describe('onYargsFail', () => {
    const mockExit = jest.spyOn(process, 'exit').mockImplementation(_nop);
    const mockedShowHelp = jest.spyOn(yargs, 'showHelp').mockImplementation(_nop);

    afterEach(() => {
        mockedRender.mockClear();
    });

    it('calls render and exists if an exception is passed', () => {
        const err = new Error('Test Error');
        onYargsFail(err);
        expect(mockedRender).toBeCalledWith(err);

        expect(mockExit).toBeCalledWith(1);
    });

    it('shows yargs help and exists if an exception is not passed', () => {
        onYargsFail(undefined);
        expect(mockedRender).not.toBeCalled();

        expect(mockedShowHelp).toBeCalled();
        expect(mockExit).toBeCalledWith(1);
    });
});
