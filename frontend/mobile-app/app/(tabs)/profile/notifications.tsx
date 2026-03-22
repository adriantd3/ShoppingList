import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Paragraph, Spinner, Switch, Text, XStack, YStack } from "tamagui";

import { useAuthSession } from "../../../src/providers/AuthSessionProvider";
import {
  fetchNotificationPreferences,
  updateNotificationPreferences,
} from "../../../src/services/lists/listsApi";
import { ErrorStatePanel } from "../../../src/ui/ErrorStatePanel";
import { ScreenContainer } from "../../../src/ui/ScreenContainer";

export default function NotificationSettingsScreen() {
  const { accessToken } = useAuthSession();
  const [isSaving, setIsSaving] = useState(false);

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["profile", "notifications"],
    queryFn: () => fetchNotificationPreferences(accessToken),
  });

  const onToggle = async (nextValue: boolean) => {
    setIsSaving(true);

    try {
      await updateNotificationPreferences(nextValue, accessToken);
      await refetch();
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <ScreenContainer>
      <YStack gap="$3">
        <Text fontSize={24} fontWeight="700">
          Notifications
        </Text>
        {isLoading ? (
          <YStack alignItems="center" paddingVertical="$6">
            <Spinner size="large" color="$primary" />
          </YStack>
        ) : null}
        {isError ? (
          <ErrorStatePanel
            title="Unable to load notification settings"
            message="Please retry shortly."
            onRetry={() => {
              void refetch();
            }}
          />
        ) : null}
        {data ? (
          <YStack borderWidth={1} borderColor="$muted" borderRadius="$3" padding="$4" backgroundColor="$surface" gap="$3">
            <XStack justifyContent="space-between" alignItems="center">
              <YStack maxWidth="80%">
                <Text fontWeight="600">List change push notifications</Text>
                <Paragraph color="$muted">Share links, item activity, reset and shopping-end events.</Paragraph>
              </YStack>
              <Switch
                checked={data.listChangePushEnabled}
                onCheckedChange={(checked) => {
                  void onToggle(Boolean(checked));
                }}
                disabled={isSaving}
                accessibilityLabel="Toggle list change push notifications"
              >
                <Switch.Thumb />
              </Switch>
            </XStack>
            <Paragraph color="$muted">Updated: {new Date(data.updatedAtIso).toLocaleString()}</Paragraph>
          </YStack>
        ) : null}
      </YStack>
    </ScreenContainer>
  );
}
