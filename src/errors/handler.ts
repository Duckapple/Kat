import PrettyError from 'pretty-error';
import UserError from './UserError';

// Make global pretty-printer
/* istanbul ignore next */
export const pe = new PrettyError();
/* istanbul ignore next */
pe.appendStyle({
    'pretty-error > header > title > kind': {
        background: 'none',
        color: 'red',
    },
    // Hide stack traces when in production
    'pretty-error > trace': {
        display: process.env.NODE_ENV === 'production' ? 'none' : 'block',
    },
    'pretty-error > trace > item': {
        marginBottom: 0,
        marginLeft: 2,

        bullet: '"<grey>•</grey>"',
    },
    'pretty-error > trace > item > header > pointer > file': {
        color: 'bright-red',
    },

    'pretty-error > trace > item > header > pointer > colon': {
        color: 'red',
    },

    'pretty-error > trace > item > header > pointer > line': {
        color: 'bright-red',
    },

    'pretty-error > trace > item > header > what': {
        color: 'grey',
    },

    'pretty-error > trace > item > footer > addr': {
        display: 'none',
    },
});

export default function render(err: Error): void {
    if (err instanceof UserError) {
        console.error(err.message);
        return;
    }

    console.error(pe.render(err));
}
