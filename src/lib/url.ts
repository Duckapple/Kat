import { basename } from 'path';

export function baseUrl(suffix = '') {
    return `https://open.kattis.com${suffix}`; // TODO: Improve based on contest mode / config
}
