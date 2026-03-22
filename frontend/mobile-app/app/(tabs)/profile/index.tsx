import { Button, Paragraph, Text, YStack } from "tamagui";

import { useAuthSession } from "../../../src/providers/AuthSessionProvider";
import { ScreenContainer } from "../../../src/ui/ScreenContainer";

export default function ProfileScreen() {
  const { signOut } = useAuthSession();

  return (
    <ScreenContainer>
      <YStack gap="$3">
        <Text fontSize={24} fontWeight="700">
          Profile
        </Text>
        <YStack borderWidth={1} borderColor="$muted" borderRadius={12} padding="$4" backgroundColor="$surface">
          <YStack gap="$3">
            <Paragraph color="$muted">Basic profile placeholder for Milestone A tab-shell completion.</Paragraph>
            <Button onPress={signOut}>Sign out</Button>
          </YStack>
        </YStack>
      </YStack>
    </ScreenContainer>
  );
}
