import { View, StyleSheet } from "react-native";
import { Pressable, Animated, Image } from "react-native";
import { Text } from "@/components/ui/text";

import {
	Checkbox,
	CheckboxIndicator,
	CheckboxIcon,
} from "@/components/ui/checkbox";
import { CheckIcon } from "@/components/ui/icon";
import { HStack } from "../ui/hstack";
import { useRef } from "react";
import { onPressInCard, onPressOutCard } from "@/components/utils/animations";

const ListItemCard = (item, state) => {
	const scaleValue = useRef(new Animated.Value(1)).current;

	const onPressIn = () => {
		onPressInCard(scaleValue);
	};

	const onPressOut = () => {
		onPressOutCard(scaleValue);
	};

	return (
		<Pressable onPressIn={onPressIn} onPressOut={onPressOut} className="w-full">
			<Animated.View
				style={[
					styles.cardShape,
					{ transform: [{ scale: scaleValue }] },
					styles.cardColorPurchased,
				]}
			>
				<Image
					source={{
						uri: "https://i.pinimg.com/236x/34/22/2a/34222a8f0d41c9158729fe194a789268.jpg",
					}}
					style={styles.image}
					alt="Heinz's Ketchup"
				/>
				<View style={styles.content}>
					<Text size="lg" numberOfLines={2} style={styles.text}>
						Heinz's Ketchup deded ed asd a SNdasnnd ndededdeded edede d
					</Text>
					<HStack style={styles.side_content} space={"xl"}>
						<Text size="lg" bold numberOfLines={1}>
							2 ud
						</Text>
						<Checkbox size="lg">
							<CheckboxIndicator>
								<CheckboxIcon as={CheckIcon} />
							</CheckboxIndicator>
						</Checkbox>
					</HStack>
				</View>
			</Animated.View>
		</Pressable>
	);
};

const styles = StyleSheet.create({
	cardShape: {
		width: "100%",
		flexDirection: "row",
		backgroundColor: "lightgray",
		borderRadius: 10,
	},
	cardColorPending: {
		backgroundColor: "lightgray",
	},
	cardColorPurchased: {
		backgroundColor: "lightgreen",
	},
	image: {
		height: 80,
		width: 80,
		borderRadius: 10,
	},
	text: {
		width: "55%",
	},
	content: {
		flex: 1,
		padding: 10,
		flexDirection: "row",
		justifyContent: "space-around",
		alignItems: "center",
	},
	side_content: {
		flex: 1,
		flexDirection: "row",
		alignItems: "center",
		justifyContent: "flex-end",
		paddingEnd: 10,
	},
});

export default ListItemCard;
