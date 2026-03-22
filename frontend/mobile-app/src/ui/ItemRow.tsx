import { Button, Checkbox, Paragraph, Text, XStack, YStack } from "tamagui";

import type { ListItem } from "../features/lists/types";

type ItemRowProps = {
  item: ListItem;
  onTogglePurchased: (itemId: string, nextState: boolean) => Promise<void>;
  onEdit: (itemId: string) => void;
  onDelete: (itemId: string) => void;
};

export const ItemRow = ({ item, onTogglePurchased, onEdit, onDelete }: ItemRowProps) => (
  <XStack
    borderWidth={1}
    borderColor="$muted"
    borderRadius="$3"
    padding="$3"
    backgroundColor="$surface"
    justifyContent="space-between"
    alignItems="center"
    gap="$3"
  >
    <XStack gap="$3" alignItems="center" flex={1}>
      <Checkbox
        checked={item.isPurchased}
        onCheckedChange={(checked) => {
          void onTogglePurchased(item.id, Boolean(checked));
        }}
        accessibilityLabel={`Mark ${item.name} as purchased`}
      >
        <Checkbox.Indicator />
      </Checkbox>
      <YStack flex={1}>
        <Text fontWeight="600" textDecorationLine={item.isPurchased ? "line-through" : "none"}>
          {item.name}
        </Text>
        <Paragraph color="$muted">
          {item.quantity} {item.unit} • {item.category}
        </Paragraph>
      </YStack>
    </XStack>
    <XStack gap="$2">
      <Button
        size="$2"
        accessibilityLabel={`Edit ${item.name}`}
        onPress={() => onEdit(item.id)}
      >
        Edit
      </Button>
      <Button
        size="$2"
        backgroundColor="$danger"
        accessibilityLabel={`Delete ${item.name}`}
        onPress={() => onDelete(item.id)}
      >
        Delete
      </Button>
    </XStack>
  </XStack>
);
