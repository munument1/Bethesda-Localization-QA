import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const read = async rel => JSON.parse(await fs.readFile(path.join(root, rel), "utf8"));
const progress = await read("reviews/online-progress.json");
const dir = path.join(root, "active");
const files = (await fs.readdir(dir)).filter(x => /^pending-\d+\.jsonl$/.test(x)).sort();
const rows = new Map();
for (const file of files) {
  const body = await fs.readFile(path.join(dir, file), "utf8");
  for (const line of body.split(/\r?\n/).filter(Boolean)) {
    const r = JSON.parse(line);
    if (rows.has(r.id)) throw Error("Duplicated source ID " + r.id);
    rows.set(r.id, r);
  }
}
const structure = s => JSON.stringify(s.match(/<[^>]*>|%[-+0-9.#]*[A-Za-z]|\{[^{}]+\}/g) || []);
const count = (text, fragment) => text.split(fragment).length - 1;
const ids = [];
let corrected = 0, approved = 0, held = 0;
for (const name of progress.online_decision_files) {
  const batch = await read(name);
  if (!batch.review_decisions) throw Error("No decisions: " + name);
  for (const d of batch.review_decisions) {
    const source = rows.get(d.id);
    if (!source || source.review_status !== "unprocessed") throw Error("Invalid source " + d.id);
    if (ids.includes(d.id)) throw Error("Duplicate reviewed ID " + d.id);
    ids.push(d.id);
    let translated = source.korean;
    for (const change of d.patches || []) {
      const occurrences = count(translated, change.before);
      if (occurrences !== change.occurrences) throw Error("Patch mismatch " + d.id + ": " + change.before);
      translated = translated.replaceAll(change.before, change.after);
    }
    if (translated !== d.reviewed_korean) throw Error("Reviewed text mismatch " + d.id);
    if (count(translated, "\r") !== count(source.korean, "\r") ||
        count(translated, "\n") !== count(source.korean, "\n") ||
        structure(translated) !== structure(source.korean)) {
      throw Error("Format mismatch " + d.id);
    }
    if (d.status === "corrected") corrected++;
    else if (d.status === "approved") approved++;
    else if (d.status === "needs_context") held++;
    else throw Error("Invalid status " + d.id);
  }
}
if (JSON.stringify(ids) !== JSON.stringify(progress.reviewed_ids) ||
    rows.size !== 41 ||
    progress.counts.completed !== 16141 + ids.length ||
    progress.counts.unprocessed !== rows.size - ids.length ||
    progress.counts.corrected !== 3191 + corrected ||
    progress.counts.approved !== 11981 + approved ||
    progress.counts.needs_context !== 969 + held ||
    progress.counts.approved + progress.counts.corrected + progress.counts.needs_context !== progress.counts.completed) {
  throw Error("Online progress/decisions inconsistent");
}
console.log("ONLINE_QA_PASS", JSON.stringify({
  reviewed: ids.length, corrected, approved, needs_context: held,
  remaining: progress.counts.unprocessed, completed: progress.counts.completed
}));
