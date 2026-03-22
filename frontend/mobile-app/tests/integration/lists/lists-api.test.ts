import {
  addListItem,
  createList,
  fetchListDetail,
  fetchListSummaries,
  fetchNotificationPreferences,
  fetchProfile,
  fetchShareLinks,
  restoreLatestSnapshot,
  updateListItem,
} from "../../../src/services/lists/listsApi";

describe("lists api", () => {
  const originalFetch = globalThis.fetch;

  afterEach(() => {
    globalThis.fetch = originalFetch;
    jest.clearAllMocks();
  });

  test("maps API response list summaries", async () => {
    globalThis.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        data: [
          {
            id: "list-123",
            name: "Weekly groceries",
            member_count: 4,
            purchased_count: 2,
            total_items: 10,
            updated_at: "2026-03-22T08:00:00.000Z",
          },
        ],
      }),
    }) as unknown as typeof fetch;

    const summaries = await fetchListSummaries("token");

    expect(summaries).toHaveLength(1);
    expect(summaries[0]).toMatchObject({
      id: "list-123",
      name: "Weekly groceries",
      memberCount: 4,
      purchasedCount: 2,
      totalItems: 10,
    });
  });

  test("returns fallback summary when API call fails", async () => {
    globalThis.fetch = jest.fn().mockRejectedValue(new Error("network")) as unknown as typeof fetch;

    const summaries = await fetchListSummaries("token");

    expect(summaries).toHaveLength(1);
    expect(summaries[0].id).toBe("default-household-list");
  });

  test("creates list and returns created id", async () => {
    globalThis.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ id: "new-list" }),
    }) as unknown as typeof fetch;

    const result = await createList({ name: "Family list" }, "token");

    expect(result.id).toBe("new-list");
    expect(globalThis.fetch).toHaveBeenCalledTimes(1);
  });

  test("rejects blank list names", async () => {
    await expect(createList({ name: "   " }, "token")).rejects.toThrow("List name is required.");
  });

  test("loads list detail and grouped item fields", async () => {
    globalThis.fetch = jest
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: "list-1",
          name: "Family",
          status: "active",
          owner_user_id: "owner",
          updated_at: "2026-03-22T12:00:00.000Z",
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => [
          {
            id: "item-1",
            list_id: "list-1",
            name: "Milk",
            quantity: 1,
            unit: "L",
            category: "Dairy",
            note: "",
            is_purchased: false,
            sort_index: 1,
            updated_at: "2026-03-22T12:01:00.000Z",
          },
        ],
      }) as unknown as typeof fetch;

    const detail = await fetchListDetail("list-1", "token");

    expect(detail.id).toBe("list-1");
    expect(detail.items).toHaveLength(1);
    expect(detail.items[0].name).toBe("Milk");
  });

  test("falls back to default detail when backend fails", async () => {
    globalThis.fetch = jest.fn().mockRejectedValue(new Error("network")) as unknown as typeof fetch;

    const detail = await fetchListDetail("default-household-list", "token");

    expect(detail.id).toBe("default-household-list");
    expect(detail.items.length).toBeGreaterThan(0);
  });

  test("adds and updates items", async () => {
    globalThis.fetch = jest
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: "item-2",
          list_id: "list-1",
          name: "Bread",
          quantity: 1,
          unit: "pcs",
          category: "Bakery",
          note: "",
          is_purchased: false,
          sort_index: 2,
          updated_at: "2026-03-22T12:04:00.000Z",
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: "item-2",
          list_id: "list-1",
          name: "Bread",
          quantity: 2,
          unit: "pcs",
          category: "Bakery",
          note: "",
          is_purchased: true,
          sort_index: 2,
          updated_at: "2026-03-22T12:05:00.000Z",
        }),
      }) as unknown as typeof fetch;

    const created = await addListItem(
      "list-1",
      {
        name: "Bread",
        quantity: 1,
        unit: "pcs",
        category: "Bakery",
        note: "",
        isPurchased: false,
      },
      "token",
    );

    const updated = await updateListItem("list-1", created.id, { isPurchased: true, quantity: 2 }, "token");

    expect(created.id).toBe("item-2");
    expect(updated.isPurchased).toBe(true);
    expect(updated.quantity).toBe(2);
  });

  test("restores latest snapshot", async () => {
    globalThis.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        list_id: "list-1",
        snapshot_id: "snapshot-1",
        restored_items_count: 4,
      }),
    }) as unknown as typeof fetch;

    const snapshot = await restoreLatestSnapshot("list-1", "token");

    expect(snapshot.snapshotId).toBe("snapshot-1");
    expect(snapshot.restoredItemsCount).toBe(4);
  });

  test("fetches profile and notification preferences", async () => {
    globalThis.fetch = jest
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          user_id: "user-1",
          email: "user@shoppinglist.dev",
          display_name: "Test User",
          is_active: true,
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          list_change_push_enabled: true,
          updated_at: "2026-03-22T12:06:00.000Z",
        }),
      }) as unknown as typeof fetch;

    const profile = await fetchProfile("token");
    const preferences = await fetchNotificationPreferences("token");

    expect(profile.displayName).toBe("Test User");
    expect(preferences.listChangePushEnabled).toBe(true);
  });

  test("fetches share links list", async () => {
    globalThis.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        link: {
          id: "share-1",
          list_id: "list-1",
          expires_at: "2026-03-22T20:00:00.000Z",
          revoked_at: null,
        },
        token: "share-token",
      }),
    }) as unknown as typeof fetch;

    const links = await fetchShareLinks("list-1", "token");

    expect(links).toHaveLength(1);
    expect(links[0].token).toBe("share-token");
  });
});
