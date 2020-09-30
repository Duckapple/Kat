import { CommandModule, ParseCallback } from 'yargs';
import { mocked } from 'ts-jest/utils';
import fetchProblem from '../../actions/fetchProblem';
import { parser } from '../../lib/cli';

import * as getCommand from '../getCommand';
import { GetArgs } from '../getCommand';
import { parse } from '../../test-utils/parse';
import makeBoilerplate from '../../actions/makeBoilerplate';

jest.mock('../../actions/fetchProblem');
jest.mock('../../actions/makeBoilerplate');

const mockedFetchProblem = mocked(fetchProblem, true);
const mockedMakeBoilerplate = mocked(makeBoilerplate, true);

describe('getCommand', () => {
    it('calls fetchProblem and makeBoilerplate', async () => {
        const cli = parser.command(getCommand as CommandModule<Record<string, unknown>, GetArgs>);

        await parse(cli, 'get twostones');

        expect(mockedFetchProblem).toBeCalledWith('twostones');
        expect(mockedMakeBoilerplate).toBeCalledWith('twostones');
    });
});
