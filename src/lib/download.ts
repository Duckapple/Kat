import stream from 'stream';
import { promisify } from 'util';
import got from 'got/dist/source';
import { Extract } from 'unzipper';

const pipeline = promisify(stream.pipeline);

export async function downloadAndExtractZip({ url, path }: { url: string; path: string }): Promise<void> {
    await pipeline(got.stream(url), Extract({ path }));
}
