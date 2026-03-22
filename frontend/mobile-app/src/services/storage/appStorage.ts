import AsyncStorage from "@react-native-async-storage/async-storage";

const ONBOARDING_COMPLETED_KEY = "preferences:onboardingCompleted";
const PUSH_PERMISSION_STATUS_KEY = "preferences:pushPermissionStatus";
const LAST_ACTIVE_LIST_ID_KEY = "navigation:lastActiveListId";

export const getOnboardingCompleted = async (): Promise<boolean> => {
  const raw = await AsyncStorage.getItem(ONBOARDING_COMPLETED_KEY);
  return raw === "true";
};

export const setOnboardingCompleted = async (value: boolean): Promise<void> => {
  await AsyncStorage.setItem(ONBOARDING_COMPLETED_KEY, value ? "true" : "false");
};

export const getPushPermissionStatus = async (): Promise<string | null> =>
  AsyncStorage.getItem(PUSH_PERMISSION_STATUS_KEY);

export const setPushPermissionStatus = async (value: string): Promise<void> => {
  await AsyncStorage.setItem(PUSH_PERMISSION_STATUS_KEY, value);
};

export const getLastActiveListId = async (): Promise<string | null> =>
  AsyncStorage.getItem(LAST_ACTIVE_LIST_ID_KEY);

export const setLastActiveListId = async (listId: string): Promise<void> => {
  await AsyncStorage.setItem(LAST_ACTIVE_LIST_ID_KEY, listId);
};

export const clearLastActiveListId = async (): Promise<void> => {
  await AsyncStorage.removeItem(LAST_ACTIVE_LIST_ID_KEY);
};
