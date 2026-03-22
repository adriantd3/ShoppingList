import { useLocalSearchParams } from "expo-router";
import { useQuery } from "@tanstack/react-query";
import { Spinner, Text, YStack } from "tamagui";

import { useAuthSession } from "../../../src/providers/AuthSessionProvider";
import { fetchMembers } from "../../../src/services/lists/listsApi";
import { EmptyStatePanel } from "../../../src/ui/EmptyStatePanel";
import { ErrorStatePanel } from "../../../src/ui/ErrorStatePanel";
import { ScreenContainer } from "../../../src/ui/ScreenContainer";

export default function MembersScreen() {
  const { listId } = useLocalSearchParams<{ listId: string }>();
  const { accessToken } = useAuthSession();

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["lists", "members", listId],
    queryFn: () => fetchMembers(listId ?? "", accessToken),
    enabled: Boolean(listId),
  });

  return (
    <ScreenContainer>
      <YStack gap="$3">
        <Text fontSize={24} fontWeight="700">
          Members
        </Text>
        {isLoading ? (
          <YStack alignItems="center" paddingVertical="$6">
            <Spinner size="large" color="$primary" />
          </YStack>
        ) : null}
        {isError ? (
          <ErrorStatePanel
            title="Unable to load members"
            message="Try again when your connection is stable."
            onRetry={() => {
              void refetch();
            }}
          />
        ) : null}
        {!isLoading && !isError && data?.length === 0 ? (
          <EmptyStatePanel title="No members" description="Invite someone using the share screen." />
        ) : null}
        {!isLoading && !isError ? (
          <YStack gap="$2">
            {data?.map((member) => (
              <YStack key={member.id} borderWidth={1} borderColor="$muted" borderRadius="$3" padding="$3" backgroundColor="$surface">
                <Text fontWeight="600">{member.email}</Text>
                <Text color="$muted">Role: {member.role}</Text>
              </YStack>
            ))}
          </YStack>
        ) : null}
      </YStack>
    </ScreenContainer>
  );
}
