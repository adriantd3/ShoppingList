import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { type ReactNode, useState } from "react";
import { TamaguiProvider } from "tamagui";

import { AppPreferencesProvider } from "./AppPreferencesProvider";
import { AuthSessionProvider } from "./AuthSessionProvider";
import { ConnectivityProvider } from "./ConnectivityProvider";
import { tamaguiConfig } from "../ui/tamagui.config";

export const RootProviders = ({ children }: { children: ReactNode }) => {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            retry: 1,
            staleTime: 10_000,
          },
        },
      }),
  );

  return (
    <TamaguiProvider config={tamaguiConfig} defaultTheme="light">
      <QueryClientProvider client={queryClient}>
        <ConnectivityProvider>
          <AppPreferencesProvider>
            <AuthSessionProvider>{children}</AuthSessionProvider>
          </AppPreferencesProvider>
        </ConnectivityProvider>
      </QueryClientProvider>
    </TamaguiProvider>
  );
};
