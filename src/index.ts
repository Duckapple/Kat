import yargs, { CommandModule, onFinishCommand } from 'yargs';

import * as getCommand from './commands/getCommand';
import { parser } from './lib/cli';
import render from './errors/handler';

try {
    // https://github.com/yargs/yargs/blob/master/docs/advanced.md#building-configurable-cli-apps
    parser.command(getCommand as CommandModule<any, any>).parse();
} catch (err) {
    render(err);
}
