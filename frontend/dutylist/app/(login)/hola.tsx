import React, { useState } from 'react';
import { Text, YStack, Button, Form } from 'tamagui';
import { Main } from '~/tamagui.config';

export default function LoginScreen() {
  const [status, setStatus] = useState<'off' | 'submitting' | 'submitted'>('off');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async () => {};

  return (
    <YStack f={1} ai="center" jc="center" gap="$5" p="$-1.5">
      <Form onSubmit={handleSubmit}>
        <YStack gap="$3">
          <Text>Email</Text>
        </YStack>
        <YStack gap="$3">
          <Text>Password</Text>
        </YStack>
        <Button w="$15" onPress={() => setStatus('submitting')}>
          Login
        </Button>
      </Form>
    </YStack>
  );
}
