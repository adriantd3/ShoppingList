import { Button, Text, YStack, type YStackProps } from "tamagui";

type ErrorStatePanelProps = YStackProps & {
  title: string;
  message: string;
  onRetry?: () => void;
};

export const ErrorStatePanel = ({ title, message, onRetry, ...rest }: ErrorStatePanelProps) => (
  <YStack
    borderWidth={1}
    borderColor="$danger"
    borderRadius="$3"
    padding="$4"
    backgroundColor="$surface"
    gap="$3"
    {...rest}
  >
    <YStack gap="$1">
      <Text fontSize={20} fontWeight="600">
        {title}
      </Text>
      <Text color="$muted">{message}</Text>
    </YStack>
    {onRetry ? (
      <Button accessibilityLabel="Retry loading lists" onPress={onRetry}>
        Retry
      </Button>
    ) : null}
  </YStack>
);
