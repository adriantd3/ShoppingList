import type { AppTamaguiConfig } from "./src/ui/tamagui.config";

declare module "tamagui" {
  interface TamaguiCustomConfig extends AppTamaguiConfig {}
}

export {};
