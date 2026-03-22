import { Button, Paragraph, Text, XStack, YStack } from "tamagui";

type DangerConfirmDialogProps = {
  title: string;
  message: string;
  isVisible: boolean;
  confirmLabel: string;
  isLoading?: boolean;
  onConfirm: () => Promise<void>;
  onCancel: () => void;
};

export const DangerConfirmDialog = ({
  title,
  message,
  isVisible,
  confirmLabel,
  isLoading = false,
  onConfirm,
  onCancel,
}: DangerConfirmDialogProps) => {
  if (!isVisible) {
    return null;
  }

  return (
    <YStack borderWidth={1} borderColor="$danger" borderRadius="$3" padding="$4" gap="$3" backgroundColor="$surface">
      <Text fontSize={20} fontWeight="700" color="$danger">
        {title}
      </Text>
      <Paragraph>{message}</Paragraph>
      <XStack justifyContent="flex-end" gap="$2">
        <Button accessibilityLabel="Cancel dangerous action" onPress={onCancel} disabled={isLoading}>
          Cancel
        </Button>
        <Button
          accessibilityLabel={confirmLabel}
          backgroundColor="$danger"
          onPress={() => {
            void onConfirm();
          }}
          disabled={isLoading}
        >
          {confirmLabel}
        </Button>
      </XStack>
    </YStack>
  );
};
