import { Button, Paragraph, Text, XStack, YStack } from "tamagui";

import { getPurchasedProgressLabel, getPurchasedProgressPercent, getRelativeUpdatedLabel } from "../features/lists/summaryMetadata";
import type { ListSummary } from "../features/lists/types";

type ListSummaryCardProps = {
  summary: ListSummary;
  onOpen: (listId: string) => void;
};

export const ListSummaryCard = ({ summary, onOpen }: ListSummaryCardProps) => {
  const progressPercent = getPurchasedProgressPercent(summary);

  return (
    <YStack borderWidth={1} borderColor="$muted" borderRadius="$3" padding="$4" backgroundColor="$surface" gap="$2">
      <Text fontSize={20} fontWeight="600">
        {summary.name}
      </Text>
      <Paragraph color="$muted">{getRelativeUpdatedLabel(summary)}</Paragraph>
      <XStack justifyContent="space-between">
        <Paragraph color="$muted">Members: {summary.memberCount}</Paragraph>
        <Paragraph color="$muted">
          Progress: {progressPercent}% ({getPurchasedProgressLabel(summary)})
        </Paragraph>
      </XStack>
      <Button
        accessibilityLabel={`Open list ${summary.name}`}
        backgroundColor="$primary"
        onPress={() => onOpen(summary.id)}
      >
        Open list
      </Button>
    </YStack>
  );
};
