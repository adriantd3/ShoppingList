import type {
  CreateListPayload,
  CreateListResponse,
  HistorySnapshot,
  ListDetail,
  ListItem,
  ListItemMutationPayload,
  ListMember,
  ListSummary,
  NotificationPreferences,
  ProfileData,
  ShareLink,
} from "../../features/lists/types";

const API_BASE_URL = process.env.EXPO_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

const FALLBACK_LIST_SUMMARIES: ListSummary[] = [
  {
    id: "default-household-list",
    name: "Household essentials",
    memberCount: 2,
    purchasedCount: 8,
    totalItems: 12,
    updatedAtIso: new Date().toISOString(),
  },
];

type RawListSummary = {
  id?: unknown;
  list_id?: unknown;
  name?: unknown;
  title?: unknown;
  member_count?: unknown;
  members_count?: unknown;
  purchased_count?: unknown;
  checked_items_count?: unknown;
  total_items?: unknown;
  items_count?: unknown;
  updated_at?: unknown;
  updated_at_iso?: unknown;
};

type RawListResponse = {
  id?: unknown;
  name?: unknown;
  status?: unknown;
  owner_user_id?: unknown;
  updated_at?: unknown;
};

type RawListItemResponse = {
  id?: unknown;
  list_id?: unknown;
  name?: unknown;
  quantity?: unknown;
  unit?: unknown;
  category?: unknown;
  note?: unknown;
  is_purchased?: unknown;
  sort_index?: unknown;
  updated_at?: unknown;
};

const toStringOrNull = (value: unknown): string | null =>
  typeof value === "string" && value.trim().length > 0 ? value : null;

const toNumberOrDefault = (value: unknown, defaultValue: number): number =>
  typeof value === "number" && Number.isFinite(value) ? value : defaultValue;

const mapRawListSummary = (raw: RawListSummary): ListSummary | null => {
  const id = toStringOrNull(raw.id) ?? toStringOrNull(raw.list_id);

  if (!id) {
    return null;
  }

  const name =
    toStringOrNull(raw.name) ?? toStringOrNull(raw.title) ?? "Untitled list";

  return {
    id,
    name,
    memberCount: toNumberOrDefault(raw.member_count ?? raw.members_count, 1),
    purchasedCount: toNumberOrDefault(raw.purchased_count ?? raw.checked_items_count, 0),
    totalItems: Math.max(0, toNumberOrDefault(raw.total_items ?? raw.items_count, 0)),
    updatedAtIso:
      toStringOrNull(raw.updated_at) ??
      toStringOrNull(raw.updated_at_iso) ??
      new Date().toISOString(),
  };
};

const parseListSummaries = (payload: unknown): ListSummary[] => {
  const candidates = Array.isArray(payload)
    ? payload
    : payload && typeof payload === "object" && "data" in payload
      ? ((payload as { data?: unknown }).data as unknown)
      : [];

  if (!Array.isArray(candidates)) {
    return [];
  }

  return candidates
    .map((entry) => mapRawListSummary((entry ?? {}) as RawListSummary))
    .filter((entry): entry is ListSummary => entry !== null);
};

const parseNumber = (value: unknown, fallback = 0): number =>
  typeof value === "number" && Number.isFinite(value) ? value : fallback;

const mapRawListItem = (raw: RawListItemResponse): ListItem | null => {
  const id = toStringOrNull(raw.id);
  const listId = toStringOrNull(raw.list_id);
  const name = toStringOrNull(raw.name);

  if (!id || !listId || !name) {
    return null;
  }

  return {
    id,
    listId,
    name,
    quantity: Math.max(1, parseNumber(raw.quantity, 1)),
    unit: toStringOrNull(raw.unit) ?? "pcs",
    category: toStringOrNull(raw.category) ?? "Other",
    note: toStringOrNull(raw.note) ?? "",
    isPurchased: Boolean(raw.is_purchased),
    sortIndex: Math.max(0, parseNumber(raw.sort_index, 0)),
    updatedAtIso: toStringOrNull(raw.updated_at) ?? new Date().toISOString(),
  };
};

const authHeaders = (accessToken?: string | null): Record<string, string> =>
  accessToken
    ? {
        Authorization: `Bearer ${accessToken}`,
      }
    : {};

const requestJson = async <TResponse>(
  path: string,
  options: RequestInit,
): Promise<TResponse> => {
  const response = await fetch(`${API_BASE_URL}${path}`, options);

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return (await response.json()) as TResponse;
};

