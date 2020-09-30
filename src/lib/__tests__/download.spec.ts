import { PassThrough } from 'stream';
import nock from 'nock';
import { Extract } from 'unzipper';
import { baseUrl } from '../url';
import { downloadAndExtractZip } from '../download';
import { StringStream } from '../../test-utils/stream';

let stream: StringStream;

jest.mock('unzipper', () => ({
    Extract: jest.fn().mockImplementation(() => stream),
    __esModule: true,
}));

describe('downloadAndExtractZip', () => {
    beforeEach(() => {
        stream = new StringStream();
    });

    it('creates stream from url to zip extraction', async () => {
        const path = 'bar';
        nock(baseUrl()).get('/foo').reply(200, path);

        await downloadAndExtractZip({ url: baseUrl('/foo'), path });

        expect(Extract).toHaveBeenCalledWith({ path });
        expect(stream.content).toEqual('bar');
    });
});
