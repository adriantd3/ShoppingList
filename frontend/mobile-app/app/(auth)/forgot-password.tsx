import { Link } from "expo-router";
import { Button, Paragraph, Text, YStack } from "tamagui";

import { ScreenContainer } from "../../src/ui/ScreenContainer";

export default function ForgotPasswordScreen() {
  return (
    <ScreenContainer justifyContent="center">
      <YStack borderWidth={1} borderColor="$muted" borderRadius={12} padding="$4" backgroundColor="$surface">
        <YStack gap="$3">
          <Text fontSize={24} fontWeight="700">
            Recover password
          </Text>
          <Paragraph color="$muted">
            Password recovery endpoint integration is planned in Feature 001 auth execution.
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
