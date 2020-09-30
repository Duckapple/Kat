import { ParseCallback, Argv } from 'yargs';

export type CommandResult<T> = {
    output: string;
    argv: T;
};

/* istanbul ignore next */
export async function parse<T>(parser: Argv<T>, input: string): Promise<CommandResult<T>> {
    return await new Promise((res, rej) => {
        const onParse: ParseCallback<T> = (err, argv, output) => {
            if (err) {
                rej(err);
            } else {
                res({ output, argv });
            }
        };
        parser.parse(input, onParse);
    });
}
