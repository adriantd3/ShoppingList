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
import { useState, useRef } from "react";

const ListCard = (list) => {
	const [active, setActive] = useState(false);
	const scaleValue = useRef(new Animated.Value(1)).current;

	const onPressIn = () => {
		setActive(true);
		Animated.timing(scaleValue, {
			toValue: 0.95,
			duration: 150, // Duración en milisegundos
			useNativeDriver: true,
		}).start();
	};

	const onPressOut = () => {
		setActive(false);
		Animated.timing(scaleValue, {
			toValue: 1,
			duration: 150, // Duración en milisegundos
			useNativeDriver: true,
		}).start();
	};

	const avatars = [
		{
			src: "https://i.pinimg.com/236x/34/22/2a/34222a8f0d41c9158729fe194a789268.jpg",
		},
		{
			src: "https://static1.personality-database.com/profile_images/02779f99c78745ceb5f3216b666328aa.png",
		},
		{
			src: "https://i.pinimg.com/236x/34/22/2a/34222a8f0d41c9158729fe194a789268.jpg",
		},
		{
			src: "https://static1.personality-database.com/profile_images/02779f99c78745ceb5f3216b666328aa.png",
		},
		{
			src: "https://i.pinimg.com/236x/34/22/2a/34222a8f0d41c9158729fe194a789268.jpg",
		},
		{
			src: "https://static1.personality-database.com/profile_images/02779f99c78745ceb5f3216b666328aa.png",
		},
	];
	const itemsCount = 12;
	const extraAvatars = avatars.slice(4);
	const remainingCount = extraAvatars.length;

	return (
		<Pressable
			onPress={() => console.log("Press detected")}
			onPressIn={onPressIn}
			onPressOut={onPressOut}
		>
			<Animated.View
				style={[
					styles.cardShape,
					{ transform: [{ scale: scaleValue }] },
					active && styles.pressedCard,
				]}
			>
				<View>
					<Text size="3xl" style={styles.titleStyle} numberOfLines={1} bold>
						List title
					</Text>
				</View>

				<View style={styles.itemsGroup}>
					<AvatarGroup>
						{avatars.slice(0, 4).map((avatar, index) => {
							return (
								<Avatar key={index} size="md">
									<AvatarImage source={{ uri: avatar.src }} />
								</Avatar>
							);
						})}
						{remainingCount > 0 && (
							<Avatar size="md">
								<AvatarFallbackText>{"+ " + remainingCount}</AvatarFallbackText>
							</Avatar>
						)}
					</AvatarGroup>
					<Text style={styles.subTitleStyle} numberOfLines={1} bold>
						{itemsCount} items
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
	},
	pressedCard: {
        filter: "brightness(0.95)",
	},
	itemsGroup: {
		paddingStart: 10,
		flexDirection: "row",
		justifyContent: "space-between",
		alignItems: "flex-end",
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
