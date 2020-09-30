import yargs from 'yargs';
import render from '../errors/handler';

// https://github.com/yargs/yargs/blob/master/docs/advanced.md#building-configurable-cli-apps
export const parser = yargs
    .scriptName('kat')
    .demandCommand(1)
    .recommendCommands()
    .completion('completion', 'Generate auto-completion script for Bash/ZSH.')
    .fail((_, err) => {
        if (err) {
            render(err);
        } else {
            yargs.showHelp();
        }

        process.exit(1);
    });
