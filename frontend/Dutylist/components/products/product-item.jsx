import { View, StyleSheet, Image, Pressable, Animated } from "react-native";
import { Text } from "@/components/ui/text";
import { useRef } from "react";
import { onPressInCard, onPressOutCard } from "@/components/utils/animations";

const ProductItem = (product) => {
	const scaleValue = useRef(new Animated.Value(1)).current;

	return (
		<Pressable
			onPressIn={() => {
				onPressInCard(scaleValue);
			}}
			onPressOut={() => {
				onPressOutCard(scaleValue);
			}}
		>
			<Animated.View
				style={[style.cardShape, { transform: [{ scale: scaleValue }] }]}
			>
				<Image
					style={style.image}
					source={{
						uri: "https://i.pinimg.com/236x/34/22/2a/34222a8f0d41c9158729fe194a789268.jpg",
					}}
                    alt="Product"
				/>
                <Text size="lg" numberOfLines={2} style={style.text}>
                    Heinz's Ketchup
                </Text>
			</Animated.View>
		</Pressable>
	);
};

const style = StyleSheet.create({
	cardShape: {
		flexDirection: "column",
		justifyContent: "center",
        alignItems: "center",
        width: 130,
	},
	image: {
		height: 100,
		width: 100,
		borderRadius: 10,
	},
    text: {
        textAlign: "center",
    },
});

export default ProductItem;
