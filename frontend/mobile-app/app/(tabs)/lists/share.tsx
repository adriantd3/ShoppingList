import { useState } from "react";
import { useLocalSearchParams } from "expo-router";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Button, Paragraph, Text, YStack } from "tamagui";

import { useAuthSession } from "../../../src/providers/AuthSessionProvider";
import { fetchShareLinks, issueShareLink, revokeShareLink } from "../../../src/services/lists/listsApi";
import { EmptyStatePanel } from "../../../src/ui/EmptyStatePanel";
import { ErrorStatePanel } from "../../../src/ui/ErrorStatePanel";
import { ScreenContainer } from "../../../src/ui/ScreenContainer";

export default function ShareScreen() {
  const { listId } = useLocalSearchParams<{ listId: string }>();
  const { accessToken } = useAuthSession();
  const queryClient = useQueryClient();
  const [feedback, setFeedback] = useState<string | null>(null);

  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["lists", "share-links", listId],
    queryFn: () => fetchShareLinks(listId ?? "", accessToken),
    enabled: Boolean(listId),
  });

  const generate = async () => {
    if (!listId) {
      return;
    }

    await issueShareLink(listId, accessToken);
    await queryClient.invalidateQueries({ queryKey: ["lists", "share-links", listId] });
    setFeedback("Share link generated.");
  };

  const revoke = async (shareLinkId: string) => {
    if (!listId) {
      return;
    }

    await revokeShareLink(listId, shareLinkId, accessToken);
    await queryClient.invalidateQueries({ queryKey: ["lists", "share-links", listId] });
    setFeedback("Share link revoked.");
  };

  return (
    <ScreenContainer>
      <YStack gap="$3">
        <Text fontSize={24} fontWeight="700">
          Share
        </Text>
        <Button accessibilityLabel="Generate share link" onPress={() => {
          void generate();
        }} backgroundColor="$primary">
          Generate link
        </Button>
        {feedback ? <Paragraph color="$muted">{feedback}</Paragraph> : null}
        {isError ? (
          <ErrorStatePanel
            title="Unable to load share links"
            message="Try again in a moment."
            onRetry={() => {
              void refetch();
            }}
          />
        ) : null}
        {!isLoading && !isError && data?.length === 0 ? (
          <EmptyStatePanel title="No active links" description="Generate a link to invite members." />
        ) : null}
        <YStack gap="$2">
          {data?.map((entry) => (
            <YStack key={entry.id} borderWidth={1} borderColor="$muted" borderRadius="$3" padding="$3" backgroundColor="$surface" gap="$2">
              <Paragraph numberOfLines={1}>Token: {entry.token}</Paragraph>
              <Text color="$muted">Expires: {new Date(entry.expiresAtIso).toLocaleString()}</Text>
              <Text color="$muted">Revoked: {entry.revokedAtIso ? "yes" : "no"}</Text>
              <Button
                accessibilityLabel="Revoke share link"
                backgroundColor="$danger"
                onPress={() => {
                  void revoke(entry.id);
                }}
              >
                Revoke link
              </Button>
            </YStack>
          ))}
        </YStack>
      </YStack>
    </ScreenContainer>
  );
}
