import { buildItemEditorPayload, validateItemEditorInput } from "../../../src/features/lists/itemEditorLogic";

describe("task 9 item editor logic", () => {
  test("requires non-empty item name", () => {
    expect(validateItemEditorInput("   ", "1")).toBe("Name is required.");
  });

  test("requires positive numeric quantity", () => {
    expect(validateItemEditorInput("Milk", "0")).toBe("Quantity must be a positive number.");
    expect(validateItemEditorInput("Milk", "abc")).toBe("Quantity must be a positive number.");
  });

  test("builds trimmed payload for update mutation", () => {
    const payload = buildItemEditorPayload({
      name: "  Bread  ",
      quantity: "2",
      unit: "pcs",
      category: "Bakery",
      note: "  seeded  ",
    });

    expect(payload).toEqual({
      name: "Bread",
      quantity: 2,
      unit: "pcs",
      category: "Bakery",
      note: "seeded",
    });
  });
});
