import fs, { mkdirSync, existsSync } from 'fs';
import { resolve } from 'path';
import { cwd } from 'process';
import nock from 'nock';
import { mocked } from 'ts-jest/utils';

import { downloadAndExtractZip } from '../../lib/download';
import { baseUrl } from '../../lib/url';
import fetchProblem from '../fetchProblem';
import UserError from '../../errors/UserError';

jest.mock('fs', () => ({
    ...jest.requireActual<typeof fs>('fs'),
    existsSync: jest.fn(),
    mkdirSync: jest.fn(),
}));

jest.mock('../../lib/download.ts');

const mockedExistsSync = mocked(existsSync, true);
const mockedMkdirSync = mocked(mkdirSync, true);

describe('fetchProblem', () => {
    // Mock console.log to silence output
    jest.spyOn(console, 'log').mockImplementation(() => {
        /**/
    });

    it('creates directory and downloads zip file with sample files', async () => {
        nock(baseUrl()).get('/problems/twostones').reply(200, 'asdf');
        mockedExistsSync.mockReturnValue(false);

        await fetchProblem('twostones');

        expect(mockedMkdirSync).toBeCalledWith('twostones', { recursive: true });
        expect(downloadAndExtractZip).toBeCalledWith({
            url: baseUrl('/problems/twostones/file/statement/samples.zip'),
            path: resolve(cwd(), 'twostones', `test`),
        });
    });

    it('fails if problem has already been downloaded', async () => {
        mockedExistsSync.mockReturnValue(true);

        await expect(fetchProblem('twostones')).rejects.toThrow(
            new UserError("The problem 'twostones' already exists")
        );
    });

    it('fails if problem does not exist on kattis', async () => {
        mockedExistsSync.mockReturnValue(false);

        nock(baseUrl()).get('/problems/twostones').reply(404, 'asdf');

        await expect(fetchProblem('twostones')).rejects.toThrow(
            new UserError("⚠️ Problem 'twostones' does not exist!")
        );
    });
});
