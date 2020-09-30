export function baseUrl(suffix = ''): string {
    return `https://open.kattis.com${suffix}`; // TODO: Improve based on contest mode / config
}
