import React from "react";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Alert, StyleSheet } from "react-native";
import { Link } from "expo-router";
import { Heading } from "@/components/ui/heading";
import { Text } from "@/components/ui/text";
import { VStack } from "@/components/ui/vstack";
import {
    Button,
    ButtonText,
  } from '@/components/ui/button';
export default function WelcomeScreen() {
	const insets = useSafeAreaInsets();
	const [count, setCount] = React.useState(0);

	const handleLogin = () => {
		setCount(count + 1);
		Alert.alert("Login", "You have logged in!");
	};
	const styles = StyleSheet.create({
		container: {
			paddingTop: insets.top,
			paddingLeft: 24,
			paddingRight: 24,
			paddingBottom: insets.bottom,
			flex: 1,
			justifyContent: "center",
			alignItems : "center",
		},
		text: {
			textAlign: "center",
		},
		buttons :{
			width: "60%",
		}
		
	});
	return (
		<VStack space="4xl" style={styles.container}>
			<VStack>
				<Heading size="3xl" style={styles.text}>Welcome to DutyList</Heading>
				<Text size="lg" style={styles.text}>
					Manage and share your shopping list in an easy and comfortable way!
				</Text>
			</VStack>
			<VStack space="lg" style={styles.buttons}>
				<Link href='auth/hola' asChild>
					<Button
						action={"primary"}
						variant={"solid"}
						size={"xl"}
						isDisabled={false}
					>
						<ButtonText>Log In</ButtonText>
					</Button>
				</Link>
				<Button
					action={"secondary"}
					variant={"solid"}
					size={"xl"}
					isDisabled={false}
				>
					<ButtonText>Sign In</ButtonText>
				</Button>
			</VStack>
		</VStack>
	);
}
