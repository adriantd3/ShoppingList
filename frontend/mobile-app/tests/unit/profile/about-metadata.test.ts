import { buildAboutMetadata } from "../../../src/features/profile/aboutMetadata";

describe("task 12 about metadata", () => {
  test("builds deterministic about metadata", () => {
    const metadata = buildAboutMetadata({
      runtimeVersion: "1.2.3",
      environmentLabel: "staging",
      buildNumber: 45,
      now: new Date("2026-03-22T13:15:00.000Z"),
    });

    expect(metadata).toEqual({
      version: "1.2.3",
      environment: "staging",
      build: "45",
      buildDate: "2026-03-22",
    });
  });
});
