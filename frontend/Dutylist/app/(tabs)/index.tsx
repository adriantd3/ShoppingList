import { Link } from "expo-router";
import { useState, useCallback, useMemo, useRef } from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Button, ButtonText } from "@/components/ui/button";
import { Heading } from "@/components/ui/heading";
import { List } from "@/components/lists/types/List.types";
import { FlashList } from "@shopify/flash-list";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import {
	BottomSheetModal,
	BottomSheetView,
	BottomSheetModalProvider,
	BottomSheetBackdrop
} from "@gorhom/bottom-sheet";

import ListCard from "@/components/lists/list-card";
import ListItemCard from "@/components/lists/list-item-card";
import ProductItem from "@/components/products/product-item";

const HomePage = () => {
	const insets = useSafeAreaInsets();
	const [selectedList, setSelectedList] = useState<List | null>(null);
	const bottomSheetModalRef = useRef<BottomSheetModal>(null);

	const initialLists: List[] = Array.from({ length: 20 }, (_, i) => ({
		id: (i + 1).toString(),
		name: `List ${i + 1}`,
		n_items: Math.floor(Math.random() * 20) + 1,
		avatars: [
			"https://i.pinimg.com/236x/34/22/2a/34222a8f0d41c9158729fe194a789268.jpg",
			"https://static1.personality-database.com/profile_images/02779f99c78745ceb5f3216b666328aa.png",
		],
		style: "default",
	}));

	const openOptionsModal = (list: List) => {
		setSelectedList(list);
		bottomSheetModalRef.current?.present();
	};

	const snapPoints = useMemo(() => ['40%'], []);

    const handleDismiss = useCallback(() => {
        setSelectedList(null);
    }, []);

	const styles = StyleSheet.create({
		container: {
			flex: 1,
			paddingTop: insets.top + 10,
			paddingLeft: 24,
			paddingRight: 24,
			paddingBottom: insets.bottom,
			justifyContent: "flex-start",
			backgroundColor: "#fff",
		},
		header: {
			paddingBottom: 15,
		},
		modal: {
			flex: 1,
			alignItems: "center",
		},
	});

	return (
		<GestureHandlerRootView style={styles.container}>
			<BottomSheetModalProvider>
				<FlashList
					ListHeaderComponent={
						<Heading size="3xl" style={styles.header}>
							My shopping lists
						</Heading>
					}
					data={initialLists}
					renderItem={({ item }) => (
						<ListCard
							list={item}
							manageOptions={() => {
								openOptionsModal(item);
							}}
						/>
					)}
					estimatedItemSize={10}
					keyExtractor={(item) => item.id}
				/>
				<BottomSheetModal
                    ref={bottomSheetModalRef}
                    stackBehavior="push"
                    snapPoints={snapPoints}
                    backdropComponent={props => (
                        <BottomSheetBackdrop
                            {...props}
                            disappearsOnIndex={-1}
                            appearsOnIndex={0}
                            pressBehavior="close"
                        />
                    )}
                    onDismiss={handleDismiss}
                >
                    <BottomSheetView style={styles.modal}>
                        <Text>{selectedList?.name}</Text>
                    </BottomSheetView>
                </BottomSheetModal>
			</BottomSheetModalProvider>
		</GestureHandlerRootView>
	);
};

export default HomePage;
