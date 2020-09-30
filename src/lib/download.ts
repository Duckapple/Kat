import got from 'got/dist/source';
import stream from 'stream';
import { Extract } from 'unzipper';
import { promisify } from 'util';

const pipeline = promisify(stream.pipeline);

export async function downloadAndExtractZip({ url, path }: { url: string; path: string }): Promise<void> {
    await pipeline(got.stream(url), Extract({ path }));
}
