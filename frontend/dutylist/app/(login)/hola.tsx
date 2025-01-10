import React, { useState } from "react";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { StyleSheet } from "react-native";
import { Button, ButtonSpinner, ButtonText } from "@/components/ui/button";
import {
	FormControl,
	FormControlError,
	FormControlErrorText,
	FormControlLabel,
	FormControlLabelText,
} from "@/components/ui/form-control";
import { Input, InputField } from "@/components/ui/input";
import { VStack } from "@/components/ui/vstack";
import { Heading } from "@/components/ui/heading";
import { Text } from "@/components/ui/text";

export default function LoginScreen() {
	const insets = useSafeAreaInsets();
	const [status, setStatus] = useState<"off" | "submitting" | "submitted">(
		"off"
	);
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const [error, setError] = useState(false);

	const handleSubmit = async () => {
		console.log("submitting");
		setStatus("submitting");
		// Aquí iría la lógica para enviar los datos del formulario

		console.log("EMAIL", email);
		console.log("PASSWORD", password);
	};

	const styles = StyleSheet.create({
		container: {
			flex: 1,
			paddingTop: insets.top,
			paddingLeft: 24,
			paddingRight: 24,
			paddingBottom: insets.bottom,
		},
	});

	return (
		<VStack space="4xl" style={styles.container}>
			<VStack>
				<Heading size="2xl">Log in to your account</Heading>
				<Text>Don't have an account? Sign Up</Text>
			</VStack>
			<VStack space="md">
				<FormControl isInvalid={error}>
					<FormControlLabel>
						<FormControlLabelText>Email</FormControlLabelText>
					</FormControlLabel>
					<Input variant="outline" size="md">
						<InputField value={email} onChangeText={setEmail} />
					</Input>
				</FormControl>
				<FormControl isInvalid={error}>
					<FormControlLabel>
						<FormControlLabelText>Password</FormControlLabelText>
					</FormControlLabel>
					<Input variant="outline" size="md">
						<InputField
							value={password}
							onChangeText={setPassword}
							type="password"
						/>
					</Input>
					<FormControlError>
						<FormControlErrorText>
							Incorrect email or password
						</FormControlErrorText>
					</FormControlError>
				</FormControl>
				<Button
					onPress={handleSubmit}
					action="primary"
					variant="solid"
					size="lg"
					isDisabled={status == "submitting"}
				>
					{status == "submitting" ? <ButtonSpinner /> : null}
					<ButtonText>
						{status == "submitting" ? "Please wait" : "Log in"}
					</ButtonText>
				</Button>
			</VStack>
		</VStack>
	);
}
