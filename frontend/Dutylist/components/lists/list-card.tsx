import { View, StyleSheet } from "react-native";
import { Pressable, Animated } from "react-native";
import { Text } from "@/components/ui/text";
import {
	Avatar,
	AvatarBadge,
	AvatarFallbackText,
	AvatarGroup,
	AvatarImage,
} from "@/components/ui/avatar";
import { Icon, ThreeDotsIcon } from "@/components/ui/icon";
import React, { useState, useRef } from "react";
import { onPressInCard, onPressOutCard } from "../utils/animations";
import { List } from "./types/List.types";

interface ListCardProps {
	list: List;
	manageOptions?: () => void;
}

const ListCard: React.FC<ListCardProps> = ({ list, manageOptions: manageOptions }) => {
	const [active, setActive] = useState(false);
	const scaleValue = useRef(new Animated.Value(1)).current;

	const onPressIn = () => {
		setActive(true);
		onPressInCard(scaleValue);
	};

	const onPressOut = () => {
		setActive(false);
		onPressOutCard(scaleValue);
	};

	const extraAvatars = list.avatars.slice(4);
	const remainingCount = extraAvatars.length;

	return (
		<Pressable
			onPress={() => console.log(`Pressed ${list.name}`)}
			onPressIn={onPressIn}
			onPressOut={onPressOut}
			onLongPress={manageOptions}
		>
			<Animated.View
				style={[
					styles.cardShape,
					{ transform: [{ scale: scaleValue }] },
					active && styles.pressedCard,
				]}
			>
				<View style={styles.itemsGroup}>
					<Text size="3xl" style={styles.titleStyle} numberOfLines={1} bold>
						{list.name}
					</Text>
					<Pressable onPress={manageOptions}>
						<Icon as={ThreeDotsIcon} size="xl" style={styles.titleStyle} />
					</Pressable>
				</View>

				<View style={styles.itemsGroup}>
					<AvatarGroup>
						{list.avatars.slice(0,4)
							.map((avatar, index) => (
								<Avatar key={index} size="md">
									<AvatarImage source={{ uri: avatar }} />
								</Avatar>
							))
							.concat(
								remainingCount > 0
									? [
											<Avatar key="extra" size="md">
												<AvatarFallbackText>{`+ ${remainingCount}`}</AvatarFallbackText>
											</Avatar>,
									  ]
									: []
							)}
					</AvatarGroup>

					<Text style={styles.subTitleStyle} numberOfLines={1} bold>
						{list.n_items} items
					</Text>
				</View>
			</Animated.View>
		</Pressable>
	);
};

const styles = StyleSheet.create({
	cardShape: {
		flexDirection: "column",
		justifyContent: "space-between",
		width: 350,
		height: 150,
		borderRadius: 10,
		backgroundColor: "lightblue",
		padding: 15,
		marginBottom: 10,
	},
	pressedCard: {
		filter: "brightness(0.95)",
	},
	itemsGroup: {
		paddingStart: 10,
		flexDirection: "row",
		justifyContent: "space-between",
		alignItems: "center",
	},
	titleStyle: {
		color: "white",
		textShadowColor: "black",
		textShadowRadius: 1,
		textShadowOffset: { width: 0.75, height: 0.75 },
	},
	subTitleStyle: {
		color: "white",
		fontSize: 16,
		textShadowColor: "black",
		textShadowRadius: 1,
		textShadowOffset: { width: 0.75, height: 0.75 },
	},
});

export default ListCard;
