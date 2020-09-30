import { CommandModule } from 'yargs';

import * as getCommand from './commands/getCommand';
import * as listCommand from './commands/listCommand';
import { parser } from './lib/cli';
import render from './errors/handler';

try {
    parser
        .command(getCommand as CommandModule<any, any>)
        .command(listCommand as CommandModule<any, any>)
        // Parse invokes the correct command, or error handling
        .parse();
} catch (err) {
    render(err);
}
