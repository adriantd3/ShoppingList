import { useMemo, useState } from "react";
import { useLocalSearchParams, useRouter } from "expo-router";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Button, Paragraph, Spinner, Text, YStack } from "tamagui";

import { useAuthSession } from "../../../src/providers/AuthSessionProvider";
import { useConnectivity } from "../../../src/providers/ConnectivityProvider";
import {
  addListItem,
  deleteList,
  deleteListItem,
  fetchListDetail,
  resetList,
  updateListItem,
} from "../../../src/services/lists/listsApi";
import { getDangerCopy, groupItemsByCategory, type DangerAction } from "../../../src/features/lists/activeListLogic";
import { DangerConfirmDialog } from "../../../src/ui/DangerConfirmDialog";
import { EmptyStatePanel } from "../../../src/ui/EmptyStatePanel";
import { ErrorStatePanel } from "../../../src/ui/ErrorStatePanel";
import { InlineAddBar } from "../../../src/ui/InlineAddBar";
import { ItemRow } from "../../../src/ui/ItemRow";
import { OfflineBanner } from "../../../src/ui/OfflineBanner";
import { ScreenContainer } from "../../../src/ui/ScreenContainer";

export default function ActiveListScreen() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const params = useLocalSearchParams<{ listId: string }>();
  const { accessToken } = useAuthSession();
  const { isOnline } = useConnectivity();
  const [pendingOfflineMutations, setPendingOfflineMutations] = useState(0);
  const [dangerAction, setDangerAction] = useState<DangerAction>(null);
  const [isConfirming, setIsConfirming] = useState(false);

  const listId = params.listId ?? "";

  const {
    data,
    isLoading,
    isError,
    refetch,
  } = useQuery({
    queryKey: ["lists", "detail", listId],
    queryFn: () => fetchListDetail(listId, accessToken),
    enabled: Boolean(listId),
  });

  const groupedItems = useMemo(() => {
    if (!data) {
      return [];
    }

    return groupItemsByCategory(data.items);
  }, [data]);

  const enqueueOfflineMutation = () => {
    setPendingOfflineMutations((value) => value + 1);
  };

  const safeRefresh = async () => {
    await queryClient.invalidateQueries({ queryKey: ["lists", "detail", listId] });
  };

  const addInline = async (name: string) => {
    if (!isOnline) {
      enqueueOfflineMutation();
      return;
    }

    await addListItem(
      listId,
      {
        name,
        quantity: 1,
        unit: "pcs",
        category: "Other",
        note: "",
        isPurchased: false,
      },
      accessToken,
    );

    await safeRefresh();
  };

  const togglePurchased = async (itemId: string, nextState: boolean) => {
    if (!isOnline) {
      enqueueOfflineMutation();
      return;
    }

    await updateListItem(listId, itemId, { isPurchased: nextState }, accessToken);
    await safeRefresh();
  };

  const openItemEditor = (itemId: string) => {
    const item = data?.items.find((entry) => entry.id === itemId);

    if (!item) {
      return;
    }

    router.push({
      pathname: "/modal/item-editor",
      params: {
        listId,
        itemId,
        name: item.name,
        quantity: String(item.quantity),
        unit: item.unit,
        category: item.category,
        note: item.note,
      },
    });
  };

  const openDeleteItemConfirm = (itemId: string) => {
    setDangerAction({ itemId });
  };

  const confirmDangerAction = async () => {
    setIsConfirming(true);

    try {
      if (dangerAction === "reset-list") {
        await resetList(listId, accessToken);
        await safeRefresh();
      } else if (dangerAction === "delete-list") {
        await deleteList(listId, accessToken);
        router.replace("/(tabs)/lists");
      } else if (dangerAction && "itemId" in dangerAction) {
        await deleteListItem(listId, dangerAction.itemId, accessToken);
        await safeRefresh();
      }
    } finally {
      setIsConfirming(false);
      setDangerAction(null);
    }
  };

  const dangerCopy = getDangerCopy(dangerAction);


  if (isLoading) {
    return (
      <ScreenContainer>
        <YStack alignItems="center" paddingVertical="$6">
          <Spinner size="large" color="$primary" />
        </YStack>
      </ScreenContainer>
    );
  }

  if (isError || !data) {
    return (
      <ScreenContainer>
        <ErrorStatePanel
          title="Unable to load list"
          message="Try again in a moment."
          onRetry={() => {
            void refetch();
          }}
        />
      </ScreenContainer>
    );
  }

  return (
    <ScreenContainer>
      <YStack gap="$3">
        <Text fontSize={24} fontWeight="700">
          {data.name}
        </Text>
        <Paragraph color="$muted">Primary actions stay within two taps: check, quick-add, and edit.</Paragraph>

        {!isOnline ? <OfflineBanner pendingCount={pendingOfflineMutations} /> : null}

        <YStack gap="$2">
          <InlineAddBar onAdd={addInline} />
        </YStack>

        <YStack gap="$2">
          <Button accessibilityLabel="Open members" onPress={() => router.push({ pathname: "/(tabs)/lists/members", params: { listId } })}>
            Members
          </Button>
          <Button accessibilityLabel="Open share screen" onPress={() => router.push({ pathname: "/(tabs)/lists/share", params: { listId } })}>
            Share
          </Button>
          <Button accessibilityLabel="Open history screen" onPress={() => router.push({ pathname: "/(tabs)/lists/history", params: { listId } })}>
            History
          </Button>
          <Button
            accessibilityLabel="Reset list"
            backgroundColor="$danger"
            onPress={() => setDangerAction("reset-list")}
          >
            Reset list
          </Button>
          <Button
            accessibilityLabel="Delete list"
            backgroundColor="$danger"
            onPress={() => setDangerAction("delete-list")}
          >
            Delete list
          </Button>
        </YStack>

        {groupedItems.length === 0 ? (
          <EmptyStatePanel title="No items yet" description="Use quick-add above to add your first item." />
        ) : (
          <YStack gap="$3">
            {groupedItems.map(([category, items]) => (
              <YStack key={category} gap="$2">
                <Text fontSize={18} fontWeight="700">
                  {category}
                </Text>
                <YStack gap="$2">
                  {items.map((item) => (
                    <ItemRow
                      key={item.id}
                      item={item}
                      onTogglePurchased={togglePurchased}
                      onEdit={openItemEditor}
                      onDelete={openDeleteItemConfirm}
                    />
                  ))}
                </YStack>
              </YStack>
            ))}
          </YStack>
        )}

        <DangerConfirmDialog
          title={dangerCopy.title}
          message={dangerCopy.message}
          isVisible={dangerAction !== null}
          confirmLabel={dangerCopy.confirmLabel}
          isLoading={isConfirming}
          onConfirm={confirmDangerAction}
          onCancel={() => setDangerAction(null)}
        />
      </YStack>
    </ScreenContainer>
  );
}