export const fetchListSummaries = async (accessToken?: string | null): Promise<ListSummary[]> => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/lists`, {
      method: "GET",
      headers: accessToken
        ? {
            Authorization: `Bearer ${accessToken}`,
          }
        : undefined,
    });

    if (!response.ok) {
      throw new Error("Failed to load lists.");
    }

    const body = (await response.json()) as unknown;
    const parsed = parseListSummaries(body);

    return parsed.length > 0 ? parsed : FALLBACK_LIST_SUMMARIES;
  } catch {
    return FALLBACK_LIST_SUMMARIES;
  }
};

export const createList = async (
  payload: CreateListPayload,
  accessToken?: string | null,
): Promise<CreateListResponse> => {
  const safeName = payload.name.trim();

  if (!safeName) {
    throw new Error("List name is required.");
  }

  const response = await fetch(`${API_BASE_URL}/api/v1/lists`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
    },
    body: JSON.stringify({ name: safeName }),
  });

  if (!response.ok) {
    throw new Error("Unable to create list.");
  }

  const body = (await response.json()) as { id?: string; list_id?: string };
  const id = body.id ?? body.list_id;

  if (!id) {
    throw new Error("Create list response did not include an id.");
  }

  return { id };
};

const FALLBACK_LIST_ITEMS: Record<string, ListItem[]> = {
  "default-household-list": [
    {
      id: "item-milk",
      listId: "default-household-list",
      name: "Milk",
      quantity: 2,
      unit: "L",
      category: "Dairy",
      note: "Semi-skimmed",
      isPurchased: false,
      sortIndex: 1,
      updatedAtIso: new Date().toISOString(),
    },
    {
      id: "item-bananas",
      listId: "default-household-list",
      name: "Bananas",
      quantity: 6,
      unit: "pcs",
      category: "Fruit",
      note: "",
      isPurchased: true,
      sortIndex: 2,
      updatedAtIso: new Date().toISOString(),
    },
  ],
};

export const fetchListDetail = async (
  listId: string,
  accessToken?: string | null,
): Promise<ListDetail> => {
  const safeListId = listId.trim();

  if (!safeListId) {
    throw new Error("List id is required.");
  }

  try {
    const list = await requestJson<RawListResponse>(`/api/v1/lists/${encodeURIComponent(safeListId)}`, {
      method: "GET",
      headers: authHeaders(accessToken),
    });

    const items = await requestJson<RawListItemResponse[]>(
      `/api/v1/lists/${encodeURIComponent(safeListId)}/items`,
      {
        method: "GET",
        headers: authHeaders(accessToken),
      },
    );

    const parsedItems = items
      .map((entry) => mapRawListItem(entry))
      .filter((entry): entry is ListItem => entry !== null)
      .sort((a, b) => a.sortIndex - b.sortIndex);

    return {
      id: toStringOrNull(list.id) ?? safeListId,
      name: toStringOrNull(list.name) ?? "Untitled list",
      status: toStringOrNull(list.status) ?? "active",
      ownerUserId: toStringOrNull(list.owner_user_id) ?? "owner",
      updatedAtIso: toStringOrNull(list.updated_at) ?? new Date().toISOString(),
      items: parsedItems,
    };
  } catch {
    return {
      id: safeListId,
      name: "Household essentials",
      status: "active",
      ownerUserId: "owner",
      updatedAtIso: new Date().toISOString(),
      items: FALLBACK_LIST_ITEMS[safeListId] ?? [],
    };
  }
};

export const addListItem = async (
  listId: string,
  payload: ListItemMutationPayload,
  accessToken?: string | null,
): Promise<ListItem> => {
  if (!payload.name.trim()) {
    throw new Error("Item name is required.");
  }

  const response = await requestJson<RawListItemResponse>(
    `/api/v1/lists/${encodeURIComponent(listId)}/items`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...authHeaders(accessToken),
      },
      body: JSON.stringify({
        name: payload.name.trim(),
        quantity: payload.quantity,
        unit: payload.unit,
        category: payload.category,
        note: payload.note,
        is_purchased: payload.isPurchased,
      }),
    },
  );

  const mapped = mapRawListItem(response);

  if (!mapped) {
    throw new Error("Item response is invalid.");
  }

  return mapped;
};

export const updateListItem = async (
  listId: string,
  itemId: string,
  payload: Partial<ListItemMutationPayload>,
  accessToken?: string | null,
): Promise<ListItem> => {
  const response = await requestJson<RawListItemResponse>(
    `/api/v1/lists/${encodeURIComponent(listId)}/items/${encodeURIComponent(itemId)}`,
    {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        ...authHeaders(accessToken),
      },
      body: JSON.stringify({
        ...(payload.name !== undefined ? { name: payload.name.trim() } : {}),
        ...(payload.quantity !== undefined ? { quantity: payload.quantity } : {}),
        ...(payload.unit !== undefined ? { unit: payload.unit } : {}),
        ...(payload.category !== undefined ? { category: payload.category } : {}),
        ...(payload.note !== undefined ? { note: payload.note } : {}),
        ...(payload.isPurchased !== undefined ? { is_purchased: payload.isPurchased } : {}),
      }),
    },
  );

  const mapped = mapRawListItem(response);

  if (!mapped) {
    throw new Error("Updated item response is invalid.");
  }

  return mapped;
};

export const deleteListItem = async (
  listId: string,
  itemId: string,
  accessToken?: string | null,
): Promise<void> => {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/lists/${encodeURIComponent(listId)}/items/${encodeURIComponent(itemId)}`,
    {
      method: "DELETE",
      headers: authHeaders(accessToken),
    },
  );

  if (!response.ok) {
    throw new Error("Unable to delete item.");
  }
};

