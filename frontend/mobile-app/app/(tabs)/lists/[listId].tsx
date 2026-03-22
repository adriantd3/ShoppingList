import { useLocalSearchParams } from "expo-router";
import { Button, Paragraph, Text, YStack } from "tamagui";

import { clearLastActiveListId } from "../../../src/services/storage/appStorage";
import { ScreenContainer } from "../../../src/ui/ScreenContainer";

export default function ActiveListScreen() {
  const params = useLocalSearchParams<{ listId: string }>();

  const resetLastActive = async () => {
    await clearLastActiveListId();
  };

  return (
    <ScreenContainer>
      <YStack gap="$3">
        <Text fontSize={24} fontWeight="700">
          Active list
        </Text>
        <YStack borderWidth={1} borderColor="$muted" borderRadius={12} padding="$4" backgroundColor="$surface">
          <YStack gap="$2">
            <Paragraph color="$muted">Route bound to list ID:</Paragraph>
            <Text fontWeight="700">{params.listId}</Text>
            <Button onPress={resetLastActive}>Clear last active list pointer</Button>
          </YStack>
        </YStack>
      </YStack>
    </ScreenContainer>
  );
}
