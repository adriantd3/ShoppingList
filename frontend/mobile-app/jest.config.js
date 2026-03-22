module.exports = {
  preset: "jest-expo",
  testMatch: ["**/tests/**/*.test.ts", "**/tests/**/*.test.tsx"],
  moduleNameMapper: {
    "^tamagui$": "<rootDir>/tests/mocks/tamagui.tsx",
  },
};
