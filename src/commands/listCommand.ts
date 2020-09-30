import { Arguments, CommandBuilder } from 'yargs';

export type ListArgs = {
    sort: 'easiest' | 'hardest';
    choises: ('unsolved' | 'solved' | 'untried' | 'tried')[];
};

export const command = 'list';
export const describe = 'Lists problems directly from Kattis according to some criteria.';

export const builder: CommandBuilder<ListArgs> = (yargs) =>
    yargs
        .option('sort', {
            choices: ['easiest', 'hardest'],
        })
        .option('filter', {
            array: true,
            choices: ['unsolved', 'solved', 'untried', 'tried'],
        });

export async function handler({ sort }: Arguments<ListArgs>): Promise<void> {
    console.log(sort);
}
