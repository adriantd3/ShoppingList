import { Link } from "expo-router";
import { Button, Paragraph, Text, YStack } from "tamagui";

import { ScreenContainer } from "../../src/ui/ScreenContainer";

export default function VerifyEmailScreen() {
  return (
    <ScreenContainer justifyContent="center">
      <YStack borderWidth={1} borderColor="$muted" borderRadius={12} padding="$4" backgroundColor="$surface">
        <YStack gap="$3">
          <Text fontSize={24} fontWeight="700">
            Verify email
          </Text>
          <Paragraph color="$muted">
            Email verification UI is active for routing guard completeness.
          </Paragraph>
          <Link href="/(auth)/login" asChild>
            <Button backgroundColor="$primary">
              Back to login
            </Button>
          </Link>
        </YStack>
      </YStack>
    </ScreenContainer>
  );
}
