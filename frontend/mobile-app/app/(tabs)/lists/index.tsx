import { useRouter } from "expo-router";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Button, Spinner, Text, YStack } from "tamagui";

import { useAuthSession } from "../../../src/providers/AuthSessionProvider";
import { useConnectivity } from "../../../src/providers/ConnectivityProvider";
import { useAppPreferences } from "../../../src/providers/AppPreferencesProvider";
import { createList, fetchListSummaries } from "../../../src/services/lists/listsApi";
import { EmptyStatePanel } from "../../../src/ui/EmptyStatePanel";
import { ErrorStatePanel } from "../../../src/ui/ErrorStatePanel";
import { ListSummaryCard } from "../../../src/ui/ListSummaryCard";
import { OfflineBanner } from "../../../src/ui/OfflineBanner";
import { ScreenContainer } from "../../../src/ui/ScreenContainer";

export default function ListsScreen() {
  const router = useRouter();
  const { saveLastActiveListId } = useAppPreferences();
  const { accessToken } = useAuthSession();
  const { isOnline } = useConnectivity();
  const queryClient = useQueryClient();

  const {
    data: summaries,
    isLoading,
    isError,
    refetch,
    isFetching,
  } = useQuery({
    queryKey: ["lists", "summaries"],
    queryFn: () => fetchListSummaries(accessToken),
  });

  const openList = async (listId: string) => {
    await saveLastActiveListId(listId);
    router.push(`/(tabs)/lists/${encodeURIComponent(listId)}`);
  };

  const handleCreateList = async () => {
    const defaultName = `New list ${new Date().toLocaleDateString()}`;
    const created = await createList({ name: defaultName }, accessToken);
    await queryClient.invalidateQueries({ queryKey: ["lists", "summaries"] });
    await openList(created.id);
  };

  const hasSummaries = Boolean(summaries && summaries.length > 0);

  const renderBody = () => {
    if (isLoading || isFetching) {
      return (
        <YStack gap="$2" alignItems="center" paddingVertical="$6">
          <Spinner size="large" color="$primary" />
          <Text color="$muted">Loading your lists...</Text>
        </YStack>
      );
    }

    if (isError) {
      return (
        <ErrorStatePanel
          title="Unable to load lists"
          message="Check your connection or backend status, then retry."
          onRetry={() => {
            void refetch();
          }}
        />
      );
    }

    if (!hasSummaries) {
      return (
        <EmptyStatePanel
          title="No lists yet"
          description="Create your first list to start shopping together."
        />
      );
    }

    return (
      <YStack gap="$3">
        {summaries?.map((summary) => (
          <ListSummaryCard key={summary.id} summary={summary} onOpen={(listId) => {
            void openList(listId);
          }} />
        ))}
      </YStack>
    );
  };

  return (
    <ScreenContainer>
      <YStack gap="$3">
        <Text fontSize={24} fontWeight="700">
          Lists
        </Text>
        {!isOnline ? <OfflineBanner pendingCount={0} /> : null}
        <YStack gap="$2">
          <Button accessibilityLabel="Create list" backgroundColor="$primary" onPress={() => {
            void handleCreateList();
          }}>
            Create list
          </Button>
          <Button accessibilityLabel="Open history" onPress={() => router.push("/(tabs)/lists/history")}>
            History
          </Button>
        </YStack>
        {renderBody()}
      </YStack>
    </ScreenContainer>
  );
}
