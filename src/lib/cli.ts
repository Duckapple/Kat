import yargs from 'yargs';
import render from '../errors/handler';

export const parser = yargs
    .scriptName('kat')
    .demandCommand(1)
    .recommendCommands()
    .completion()
    .fail((_, err) => {
        if (err) {
            render(err);
        } else {
            yargs.showHelp();
        }

        process.exit(1);
    });
