import * as Notifications from "expo-notifications";
import { useRouter } from "expo-router";
import { Button, Paragraph, Text, YStack } from "tamagui";

import { useAppPreferences } from "../../src/providers/AppPreferencesProvider";
import { ScreenContainer } from "../../src/ui/ScreenContainer";

export default function OnboardingScreen() {
  const router = useRouter();
  const { completeOnboarding, savePushPermissionStatus } = useAppPreferences();

  const requestPermission = async () => {
    const current = await Notifications.getPermissionsAsync();

    if (current.granted) {
      await savePushPermissionStatus(current.status);
      return;
    }

    const requested = await Notifications.requestPermissionsAsync();
    await savePushPermissionStatus(requested.status);
  };

  const finishOnboarding = async () => {
    await requestPermission();
    await completeOnboarding();
    router.replace("/(auth)/login");
  };

  return (
    <ScreenContainer justifyContent="center">
      <YStack borderWidth={1} borderColor="$muted" borderRadius={12} padding="$4" backgroundColor="$surface">
        <YStack gap="$3">
          <Text fontSize={24} fontWeight="700">
            Welcome to ShoppingList
          </Text>
          <Paragraph color="$muted">
            We ask notification permission once so you can receive only key collaboration events.
          </Paragraph>
          <Button backgroundColor="$primary" onPress={finishOnboarding}>
            Continue
          </Button>
        </YStack>
      </YStack>
    </ScreenContainer>
  );
}
