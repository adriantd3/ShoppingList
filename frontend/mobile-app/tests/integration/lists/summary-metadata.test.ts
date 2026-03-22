import { getPurchasedProgressLabel, getPurchasedProgressPercent, getRelativeUpdatedLabel } from "../../../src/features/lists/summaryMetadata";
import type { ListSummary } from "../../../src/features/lists/types";

const buildSummary = (override: Partial<ListSummary> = {}): ListSummary => ({
  id: "list-1",
  name: "Family",
  memberCount: 2,
  purchasedCount: 3,
  totalItems: 6,
  updatedAtIso: "2026-03-22T10:00:00.000Z",
  ...override,
});

describe("summary metadata", () => {
  test("computes purchased progress percent", () => {
    expect(getPurchasedProgressPercent(buildSummary())).toBe(50);
  });

  test("uses zero percent when total items is not positive", () => {
    expect(getPurchasedProgressPercent(buildSummary({ totalItems: 0 }))).toBe(0);
  });

  test("builds purchased progress label", () => {
    expect(getPurchasedProgressLabel(buildSummary())).toBe("3/6");
  });

  test("formats recent relative update label", () => {
    const now = new Date("2026-03-22T10:30:00.000Z");
    expect(getRelativeUpdatedLabel(buildSummary(), now)).toBe("Updated 30m ago");
  });

  test("falls back to generic label for invalid date", () => {
    expect(getRelativeUpdatedLabel(buildSummary({ updatedAtIso: "invalid" }))).toBe("Updated recently");
  });
});
