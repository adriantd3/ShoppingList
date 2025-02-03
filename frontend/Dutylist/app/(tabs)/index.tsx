import { Link } from "expo-router";
import { useState, useCallback, useMemo, useRef } from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { Button, ButtonText } from "@/components/ui/button";
import { Heading } from "@/components/ui/heading";
import { EditIcon, TrashIcon, ShareIcon } from "@/components/ui/icon";
import {
	Actionsheet,
	ActionsheetContent,
	ActionsheetItem,
	ActionsheetItemText,
	ActionsheetDragIndicator,
	ActionsheetDragIndicatorWrapper,
	ActionsheetBackdrop,
	ActionsheetIcon,
} from "@/components/ui/actionsheet";
import { List } from "@/components/lists/types/List.types";
import { FlashList } from "@shopify/flash-list";
import { GestureHandlerRootView } from "react-native-gesture-handler";
import {
	BottomSheetModal,
	BottomSheetView,
	BottomSheetModalProvider,
	BottomSheetBackdrop,
} from "@gorhom/bottom-sheet";

import ListCard from "@/components/lists/list-card";

const HomePage = () => {
	const insets = useSafeAreaInsets();
	const [selectedList, setSelectedList] = useState<List | null>(null);
	const [showActionsheet, setShowActionsheet] = useState(false);

	const snapPoints = useMemo(() => [30], []);

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

	const renameList = () => {
		console.log("List renamed");
	}

	const shareList = () => {
		console.log("List shared");
	}

	const deleteList = () => {
		console.log("List deleted");
	}	

	const openOptionsModal = (list: List) => {
		setSelectedList(list);
		setShowActionsheet(true);
	};

	const handleDismiss = useCallback(() => {
		setSelectedList(null);
		setShowActionsheet(false);
	}, []);

	const styles = StyleSheet.create({
		container: {
			flex: 1,
			paddingTop: insets.top + 10,
			paddingLeft: 24,
			paddingRight: 24,
			paddingBottom: insets.bottom,
			justifyContent: "flex-start",
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
		<View style={styles.container} className="bg-background-50">
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
			<Actionsheet
				isOpen={showActionsheet}
				onClose={handleDismiss}
				snapPoints={snapPoints}
			>
				<ActionsheetBackdrop />
				<ActionsheetContent>
					<ActionsheetDragIndicatorWrapper>
						<ActionsheetDragIndicator />
					</ActionsheetDragIndicatorWrapper>
					<ActionsheetItem onPress={renameList}>
						<ActionsheetIcon as={EditIcon} size="lg" />
						<ActionsheetItemText>Rename list</ActionsheetItemText>
					</ActionsheetItem>
					<ActionsheetItem onPress={shareList}>
						<ActionsheetIcon as={ShareIcon} size="lg" />
						<ActionsheetItemText>Share list</ActionsheetItemText>
					</ActionsheetItem>
					<ActionsheetItem onPress={deleteList}>
						<ActionsheetIcon as={TrashIcon} size="lg" />
						<ActionsheetItemText>Delete list</ActionsheetItemText>
					</ActionsheetItem>
				</ActionsheetContent>
			</Actionsheet>
		</View>
	);
};

export default HomePage;
