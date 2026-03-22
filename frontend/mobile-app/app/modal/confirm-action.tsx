import { useLocalSearchParams, useRouter } from "expo-router";
import { Paragraph, YStack } from "tamagui";

import { DangerConfirmDialog } from "../../src/ui/DangerConfirmDialog";
import { ScreenContainer } from "../../src/ui/ScreenContainer";

export default function ConfirmActionModal() {
  const router = useRouter();
  const params = useLocalSearchParams<{ title?: string; message?: string; confirmLabel?: string }>();

  return (
    <ScreenContainer>
      <YStack gap="$3">
        <DangerConfirmDialog
          title={params.title ?? "Confirm action"}
          message={params.message ?? "Please confirm this action."}
          confirmLabel={params.confirmLabel ?? "Confirm"}
          isVisible
          onCancel={() => router.back()}
          onConfirm={async () => {
            router.back();
          }}
        />
        <Paragraph color="$muted">This reusable modal is used by destructive flows when a dedicated route is needed.</Paragraph>
      </YStack>
    </ScreenContainer>
  );
}
