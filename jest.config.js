/* eslint-disable */
module.exports = {
    roots: ['<rootDir>/src'],
    testMatch: ['**/__tests__/**/*.spec.(ts|tsx|js)'],
    transform: {
        '^.+\\.(ts|tsx)$': 'ts-jest',
    },
    collectCoverage: true,
    collectCoverageFrom: ['src/**/*.ts'],
    coveragePathIgnorePatterns: ['/node_modules/', 'src/index.ts'],
};
