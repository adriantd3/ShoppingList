import { Link } from "expo-router";
import { Button, Paragraph, Text, YStack } from "tamagui";

import { ScreenContainer } from "../../src/ui/ScreenContainer";

export default function RegisterScreen() {
  return (
    <ScreenContainer justifyContent="center">
      <YStack borderWidth={1} borderColor="$muted" borderRadius={12} padding="$4" backgroundColor="$surface">
        <YStack gap="$3">
          <Text fontSize={24} fontWeight="700">
            Register
          </Text>
          <Paragraph color="$muted">
            Registration API wiring arrives in Feature 001 execution. This route is available for flow completeness.
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
