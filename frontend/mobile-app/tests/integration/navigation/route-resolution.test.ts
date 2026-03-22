import { getAuthenticatedEntryRoute, resolveEntryRedirect } from "../../../src/navigation/routeResolution";

describe("route resolution", () => {
  test("routes first launch users to onboarding", () => {
    const redirect = resolveEntryRedirect({
      isHydrating: false,
      onboardingCompleted: false,
      isAuthenticated: false,
      currentSegment: undefined,
      lastActiveListId: null,
    });

    expect(redirect).toBe("/onboarding");
  });

  test("routes unauthenticated users to login when onboarding is complete", () => {
    const redirect = resolveEntryRedirect({
      isHydrating: false,
      onboardingCompleted: true,
      isAuthenticated: false,
      currentSegment: "(tabs)",
      lastActiveListId: null,
    });

    expect(redirect).toBe("/(auth)/login");
  });

  test("routes authenticated users to last active list when available", () => {
    const redirect = resolveEntryRedirect({
      isHydrating: false,
      onboardingCompleted: true,
      isAuthenticated: true,
      currentSegment: "(auth)",
      lastActiveListId: "family-list",
    });

    expect(redirect).toBe("/(tabs)/lists/family-list");
  });

  test("falls back to list collection when last active list does not exist", () => {
    const redirect = resolveEntryRedirect({
      isHydrating: false,
      onboardingCompleted: true,
      isAuthenticated: true,
      currentSegment: "(auth)",
      lastActiveListId: null,
    });

    expect(redirect).toBe("/(tabs)/lists");
  });

  test("keeps authenticated users in tabs without redirect loops", () => {
    const redirect = resolveEntryRedirect({
      isHydrating: false,
      onboardingCompleted: true,
      isAuthenticated: true,
      currentSegment: "(tabs)",
      lastActiveListId: "family-list",
    });

    expect(redirect).toBeNull();
  });

  test("encodes list ids in authenticated entry route", () => {
    const route = getAuthenticatedEntryRoute("family list");
    expect(route).toBe("/(tabs)/lists/family%20list");
  });
});
