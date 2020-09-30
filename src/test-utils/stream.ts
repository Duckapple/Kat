import { PassThrough } from 'stream';

export class StringStream extends PassThrough {
    private buffer = '';
    constructor() {
        super();
        super.on('data', (data: string) => (this.buffer += data));
    }

    get content(): string {
        return this.buffer;
    }
}