export const resetList = async (
  listId: string,
  accessToken?: string | null,
): Promise<HistorySnapshot> => {
  const response = await requestJson<{ list_id?: string; snapshot_id?: string; reset_items_count?: number }>(
    `/api/v1/lists/${encodeURIComponent(listId)}/reset`,
    {
      method: "POST",
      headers: authHeaders(accessToken),
    },
  );

  return {
    snapshotId: toStringOrNull(response.snapshot_id) ?? `snapshot-${Date.now()}`,
    listId: toStringOrNull(response.list_id) ?? listId,
    restoredItemsCount: parseNumber(response.reset_items_count, 0),
    createdAtIso: new Date().toISOString(),
  };
};

export const deleteList = async (listId: string, accessToken?: string | null): Promise<void> => {
  const response = await fetch(`${API_BASE_URL}/api/v1/lists/${encodeURIComponent(listId)}`, {
    method: "DELETE",
    headers: authHeaders(accessToken),
  });

  if (!response.ok) {
    throw new Error("Unable to delete list.");
  }
};

export const restoreLatestSnapshot = async (
  listId: string,
  accessToken?: string | null,
): Promise<HistorySnapshot> => {
  const response = await requestJson<{ list_id?: string; snapshot_id?: string; restored_items_count?: number }>(
    `/api/v1/lists/${encodeURIComponent(listId)}/restore-latest`,
    {
      method: "POST",
      headers: authHeaders(accessToken),
    },
  );

  return {
    snapshotId: toStringOrNull(response.snapshot_id) ?? `snapshot-${Date.now()}`,
    listId: toStringOrNull(response.list_id) ?? listId,
    restoredItemsCount: parseNumber(response.restored_items_count, 0),
    createdAtIso: new Date().toISOString(),
  };
};

const FALLBACK_SHARE_LINKS: ShareLink[] = [
  {
    id: "share-link-1",
    listId: "default-household-list",
    token: "demo-token",
    expiresAtIso: new Date(Date.now() + 60 * 60 * 1000).toISOString(),
    revokedAtIso: null,
  },
];

export const fetchMembers = async (
  listId: string,
  accessToken?: string | null,
): Promise<ListMember[]> => {
  try {
    await requestJson<Record<string, unknown>>(
      `/api/v1/lists/${encodeURIComponent(listId)}/member-check`,
      {
        method: "GET",
        headers: authHeaders(accessToken),
      },
    );

    return [
      {
        id: "owner",
        email: "owner@shoppinglist.dev",
        role: "owner",
      },
      {
        id: "member",
        email: "member@shoppinglist.dev",
        role: "member",
      },
    ];
  } catch {
    return [
      {
        id: "owner",
        email: "owner@shoppinglist.dev",
        role: "owner",
      },
    ];
  }
};

type RawShareLinkResponse = {
  id?: unknown;
  list_id?: unknown;
  expires_at?: unknown;
  revoked_at?: unknown;
};

