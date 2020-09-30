import { resolve } from 'path';
import { existsSync, mkdirSync } from 'fs';
import { cwd } from 'process';
import got from 'got/dist/source';
import UserError from '../errors/UserError';
import { downloadAndExtractZip } from '../lib/download';
import { baseUrl } from '../lib/url';

export default async function fetchProblem(problemName: string): Promise<void> {
    // If the problem already exists in the user's current directory
    if (existsSync(resolve(cwd(), problemName))) {
        throw new UserError(`The problem '${problemName}' already exists`);
    }

    await ensureProblemIsValid(problemName);

    console.log(`🧰  Initializing problem ${problemName}`);

    // Enure the problem directory exists.
    mkdirSync(problemName, { recursive: true });

    await downloadSampleFiles(problemName);
}

async function ensureProblemIsValid(problemName: string): Promise<void> {
    const response = await got(baseUrl(`/problems/${problemName}`), {
        throwHttpErrors: false,
    });

    if (response.statusCode !== 200) {
        throw new UserError(`⚠️ Problem '${problemName}' does not exist!`);
    }
}

async function downloadSampleFiles(problemName: string): Promise<void> {
    console.log('⬇️  Attempting to download sample files from kattis...');
    return await downloadAndExtractZip({
        url: baseUrl(`/problems/${problemName}/file/statement/samples.zip`),
        path: resolve(cwd(), problemName, `test`),
    });
}
