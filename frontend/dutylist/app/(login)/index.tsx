import { Main, Title, Subtitle } from '~/tamagui.config';
import React from 'react';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Text, YStack, Button } from 'tamagui';
import { Alert, StyleSheet } from 'react-native';
import { Link } from 'expo-router';

export default function WelcomeScreen() {
  const insets = useSafeAreaInsets();
  const [count, setCount] = React.useState(0);

  const handleLogin = () => {
    setCount(count + 1);
    Alert.alert('Login', 'You have logged in!');
  };

  const styles = StyleSheet.create({
    container: {
      paddingTop: insets.top,
      paddingLeft: 24,
      paddingRight: 24,
      paddingBottom: insets.bottom,
    },
  });

  return (
    <YStack f={1} ai="center" jc="center" gap="$5" p="$-1.5">
      <YStack maxWidth={350} gap="$3">
        <Title textAlign="center">Welcome to DutyList</Title>
        <Subtitle textAlign="center">
          Manage and share your shopping list in an easy and comfortable way!
        </Subtitle>
      </YStack>
      <YStack gap="$3">
        <Link href='/hola' asChild>
          <Button w="$15">
            Sign in
          </Button>
        </Link>
        <Button theme="active" w="$15" onPress={handleLogin}>
          Sign up
        </Button>
      </YStack>
    </YStack>
  );
}
