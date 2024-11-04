import React, { useState } from 'react';
import { Text, YStack, Button, Form, Input, Label } from 'tamagui';
import { Container, Main, Subtitle, Title } from '~/tamagui.config';

export default function LoginScreen() {
  const [status, setStatus] = useState<'off' | 'submitting' | 'submitted'>('off');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async () => {
    console.log('submitting');
    setStatus('submitting');
  };

  return (
    <Form f={1} onSubmit={handleSubmit}>
      <YStack f={1} ai={'flex-start'} jc={'center'} gap="$4" m="$8">
        <Title>Login to your account</Title>
        <Subtitle>Don't have an account? Sign Up</Subtitle>
        <YStack gap="$1" w={'100%'}>
          <Label htmlFor="email" color={'black'}>
            Username or email
          </Label>
          <Input
            id="email"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
            autoComplete="email"
            textContentType="emailAddress"
          />
          <Label htmlFor="password" color={'black'}>
            Password
          </Label>
          <Input id="password" value={password} onChangeText={setPassword} secureTextEntry />
        </YStack>
        {
          // Hacer que el boton sea un componente que reciba el texto, la funcion a aplicar
          // y que cuando se haga click se le ponga un estado de loading
        }
        <Form.Trigger asChild>
          <Button width={'100%'}>Log in</Button>
        </Form.Trigger>
      </YStack>
    </Form>
  );
}
