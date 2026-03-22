import { Text, YStack, type YStackProps } from "tamagui";

type EmptyStatePanelProps = YStackProps & {
  title: string;
  description: string;
};

export const EmptyStatePanel = ({ title, description, ...rest }: EmptyStatePanelProps) => (
  <YStack
    borderWidth={1}
    borderColor="$muted"
    borderRadius="$3"
    padding="$4"
    backgroundColor="$surface"
    gap="$2"
    {...rest}
  >
    <Text fontSize={20} fontWeight="600">
      {title}
    </Text>
    <Text color="$muted">{description}</Text>
  </YStack>
);
