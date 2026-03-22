import { formatRestoreFeedback } from "../../../src/features/lists/historyLogic";

describe("task 13 history restore feedback", () => {
  test("formats restore feedback with snapshot id and restored count", () => {
    expect(formatRestoreFeedback("snapshot-7", 4)).toBe("Restored snapshot snapshot-7 with 4 items.");
  });
});
