import { Redirect, Stack, useSegments } from "expo-router";
import { Spinner, Text, YStack } from "tamagui";

import { useAuthSession } from "../src/providers/AuthSessionProvider";
import { useAppPreferences } from "../src/providers/AppPreferencesProvider";
import { RootProviders } from "../src/providers/RootProviders";
import { resolveEntryRedirect } from "../src/navigation/routeResolution";

const AppShell = () => {
  const segments = useSegments();
  const currentSegment = segments[0];

  const auth = useAuthSession();
  const preferences = useAppPreferences();

  const redirect = resolveEntryRedirect({
    isHydrating: auth.isHydrating || preferences.isHydrating,
    onboardingCompleted: preferences.onboardingCompleted,
    isAuthenticated: auth.isAuthenticated,
    currentSegment,
    lastActiveListId: preferences.lastActiveListId,
  });

  if (auth.isHydrating || preferences.isHydrating) {
    return (
      <YStack flex={1} alignItems="center" justifyContent="center" gap="$3" backgroundColor="$background">
        <Spinner size="large" color="$primary" />
        <Text color="$muted">Preparing app...</Text>
      </YStack>
    );
  }

  if (redirect) {
    return <Redirect href={redirect} />;
  }

  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="onboarding" />
      <Stack.Screen name="(auth)" />
      <Stack.Screen name="(tabs)" />
      <Stack.Screen name="modal" options={{ presentation: "modal" }} />
    </Stack>
  );
};

export default function RootLayout() {
  return (
    <RootProviders>
      <AppShell />
    </RootProviders>
  );
}
