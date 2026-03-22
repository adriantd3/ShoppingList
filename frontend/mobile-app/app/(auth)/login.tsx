import { Link, useRouter } from "expo-router";
import { useState } from "react";
import { Button, Input, Label, Paragraph, Text, YStack } from "tamagui";

import { useAuthSession } from "../../src/providers/AuthSessionProvider";
import { ScreenContainer } from "../../src/ui/ScreenContainer";

export default function LoginScreen() {
  const router = useRouter();
  const { signIn } = useAuthSession();

  const [email, setEmail] = useState("demo@shoppinglist.dev");
  const [password, setPassword] = useState("DemoPass123!");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const submit = async () => {
    if (!email || !password) {
      setErrorMessage("Email and password are required.");
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      await signIn(email.trim(), password);
      router.replace("/(tabs)/lists");
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Login failed.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <ScreenContainer justifyContent="center">
      <YStack borderWidth={1} borderColor="$muted" borderRadius={12} padding="$4" backgroundColor="$surface">
        <YStack gap="$3">
          <Text fontSize={24} fontWeight="700">
            Login
          </Text>

          <YStack gap="$2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" value={email} onChangeText={setEmail} autoCapitalize="none" />
          </YStack>

          <YStack gap="$2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" value={password} onChangeText={setPassword} secureTextEntry />
          </YStack>

          {errorMessage ? <Paragraph color="$danger">{errorMessage}</Paragraph> : null}

          <Button backgroundColor="$primary" disabled={isSubmitting} onPress={submit}>
            {isSubmitting ? "Signing in..." : "Sign in"}
          </Button>

          <Link href="/(auth)/register">Create account</Link>
          <Link href="/(auth)/forgot-password">Forgot password?</Link>
          <Link href="/(auth)/verify-email">Verify email</Link>
        </YStack>
      </YStack>
    </ScreenContainer>
  );
}
