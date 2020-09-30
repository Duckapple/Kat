import { Arguments, CommandBuilder } from 'yargs';
import fetchProblem from '../actions/fetchProblem';
import makeBoilerplate from '../actions/makeBoilerplate';

export type GetArgs = {
    problemName: string;
};

export const command = 'get <problemName>';
export const describe = 'Downloads and prepares a boilerplate for a kattis problem';

export const builder: CommandBuilder<GetArgs, GetArgs> = (yargs) =>
    yargs.positional('problemName', {
        describe: 'The ID of the kattis problem',
        type: 'string',
        demandOption: true,
    });

export async function handler({ problemName }: Arguments<GetArgs>): Promise<void> {
    await fetchProblem(problemName);
    makeBoilerplate(problemName);
}
