import { __testables } from "../../../src/services/lists/listsApi";

describe("task 11 share link mapping", () => {
  test("maps valid share-link payload including token", () => {
    const mapped = __testables.mapShareLink(
      {
        id: "share-1",
        list_id: "list-1",
        expires_at: "2026-03-22T20:00:00.000Z",
        revoked_at: null,
      },
      "join-token",
    );

    expect(mapped).toEqual({
      id: "share-1",
      listId: "list-1",
      token: "join-token",
      expiresAtIso: "2026-03-22T20:00:00.000Z",
      revokedAtIso: null,
    });
  });

  test("returns null when payload is missing required fields", () => {
    const mapped = __testables.mapShareLink({ id: "share-1" }, "join-token");
    expect(mapped).toBeNull();
  });
});
