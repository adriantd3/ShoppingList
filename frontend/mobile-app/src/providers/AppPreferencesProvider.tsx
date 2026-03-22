import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  getLastActiveListId,
  getOnboardingCompleted,
  getPushPermissionStatus,
  setLastActiveListId,
  setOnboardingCompleted,
  setPushPermissionStatus,
} from "../services/storage/appStorage";

type AppPreferencesContextValue = {
  isHydrating: boolean;
  onboardingCompleted: boolean;
  pushPermissionStatus: string | null;
  lastActiveListId: string | null;
  completeOnboarding: () => Promise<void>;
  savePushPermissionStatus: (status: string) => Promise<void>;
  saveLastActiveListId: (listId: string) => Promise<void>;
};

const AppPreferencesContext = createContext<AppPreferencesContextValue | undefined>(undefined);

export const AppPreferencesProvider = ({ children }: { children: ReactNode }) => {
  const [isHydrating, setIsHydrating] = useState(true);
  const [onboardingCompleted, setOnboardingCompletedState] = useState(false);
  const [pushPermissionStatus, setPushPermissionStatusState] = useState<string | null>(null);
  const [lastActiveListId, setLastActiveListIdState] = useState<string | null>(null);

  useEffect(() => {
    const hydrate = async () => {
      const [savedOnboardingCompleted, savedPushStatus, savedLastActiveListId] =
        await Promise.all([
          getOnboardingCompleted(),
          getPushPermissionStatus(),
          getLastActiveListId(),
        ]);

      setOnboardingCompletedState(savedOnboardingCompleted);
      setPushPermissionStatusState(savedPushStatus);
      setLastActiveListIdState(savedLastActiveListId);
      setIsHydrating(false);
    };

    hydrate().catch(() => {
      setIsHydrating(false);
    });
  }, []);

  const completeOnboarding = useCallback(async () => {
    await setOnboardingCompleted(true);
    setOnboardingCompletedState(true);
  }, []);

  const savePushPermissionStatus = useCallback(async (status: string) => {
    await setPushPermissionStatus(status);
    setPushPermissionStatusState(status);
  }, []);

  const saveLastActiveListId = useCallback(async (listId: string) => {
    await setLastActiveListId(listId);
    setLastActiveListIdState(listId);
  }, []);

  const value = useMemo<AppPreferencesContextValue>(
    () => ({
      isHydrating,
      onboardingCompleted,
      pushPermissionStatus,
      lastActiveListId,
      completeOnboarding,
      savePushPermissionStatus,
      saveLastActiveListId,
    }),
    [
      completeOnboarding,
      isHydrating,
      lastActiveListId,
      onboardingCompleted,
      pushPermissionStatus,
      saveLastActiveListId,
      savePushPermissionStatus,
    ],
  );

  return <AppPreferencesContext.Provider value={value}>{children}</AppPreferencesContext.Provider>;
};

export const useAppPreferences = (): AppPreferencesContextValue => {
  const context = useContext(AppPreferencesContext);

  if (!context) {
    throw new Error("useAppPreferences must be used inside AppPreferencesProvider.");
  }

  return context;
};
