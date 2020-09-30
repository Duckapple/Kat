#!/usr/bin/env node

import { CommandModule } from 'yargs';
import { parser } from './lib/cli';
import render from './errors/handler';

import * as getCommand from './commands/getCommand';
import { GetArgs } from './commands/getCommand';

import * as listCommand from './commands/listCommand';
import { ListArgs } from './commands/listCommand';

try {
    parser
        .command(getCommand as CommandModule<Record<string, unknown>, GetArgs>)
        .command(listCommand as CommandModule<Record<string, unknown>, ListArgs>)
        // Parse invokes the correct command, or error handling
        .parse();
} catch (err) {
    render(err);
}