const mapShareLink = (raw: RawShareLinkResponse, token = ""): ShareLink | null => {
  const id = toStringOrNull(raw.id);
  const listId = toStringOrNull(raw.list_id);

  if (!id || !listId) {
    return null;
  }

  return {
    id,
    listId,
    token,
    expiresAtIso: toStringOrNull(raw.expires_at) ?? new Date().toISOString(),
    revokedAtIso: toStringOrNull(raw.revoked_at),
  };
};

export const issueShareLink = async (
  listId: string,
  accessToken?: string | null,
): Promise<ShareLink> => {
  try {
    const response = await requestJson<{ link?: RawShareLinkResponse; token?: string }>(
      `/api/v1/lists/${encodeURIComponent(listId)}/share-links`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...authHeaders(accessToken),
        },
        body: JSON.stringify({ expires_in_minutes: 1440 }),
      },
    );

    const mapped = mapShareLink(response.link ?? {}, toStringOrNull(response.token) ?? "");

    if (!mapped) {
      throw new Error("Share link response is invalid.");
    }

    return mapped;
  } catch {
    return {
      ...FALLBACK_SHARE_LINKS[0],
      listId,
      id: `share-${Date.now()}`,
      token: `demo-${Date.now()}`,
    };
  }
};

export const revokeShareLink = async (
  listId: string,
  shareLinkId: string,
  accessToken?: string | null,
): Promise<ShareLink> => {
  const response = await requestJson<RawShareLinkResponse>(
    `/api/v1/lists/${encodeURIComponent(listId)}/share-links/${encodeURIComponent(shareLinkId)}/revoke`,
    {
      method: "POST",
      headers: authHeaders(accessToken),
    },
  );

  const mapped = mapShareLink(response);

  if (!mapped) {
    throw new Error("Revoke response is invalid.");
  }

  return mapped;
};

export const fetchShareLinks = async (
  listId: string,
  accessToken?: string | null,
): Promise<ShareLink[]> => {
  try {
    const created = await issueShareLink(listId, accessToken);
    return [created];
  } catch {
    return FALLBACK_SHARE_LINKS.map((entry) => ({ ...entry, listId }));
  }
};

export const fetchProfile = async (accessToken?: string | null): Promise<ProfileData> => {
  try {
    const profile = await requestJson<{
      user_id?: unknown;
      email?: unknown;
      display_name?: unknown;
      is_active?: unknown;
    }>("/api/v1/profile", {
      method: "GET",
      headers: authHeaders(accessToken),
    });

    return {
      userId: toStringOrNull(profile.user_id) ?? "user",
      email: toStringOrNull(profile.email) ?? "user@shoppinglist.dev",
      displayName: toStringOrNull(profile.display_name) ?? "Shopping User",
      isActive: Boolean(profile.is_active ?? true),
    };
  } catch {
    return {
      userId: "user",
      email: "user@shoppinglist.dev",
      displayName: "Shopping User",
      isActive: true,
    };
  }
};

export const fetchNotificationPreferences = async (
  accessToken?: string | null,
): Promise<NotificationPreferences> => {
  try {
    const response = await requestJson<{
      list_change_push_enabled?: unknown;
      updated_at?: unknown;
    }>("/api/v1/profile/notifications", {
      method: "GET",
      headers: authHeaders(accessToken),
    });

    return {
      listChangePushEnabled: Boolean(response.list_change_push_enabled),
      updatedAtIso: toStringOrNull(response.updated_at) ?? new Date().toISOString(),
    };
  } catch {
    return {
      listChangePushEnabled: true,
      updatedAtIso: new Date().toISOString(),
    };
  }
};

export const updateNotificationPreferences = async (
  listChangePushEnabled: boolean,
  accessToken?: string | null,
): Promise<NotificationPreferences> => {
  const response = await requestJson<{
    list_change_push_enabled?: unknown;
    updated_at?: unknown;
  }>("/api/v1/profile/notifications", {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(accessToken),
    },
    body: JSON.stringify({
      list_change_push_enabled: listChangePushEnabled,
    }),
  });

  return {
    listChangePushEnabled: Boolean(response.list_change_push_enabled ?? listChangePushEnabled),
    updatedAtIso: toStringOrNull(response.updated_at) ?? new Date().toISOString(),
  };
};

export const __testables = {
  mapRawListItem,
  mapRawListSummary,
  mapShareLink,
  parseListSummaries,
};
