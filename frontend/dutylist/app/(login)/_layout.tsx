import { Stack } from 'expo-router';

export default function LoginLayout() {
  return (
    <Stack>
      <Stack.Screen
        name="index"
        options={{
          headerShown: false,
          presentation: 'modal',
        }}
      />
      <Stack.Screen name="hola" options={{
        headerTitle: 'Back',
        headerShown: true,
        presentation: 'modal',
      }}/>
      <Stack.Screen name='register'/>
    </Stack>
  );
}
