import React from "react";
import { Pressable, Text, View } from "react-native";

type BaseProps = {
  children?: React.ReactNode;
};

type ButtonProps = BaseProps & {
  accessibilityLabel?: string;
  disabled?: boolean;
  onPress?: () => void;
};

export const Button = ({ children, accessibilityLabel, disabled, onPress }: ButtonProps) => (
  <Pressable accessibilityLabel={accessibilityLabel} disabled={disabled} onPress={onPress}>
    <Text>{children}</Text>
  </Pressable>
);

export const Paragraph = ({ children }: BaseProps) => <Text>{children}</Text>;
export const XStack = ({ children }: BaseProps) => <View>{children}</View>;
export const YStack = ({ children }: BaseProps) => <View>{children}</View>;
export { Text };
