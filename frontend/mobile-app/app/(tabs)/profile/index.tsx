import { useRouter } from "expo-router";
import { useQuery } from "@tanstack/react-query";
import { Button, Paragraph, Spinner, Text, YStack } from "tamagui";

import { useAuthSession } from "../../../src/providers/AuthSessionProvider";
import { fetchProfile } from "../../../src/services/lists/listsApi";
import { ErrorStatePanel } from "../../../src/ui/ErrorStatePanel";
import { ScreenContainer } from "../../../src/ui/ScreenContainer";

export default function ProfileScreen() {
  const router = useRouter();
  const { accessToken, signOut } = useAuthSession();

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["profile", "basic"],
    queryFn: () => fetchProfile(accessToken),
  });

  return (
    <ScreenContainer>
      <YStack gap="$3">
        <Text fontSize={24} fontWeight="700">
          Profile
        </Text>
        {isLoading ? (
          <YStack alignItems="center" paddingVertical="$6">
            <Spinner size="large" color="$primary" />
          </YStack>
        ) : null}
        {isError ? (
          <ErrorStatePanel
            title="Unable to load profile"
            message="Try again in a moment."
            onRetry={() => {
              void refetch();
            }}
          />
        ) : null}
        <YStack borderWidth={1} borderColor="$muted" borderRadius={12} padding="$4" backgroundColor="$surface" gap="$3">
          <YStack gap="$3">
            <Paragraph color="$muted">Basic account data for your shopping profile.</Paragraph>
            <Text fontWeight="700">{data?.displayName ?? "Shopping User"}</Text>
            <Text color="$muted">{data?.email ?? "user@shoppinglist.dev"}</Text>
            <Text color="$muted">Status: {data?.isActive ? "Active" : "Inactive"}</Text>
            <Button
              accessibilityLabel="Open notification settings"
              onPress={() => router.push("/(tabs)/profile/notifications")}
            >
              Notification settings
            </Button>
            <Button accessibilityLabel="Open about screen" onPress={() => router.push("/(tabs)/profile/about")}>
              About
            </Button>
            <Button onPress={signOut}>Sign out</Button>
          </YStack>
        </YStack>
      </YStack>
    </ScreenContainer>
  );
}
