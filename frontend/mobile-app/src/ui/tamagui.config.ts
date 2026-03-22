import { createFont, createTamagui, createTokens } from "@tamagui/core";

const bodyFont = createFont({
  family: "System",
  size: {
    1: 12,
    2: 14,
    3: 16,
    4: 18,
    5: 22,
  },
  lineHeight: {
    1: 18,
    2: 20,
    3: 24,
    4: 28,
    5: 32,
  },
  weight: {
    4: "400",
    6: "600",
    7: "700",
  },
  letterSpacing: {
    4: 0,
  },
});

const tokens = createTokens({
  size: {
    true: 16,
    1: 4,
    2: 8,
    3: 12,
    4: 16,
    5: 20,
    6: 24,
  },
  space: {
    true: 16,
    1: 4,
    2: 8,
    3: 12,
    4: 16,
    5: 20,
    6: 24,
    7: 28,
    8: 32,
  },
  radius: {
    true: 8,
    1: 4,
    2: 8,
    3: 12,
    4: 16,
  },
  color: {
    background: "#F8FAFC",
    color: "#0F172A",
    primary: "#0F766E",
    muted: "#64748B",
    surface: "#FFFFFF",
    danger: "#B91C1C",
  },
});

export const tamaguiConfig = createTamagui({
  tokens,
  themes: {
    light: {
      background: "#F8FAFC",
      color: "#0F172A",
      primary: "#0F766E",
      muted: "#64748B",
      surface: "#FFFFFF",
      danger: "#B91C1C",
    },
  },
  fonts: {
    body: bodyFont,
    heading: bodyFont,
  },
});

export type AppTamaguiConfig = typeof tamaguiConfig;
