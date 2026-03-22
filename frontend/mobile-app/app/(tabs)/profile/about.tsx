import Constants from "expo-constants";
import { Paragraph, Text, YStack } from "tamagui";

import { buildAboutMetadata } from "../../../src/features/profile/aboutMetadata";
import { ScreenContainer } from "../../../src/ui/ScreenContainer";

const runtimeVersion = Constants.expoConfig?.version ?? "0.0.0";
const environmentLabel = process.env.EXPO_PUBLIC_ENVIRONMENT ?? "development";
const buildNumber = Constants.expoConfig?.ios?.buildNumber ?? Constants.expoConfig?.android?.versionCode ?? "local";
const metadata = buildAboutMetadata({
  runtimeVersion,
  environmentLabel,
  buildNumber,
  now: new Date(),
});

export default function AboutScreen() {
  return (
    <ScreenContainer>
      <YStack gap="$3">
        <Text fontSize={24} fontWeight="700">
          About
        </Text>
        <YStack borderWidth={1} borderColor="$muted" borderRadius="$3" padding="$4" backgroundColor="$surface" gap="$2">
          <Paragraph>Version: {metadata.version}</Paragraph>
          <Paragraph>Environment: {metadata.environment}</Paragraph>
          <Paragraph>Build: {metadata.build}</Paragraph>
          <Paragraph>Build date: {metadata.buildDate}</Paragraph>
        </YStack>
      </YStack>
    </ScreenContainer>
  );
}
