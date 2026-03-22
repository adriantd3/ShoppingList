import { __testables } from "../../../src/services/lists/listsApi";

describe("task 7 list summary mapping", () => {
  test("maps snake_case summary payload into UI summary model", () => {
    const mapped = __testables.mapRawListSummary({
      list_id: "list-42",
      title: "Weekend",
      members_count: 3,
      checked_items_count: 5,
      items_count: 9,
      updated_at_iso: "2026-03-22T10:00:00.000Z",
    });

    expect(mapped).toEqual({
      id: "list-42",
      name: "Weekend",
      memberCount: 3,
      purchasedCount: 5,
      totalItems: 9,
      updatedAtIso: "2026-03-22T10:00:00.000Z",
    });
  });

  test("ignores malformed entries when parsing summaries array", () => {
    const parsed = __testables.parseListSummaries({
      data: [{ id: "ok", name: "Valid" }, { name: "Missing id" }],
    });

    expect(parsed).toHaveLength(1);
    expect(parsed[0].id).toBe("ok");
  });
});
