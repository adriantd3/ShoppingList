import type { ListItem } from "../../../src/features/lists/types";
import { getDangerCopy, groupItemsByCategory } from "../../../src/features/lists/activeListLogic";

const item = (override: Partial<ListItem>): ListItem => ({
  id: "item-1",
  listId: "list-1",
  name: "Milk",
  quantity: 1,
  unit: "L",
  category: "Dairy",
  note: "",
  isPurchased: false,
  sortIndex: 1,
  updatedAtIso: "2026-03-22T10:00:00.000Z",
  ...override,
});

describe("task 8 active list logic", () => {
  test("groups by category and orders categories alphabetically", () => {
    const grouped = groupItemsByCategory([
      item({ id: "a", category: "Produce", sortIndex: 2 }),
      item({ id: "b", category: "Dairy", sortIndex: 2 }),
      item({ id: "c", category: "Produce", sortIndex: 1 }),
    ]);

    expect(grouped.map(([category]) => category)).toEqual(["Dairy", "Produce"]);
    expect(grouped[1][1].map((entry) => entry.id)).toEqual(["c", "a"]);
  });

  test("returns reset-specific destructive copy", () => {
    expect(getDangerCopy("reset-list")).toEqual({
      title: "Reset list",
      message: "All items will be reset and saved as latest snapshot.",
      confirmLabel: "Reset list",
    });
  });
});
