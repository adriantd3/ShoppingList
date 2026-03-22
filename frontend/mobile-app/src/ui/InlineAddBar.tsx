import { useState } from "react";
import { Button, Input, Text, XStack, YStack } from "tamagui";

type InlineAddBarProps = {
  onAdd: (name: string) => Promise<void>;
};

export const InlineAddBar = ({ onAdd }: InlineAddBarProps) => {
  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSaving, setIsSaving] = useState(false);

  const submit = async () => {
    const safeName = name.trim();

    if (!safeName) {
      setError("Item name is required.");
      return;
    }

    setError(null);
    setIsSaving(true);

    try {
      await onAdd(safeName);
      setName("");
    } catch {
      setError("Unable to add item right now.");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <YStack gap="$2">
      <XStack gap="$2" alignItems="center">
        <Input
          flex={1}
          value={name}
          onChangeText={setName}
          placeholder="Quick add item"
          accessibilityLabel="Quick add item name"
        />
        <Button
          accessibilityLabel="Add item"
          backgroundColor="$primary"
          onPress={() => {
            void submit();
          }}
          disabled={isSaving}
        >
          Add
        </Button>
      </XStack>
      {error ? <Text color="$danger">{error}</Text> : null}
    </YStack>
  );
};
