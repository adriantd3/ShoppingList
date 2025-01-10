import { Stack } from "expo-router";

import "@/global.css";
import { GluestackUIProvider } from "@/components/ui/gluestack-ui-provider";
import { useState } from "react";
import { StatusBar } from "expo-status-bar";

export default function RootLayout() {
	const [authenticated, setAuthenticated] = useState(false);

	return (
		<GluestackUIProvider mode="system">
			<StatusBar style="auto" />
			{!authenticated ? (
				<Stack>
					<Stack.Screen name="(login)" options={{ headerShown: false }} />
				</Stack>
			) : (
				<Stack>
					<Stack.Screen
						name="(tabs)"
						options={{ headerShown: false, presentation: "modal" }}
					/>
				</Stack>
			)}
		</GluestackUIProvider>
	);
}
