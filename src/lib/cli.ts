import yargs from 'yargs';
import render from '../errors/handler';

export function onYargsFail(err: Error | undefined): void {
    if (err) {
        render(err);
    } else {
        yargs.showHelp();
    }

    process.exit(1);
}

// https://github.com/yargs/yargs/blob/master/docs/advanced.md#building-configurable-cli-apps
/* istanbul ignore next */
export const parser = yargs
    .scriptName('kat')
    .demandCommand(1)
    .recommendCommands()
    .completion('completion', 'Generate auto-completion script for Bash/ZSH.')
    .fail((_, err) => onYargsFail(err));
