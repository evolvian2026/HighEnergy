// In-memory stand-in for the artifact runtime's `db`, `user` and `downloads` capabilities.
// Config comes from window.__MOCK = {uid, staff, names, seed}. Rules mirror portal/capabilities.json.
(() => {
  const M = window.__MOCK; if (!M) return;
  const store = window.__store = JSON.parse(JSON.stringify(M.seed || {}));
  const subs = new Set();
  const notify = () => setTimeout(() => subs.forEach(f => f()), 5);
  const clone = v => JSON.parse(JSON.stringify(v));
  const canRead = p => M.staff || p === "progress/" + M.uid || p === "scores/" + M.uid;
  const canWrite = p => M.staff || p === "progress/" + M.uid;
  const meta = {fromCache: false, hasPendingWrites: false};
  const snap = p => { const ok = canRead(p) && p in store; return {id: p.split("/").pop(), exists: ok, data: () => ok ? Object.freeze(clone(store[p])) : undefined, metadata: meta}; };
  const doc = p => ({id: p.split("/").pop(), path: p,
    get: async () => snap(p),
    set: async d => { if (!canWrite(p)) throw {code: "invalid_argument", message: "denied"}; store[p] = clone(d); window.__writes = (window.__writes || 0) + 1; notify(); },
    update: async d => { if (!canWrite(p) || !(p in store)) throw {code: "invalid_argument"}; Object.assign(store[p], clone(d)); notify(); },
    delete: async () => { if (!canWrite(p)) throw {code: "invalid_argument"}; delete store[p]; notify(); },
    onSnapshot(next) { const f = () => next(snap(p)); subs.add(f); setTimeout(f, 10); return () => subs.delete(f); },
    collection: s => coll(p + "/" + s)});
  const coll = p => ({path: p, doc: id => doc(p + "/" + (id || Math.random().toString(36).slice(2))),
    onSnapshot(next) { const f = () => { const depth = p.split("/").length + 1;
        const docs = Object.keys(store).filter(k => k.startsWith(p + "/") && k.split("/").length === depth && canRead(k)).sort().map(snap);
        next({docs, size: docs.length, empty: !docs.length, docChanges: () => [], metadata: meta}); };
      subs.add(f); setTimeout(f, 10); return () => subs.delete(f); }});
  const db = {doc, collection: coll};
  const user = {id: async () => M.uid, canEdit: async () => !!M.staff, isOwner: async () => !!M.owner, can: async () => null,
    profiles: async ids => Object.fromEntries(ids.map(i => [i, {name: (M.names || {})[i] || ""}]))};
  const downloads = {save: async f => { window.__download = f; }};
  window.claude = {use: async n => ({db, user, downloads})[n] || null};
})();
