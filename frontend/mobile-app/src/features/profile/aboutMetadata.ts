export type AboutMetadataInput = {
  runtimeVersion: string;
  environmentLabel: string;
  buildNumber: string | number;
  now: Date;
};

export type AboutMetadata = {
  version: string;
  environment: string;
  build: string;
  buildDate: string;
};

export const buildAboutMetadata = (input: AboutMetadataInput): AboutMetadata => ({
  version: input.runtimeVersion,
  environment: input.environmentLabel,
  build: String(input.buildNumber),
  buildDate: input.now.toISOString().slice(0, 10),
});
