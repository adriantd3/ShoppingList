import { SafeAreaView } from "react-native-safe-area-context";
import { YStack, type YStackProps } from "tamagui";

type ScreenContainerProps = YStackProps;

export const ScreenContainer = ({ children, ...rest }: ScreenContainerProps) => (
  <SafeAreaView style={{ flex: 1 }}>
    <YStack flex={1} backgroundColor="$background" padding="$4" gap="$4" {...rest}>
      {children}
    </YStack>
  </SafeAreaView>
);
