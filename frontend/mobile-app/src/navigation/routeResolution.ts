type RouteInput = {
  isHydrating: boolean;
  onboardingCompleted: boolean;
  isAuthenticated: boolean;
  currentSegment: string | undefined;
  lastActiveListId: string | null;
};

export const getAuthenticatedEntryRoute = (lastActiveListId: string | null): string => {
  if (lastActiveListId) {
    return `/(tabs)/lists/${encodeURIComponent(lastActiveListId)}`;
  }

  return "/(tabs)/lists";
};

export const resolveEntryRedirect = ({
  isHydrating,
  onboardingCompleted,
  isAuthenticated,
  currentSegment,
  lastActiveListId,
}: RouteInput): string | null => {
  if (isHydrating) {
    return null;
  }

  if (!onboardingCompleted) {
    return currentSegment === "onboarding" ? null : "/onboarding";
  }

  if (!isAuthenticated) {
    return currentSegment === "(auth)" ? null : "/(auth)/login";
  }

  if (currentSegment === "(tabs)") {
    return null;
  }

  return getAuthenticatedEntryRoute(lastActiveListId);
};
