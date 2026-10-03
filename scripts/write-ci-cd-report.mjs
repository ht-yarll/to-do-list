import { execFileSync } from "node:child_process";
import { readFileSync, writeFileSync } from "node:fs";

const [eventsPath, imageIdsPath, reportPath] = process.argv.slice(2);

const events = readFileSync(eventsPath, "utf8")
  .split("\n")
  .filter(Boolean)
  .map((line) => {
    const [name, command, status, duration] = line.split("\t");
    return { name, command, status, duration_seconds: Number(duration) };
  });

const imageIds = readFileSync(imageIdsPath, "utf8")
  .split("\n")
  .filter(Boolean);

const images = imageIds.map((id) => {
  const image = JSON.parse(
    execFileSync("docker", ["image", "inspect", id], { encoding: "utf8" }),
  )[0];

  return {
    repository_tags: image.RepoTags ?? [],
    id: image.Id,
    size_bytes: image.Size,
    size_mib: Number((image.Size / 1024 / 1024).toFixed(2)),
    architecture: image.Architecture,
    os: image.Os,
    configured_user: image.Config.User || "root (default)",
    entrypoint: image.Config.Entrypoint ?? [],
    command: image.Config.Cmd ?? [],
    exposed_ports: Object.keys(image.Config.ExposedPorts ?? {}),
    layers: image.RootFS.Layers.length,
  };
});

const report = {
  run_id: process.env.CI_CD_RUN_ID,
  result: process.env.CI_CD_RESULT,
  started_at: process.env.CI_CD_STARTED_AT,
  finished_at: new Date().toISOString(),
  checks: events,
  deployment: {
    mode: "emulated",
    message: "Deploying on Coolify (emulated)",
    triggered: false,
  },
  images,
};

writeFileSync(reportPath, `${JSON.stringify(report, null, 2)}\n`);
