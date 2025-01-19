import { Stack } from "expo-router";

import "@/global.css";
import { GluestackUIProvider } from "@/components/ui/gluestack-ui-provider";
import { useState } from "react";
import { StatusBar } from "expo-status-bar";

export default function RootLayout() {

	return (
		<GluestackUIProvider mode="system">
			<StatusBar style="auto" />
			<Stack>
				<Stack.Screen name="(tabs)" options={{ headerShown: false }} />
				<Stack.Screen name="login" options={{ headerShown: false }} />
			</Stack>
		</GluestackUIProvider>
	);
}
