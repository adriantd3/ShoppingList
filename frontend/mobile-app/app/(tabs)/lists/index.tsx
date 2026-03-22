import { useRouter } from "expo-router";
import { Button, Paragraph, Text, YStack } from "tamagui";

import { useAppPreferences } from "../../../src/providers/AppPreferencesProvider";
import { ScreenContainer } from "../../../src/ui/ScreenContainer";

const DEMO_LIST_ID = "default-household-list";

export default function ListsScreen() {
  const router = useRouter();
  const { saveLastActiveListId } = useAppPreferences();

  const openDemoList = async () => {
    await saveLastActiveListId(DEMO_LIST_ID);
    router.push(`/(tabs)/lists/${DEMO_LIST_ID}`);
  };

  return (
    <ScreenContainer>
      <YStack gap="$3">
        <Text fontSize={24} fontWeight="700">
          Lists
        </Text>
        <YStack borderWidth={1} borderColor="$muted" borderRadius={12} padding="$4" backgroundColor="$surface">
          <YStack gap="$2">
            <Text fontSize={20} fontWeight="600">
              Household essentials
            </Text>
            <Paragraph color="$muted">Updated recently. 2 members, 8/12 purchased.</Paragraph>
            <Button backgroundColor="$primary" onPress={openDemoList}>
              Open active list
            </Button>
          </YStack>
        </YStack>
      </YStack>
    </ScreenContainer>
  );
}
