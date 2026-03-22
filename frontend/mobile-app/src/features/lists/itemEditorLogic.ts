import type { ListItemMutationPayload } from "./types";

export const validateItemEditorInput = (name: string, quantity: string): string | null => {
  if (!name.trim()) {
    return "Name is required.";
  }

  const parsedQuantity = Number(quantity);

  if (!Number.isFinite(parsedQuantity) || parsedQuantity <= 0) {
    return "Quantity must be a positive number.";
  }

  return null;
};

export const buildItemEditorPayload = (input: {
  name: string;
  quantity: string;
  unit: string;
  category: string;
  note: string;
}): Partial<ListItemMutationPayload> => ({
  name: input.name.trim(),
  quantity: Number(input.quantity),
  unit: input.unit,
  category: input.category,
  note: input.note.trim(),
});
