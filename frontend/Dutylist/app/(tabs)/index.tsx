import { Link } from "expo-router";
import { useState } from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";
import { Button, ButtonText } from "@/components/ui/button";
import ListCard from "@/components/home/list-card";
import ListItemCard from "@/components/lists/list-item-card";
import ProductItem from "@/components/products/product-item";

const HomePage = () => {
	const [timesPressed, setTimesPressed] = useState(0);

	let textLog = "";
	if (timesPressed > 1) {
		textLog = timesPressed + "x onPress";
	} else if (timesPressed > 0) {
		textLog = "onPress";
	}

	return (
		<View style={styles.container}>
			<ListCard />
			<ListItemCard />
			<ProductItem />
			<Link href="/auth">Go to Login</Link>
			<Text style={styles.text}>Hello, I am home</Text>
			<Button>
				<ButtonText>Click me</ButtonText>
			</Button>
			<Pressable
				onPress={() => {
					setTimesPressed((current) => current + 1);
				}}
				style={({ pressed }) => [
					{
						backgroundColor: pressed ? "rgb(210, 230, 255)" : "white",
					},
					styles.wrapperCustom,
				]}
			>
				{({ pressed }) => (
					<Text style={styles.text}>{pressed ? "Pressed!" : "Press Me"}</Text>
				)}
			</Pressable>
		</View>
	);
};

const styles = StyleSheet.create({
	container: {
		flex: 1,
		padding: 10,
		justifyContent: "center",
		alignItems: "center",
		backgroundColor: "#fff",
	},
	pressable: {
		backgroundColor: "blue",
		width: 100,
	},
	pressablePressed: {
		backgroundColor: "red",
	},
	text: {
		fontSize: 20,
		fontWeight: "bold",
	},
	textPressed: {
		color: "red",
	},
	wrapperCustom: {
		borderRadius: 8,
		padding: 6,
	},
});

export default HomePage;
