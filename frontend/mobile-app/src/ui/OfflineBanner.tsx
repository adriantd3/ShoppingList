import { Text, XStack } from "tamagui";

type OfflineBannerProps = {
  pendingCount: number;
};

export const OfflineBanner = ({ pendingCount }: OfflineBannerProps) => (
  <XStack
    borderRadius="$2"
    borderWidth={1}
    borderColor="$muted"
    backgroundColor="$surface"
    padding="$3"
    justifyContent="space-between"
    alignItems="center"
  >
    <Text fontWeight="600">Offline mode</Text>
    <Text color="$muted">Pending {pendingCount}</Text>
  </XStack>
);
