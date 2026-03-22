import NetInfo from "@react-native-community/netinfo";
import { createContext, useContext, useEffect, useMemo, useState, type ReactNode } from "react";

type ConnectivityContextValue = {
  isOnline: boolean;
};

const ConnectivityContext = createContext<ConnectivityContextValue | undefined>(undefined);

export const ConnectivityProvider = ({ children }: { children: ReactNode }) => {
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener((state) => {
      setIsOnline(Boolean(state.isConnected));
    });

    return () => {
      unsubscribe();
    };
  }, []);

  const value = useMemo<ConnectivityContextValue>(() => ({ isOnline }), [isOnline]);

  return <ConnectivityContext.Provider value={value}>{children}</ConnectivityContext.Provider>;
};

export const useConnectivity = (): ConnectivityContextValue => {
  const context = useContext(ConnectivityContext);

  if (!context) {
    throw new Error("useConnectivity must be used inside ConnectivityProvider.");
  }

  return context;
};
