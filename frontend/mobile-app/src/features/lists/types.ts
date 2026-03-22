export type ListSummary = {
  id: string;
  name: string;
  memberCount: number;
  purchasedCount: number;
  totalItems: number;
  updatedAtIso: string;
};

export type CreateListPayload = {
  name: string;
};

export type CreateListResponse = {
  id: string;
};

export type ListItem = {
  id: string;
  listId: string;
  name: string;
  quantity: number;
  unit: string;
  category: string;
  note: string;
  isPurchased: boolean;
  sortIndex: number;
  updatedAtIso: string;
};

export type ListDetail = {
  id: string;
  name: string;
  status: string;
  ownerUserId: string;
  updatedAtIso: string;
  items: ListItem[];
};

export type ListItemMutationPayload = {
  name: string;
  quantity: number;
  unit: string;
  category: string;
  note: string;
  isPurchased: boolean;
};

export type ShareLink = {
  id: string;
  listId: string;
  token: string;
  expiresAtIso: string;
  revokedAtIso: string | null;
};

export type ListMember = {
  id: string;
  email: string;
  role: "owner" | "member";
};

export type ProfileData = {
  userId: string;
  email: string;
  displayName: string;
  isActive: boolean;
};

export type NotificationPreferences = {
  listChangePushEnabled: boolean;
  updatedAtIso: string;
};

export type HistorySnapshot = {
  snapshotId: string;
  listId: string;
  restoredItemsCount: number;
  createdAtIso: string;
};
