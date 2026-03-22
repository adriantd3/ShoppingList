import { useState } from "react";
import { useLocalSearchParams } from "expo-router";
import { useQuery } from "@tanstack/react-query";
import { Button, Paragraph, Spinner, Text, YStack } from "tamagui";

import { useAuthSession } from "../../../src/providers/AuthSessionProvider";
import { formatRestoreFeedback } from "../../../src/features/lists/historyLogic";
import { fetchListDetail, restoreLatestSnapshot } from "../../../src/services/lists/listsApi";
import { EmptyStatePanel } from "../../../src/ui/EmptyStatePanel";
import { ErrorStatePanel } from "../../../src/ui/ErrorStatePanel";
import { ScreenContainer } from "../../../src/ui/ScreenContainer";

export default function ListsHistoryScreen() {
  const { listId } = useLocalSearchParams<{ listId?: string }>();
  const { accessToken } = useAuthSession();
  const [feedback, setFeedback] = useState<string | null>(null);
  const [isRestoring, setIsRestoring] = useState(false);

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["lists", "history-source", listId ?? "default-household-list"],
    queryFn: () => fetchListDetail(listId ?? "default-household-list", accessToken),
  });

  const restoreLatest = async () => {
    setIsRestoring(true);

    try {
      const snapshot = await restoreLatestSnapshot(listId ?? "default-household-list", accessToken);
      setFeedback(formatRestoreFeedback(snapshot.snapshotId, snapshot.restoredItemsCount));
      await refetch();
    } catch {
      setFeedback("Unable to restore latest snapshot.");
    } finally {
      setIsRestoring(false);
    }
  };

  return (
    <ScreenContainer>
      <YStack gap="$3">
        <Text fontSize={24} fontWeight="700">
          History
        </Text>
        {isLoading ? (
          <YStack alignItems="center" paddingVertical="$6">
            <Spinner size="large" color="$primary" />
          </YStack>
        ) : null}
        {isError ? (
          <ErrorStatePanel
            title="Unable to load history"
            message="Please retry in a moment."
            onRetry={() => {
              void refetch();
            }}
          />
        ) : null}
        {!isLoading && !isError && data?.items.length === 0 ? (
          <EmptyStatePanel
            title="No closed shopping history"
            description="A snapshot appears after a list reset action."
          />
        ) : null}
        {!isLoading && !isError && data ? (
          <YStack gap="$2">
            <YStack borderWidth={1} borderColor="$muted" borderRadius="$3" padding="$3" backgroundColor="$surface">
              <Text fontWeight="600">Latest available pre-reset snapshot</Text>
              <Paragraph color="$muted">List: {data.name}</Paragraph>
              <Paragraph color="$muted">Items currently in list: {data.items.length}</Paragraph>
            </YStack>
            <Button
              accessibilityLabel="Restore latest snapshot"
              backgroundColor="$primary"
              disabled={isRestoring}
              onPress={() => {
                void restoreLatest();
              }}
            >
              Quick restore latest snapshot
            </Button>
          </YStack>
        ) : null}
        {feedback ? <Paragraph color="$muted">{feedback}</Paragraph> : null}
      </YStack>
    </ScreenContainer>
  );
}
