import { useMemo, useState } from "react";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useQueryClient } from "@tanstack/react-query";
import { Button, Input, Label, Paragraph, ScrollView, Text, YStack } from "tamagui";

import { ITEM_CATEGORIES, ITEM_UNITS } from "../../src/features/lists/catalogs";
import { buildItemEditorPayload, validateItemEditorInput } from "../../src/features/lists/itemEditorLogic";
import { useAuthSession } from "../../src/providers/AuthSessionProvider";
import { updateListItem } from "../../src/services/lists/listsApi";
import { ScreenContainer } from "../../src/ui/ScreenContainer";

export default function ItemEditorModal() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { accessToken } = useAuthSession();
  const params = useLocalSearchParams<{
    listId: string;
    itemId: string;
    name?: string;
    quantity?: string;
    unit?: string;
    category?: string;
    note?: string;
  }>();

  const [name, setName] = useState(params.name ?? "");
  const [quantity, setQuantity] = useState(params.quantity ?? "1");
  const [unit, setUnit] = useState(params.unit ?? ITEM_UNITS[0]);
  const [category, setCategory] = useState(params.category ?? ITEM_CATEGORIES[0]);
  const [note, setNote] = useState(params.note ?? "");
  const [error, setError] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  const validationError = useMemo(() => {
    return validateItemEditorInput(name, quantity);
  }, [name, quantity]);

  const save = async () => {
    const listId = params.listId ?? "";
    const itemId = params.itemId ?? "";

    if (!listId || !itemId) {
      setError("Missing item context.");
      return;
    }

    if (validationError) {
      setError(validationError);
      return;
    }

    setError(null);
    setIsSaving(true);

    try {
      await updateListItem(
        listId,
        itemId,
        buildItemEditorPayload({ name, quantity, unit, category, note }),
        accessToken,
      );

      await queryClient.invalidateQueries({ queryKey: ["lists", "detail", listId] });
      router.back();
    } catch {
      setError("Unable to save item changes.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <ScreenContainer>
      <ScrollView>
        <YStack gap="$3">
          <Text fontSize={24} fontWeight="700">
            Edit item
          </Text>

          <YStack gap="$2">
            <Label htmlFor="item-name">Name</Label>
            <Input id="item-name" value={name} onChangeText={setName} />
          </YStack>

          <YStack gap="$2">
            <Label htmlFor="item-quantity">Quantity</Label>
            <Input id="item-quantity" value={quantity} onChangeText={setQuantity} keyboardType="decimal-pad" />
          </YStack>

          <YStack gap="$2">
            <Label>Unit</Label>
            <YStack gap="$2">
              {ITEM_UNITS.map((entry) => (
                <Button
                  key={entry}
                  onPress={() => setUnit(entry)}
                  backgroundColor={entry === unit ? "$primary" : "$surface"}
                >
                  {entry}
                </Button>
              ))}
            </YStack>
          </YStack>

          <YStack gap="$2">
            <Label>Category</Label>
            <YStack gap="$2">
              {ITEM_CATEGORIES.map((entry) => (
                <Button
                  key={entry}
                  onPress={() => setCategory(entry)}
                  backgroundColor={entry === category ? "$primary" : "$surface"}
                >
                  {entry}
                </Button>
              ))}
            </YStack>
          </YStack>

          <YStack gap="$2">
            <Label htmlFor="item-note">Note</Label>
            <Input id="item-note" value={note} onChangeText={setNote} />
          </YStack>

          {error ? <Paragraph color="$danger">{error}</Paragraph> : null}

          <Button
            accessibilityLabel="Save item"
            backgroundColor="$primary"
            onPress={() => {
              void save();
            }}
            disabled={isSaving}
          >
            Save changes
          </Button>

          <Button accessibilityLabel="Cancel edit item" onPress={() => router.back()}>
            Cancel
          </Button>
        </YStack>
      </ScrollView>
    </ScreenContainer>
  );
}
