import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";

import { loginWithEmailPassword } from "../services/auth/authApi";
import { clearAccessToken, getAccessToken, setAccessToken } from "../services/auth/sessionStorage";

type AuthSessionContextValue = {
  isHydrating: boolean;
  accessToken: string | null;
  isAuthenticated: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
};

const AuthSessionContext = createContext<AuthSessionContextValue | undefined>(undefined);

export const AuthSessionProvider = ({ children }: { children: ReactNode }) => {
  const [isHydrating, setIsHydrating] = useState(true);
  const [accessToken, setAccessTokenState] = useState<string | null>(null);

  useEffect(() => {
    const hydrate = async () => {
      const token = await getAccessToken();
      setAccessTokenState(token);
      setIsHydrating(false);
    };

    hydrate().catch(async () => {
      await clearAccessToken();
      setAccessTokenState(null);
      setIsHydrating(false);
    });
  }, []);

  const value = useMemo<AuthSessionContextValue>(
    () => ({
      isHydrating,
      accessToken,
      isAuthenticated: Boolean(accessToken),
      signIn: async (email: string, password: string) => {
        const result = await loginWithEmailPassword({ email, password });
        await setAccessToken(result.access_token);
        setAccessTokenState(result.access_token);
      },
      signOut: async () => {
        await clearAccessToken();
        setAccessTokenState(null);
      },
    }),
    [accessToken, isHydrating],
  );

  return <AuthSessionContext.Provider value={value}>{children}</AuthSessionContext.Provider>;
};

export const useAuthSession = (): AuthSessionContextValue => {
  const context = useContext(AuthSessionContext);

  if (!context) {
    throw new Error("useAuthSession must be used inside AuthSessionProvider.");
  }

  return context;
};
