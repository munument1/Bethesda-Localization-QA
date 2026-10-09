import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import zlib from "node:zlib";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const meta = JSON.parse(await fs.readFile(path.join(root, "snapshot-manifest.json"), "utf8"));
const output = path.resolve(process.argv[2] || path.join(root, "restored-review"));
await fs.mkdir(output, { recursive: true });
const digest = bytes => crypto.createHash("sha256").update(bytes).digest("hex");

for (const [filename, info] of Object.entries(meta.source_files)) {
  let encoded = "";
  for (const part of info.parts) {
    encoded += (await fs.readFile(path.join(root, part), "utf8")).trim();
  }
  const compressed = Buffer.from(encoded, "base64");
  const raw = zlib.gunzipSync(compressed);
  if (digest(compressed) !== info.gzip_sha256 ||
      digest(raw) !== info.sha256 ||
      raw.length !== info.bytes) {
    throw new Error("Snapshot checksum mismatch: " + filename);
  }
  await fs.writeFile(path.join(output, filename), raw);
  console.log("RESTORED", filename, raw.length, "bytes");
}
console.log("All snapshot files restored and verified.");
