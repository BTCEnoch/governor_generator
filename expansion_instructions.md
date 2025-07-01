Perfect. I’ll explore how to inscribe a core application that is immutable yet recursively expandable using Bitcoin Ordinals, relying on the ord client and MetaShrew, with logic and content updates via reinscription or expansion sets (e.g., Goetia or Archangels). I’ll identify approaches that allow you to preload recursive pointers to future content, and methods for dynamic referencing using sat names, IDs, and inscription manifests. I’ll also consider recursive loader scripts that can pull the latest expansion sets. I’ll get back to you shortly with the findings.


# Deploying an Ordinals Application with Recursive Expansion Support

## Overview

Bitcoin Ordinals enable an application (like a game) to be stored on-chain as an **immutable core inscription**, with the ability to reference additional content later via **recursive inscriptions**. In practice, this means you can inscribe a base game (e.g. the 91 Enochian Governors) and **extend it with future expansions** (like Ars Goetia demons or Archangel profiles) without altering the original inscription. The core idea is to bake into the base inscription some logic or pointers that can **dynamically pull in new inscriptions** as they are created. This guide explores all technical approaches to achieve this, focusing on using satoshi anchors (by number or *sat name*) for re-inscription, recursion via the `ord` client, and optional use of MetaShrew for advanced indexing. We’ll cover how to pre-bake recursion support, how to reference or discover new data (`sat::number`, `sat::name`, or `inscription::id`), patterns for on-chain manifests or indexers, dynamic loading techniques, and MetaShrew integration. Code snippets and examples (using an RPG expansion theme) are included, along with notes on limitations.

## Pre-Baking Recursive Support in the Core Inscription

To future-proof your base Ordinals application for expansions, you must **embed recursion logic upfront** in its content. In practice, this means designing the core inscription (HTML/JS or other code) such that it knows how to fetch and incorporate external inscriptions. Key steps include:

* **Use an HTML/JavaScript Inscription as the Core:** A common approach is to inscribe the base game as an HTML file with embedded JavaScript. This allows the inscription to execute logic in a browser or Ordinals viewer and dynamically load other data. Ordinals protocol now supports **inscription recursion**, meaning one inscription can request content of another via Ordinals-specific endpoints. By leveraging these endpoints in the code, your base app can pull in expansion content on the fly.

* **Whitelist Recursive Calls:** The Ordinals `ord` server provides certain whitelisted HTTP endpoints (under a special path, often `/r/` or similar) that inscriptions can call to retrieve on-chain data (other inscriptions, block data, etc). These are designed for recursion and are sandboxed for security. Ensure your core app’s code uses these whitelisted calls (e.g. fetching from `/content/<inscription_id>` or `/r/sat/...`) rather than any off-chain URLs. This guarantees all data remains on-chain.

* **Plan an Anchor for Expansions:** Decide how the base will **identify future expansions**. The most robust method is to dedicate a specific satoshi (or a set of sats) as **anchors** for expansion content. By “anchor” we mean a known identifier (sat number or a sat name) that the base can reference. The base inscription should “know” these anchors (hard-coded or by algorithm) so it can look up inscriptions on them later. Pre-baking support might involve an internal list of expansion anchors (which could correspond to expansion categories or packs) or logic to scan an anchor for *any number of new inscriptions*. We’ll detail this under anchors and manifests below.

* **Include a Recursion Loader Script:** Within the core inscription, include a small loader routine that uses Ordinals recursion APIs to fetch expansion content. For example, you might have a JavaScript function that queries the Ordinals server for new inscription IDs on a given satoshi, or directly loads content by inscription ID. This code will run when the inscription is viewed (e.g. in a wallet or web viewer that supports Ordinals content), automatically pulling in expansions. By preparing this in advance, the core app can remain immutable yet *extensible* – as new inscriptions appear, the loader will retrieve and integrate them.

By taking the above steps, the core inscription is effectively a **self-contained application with hooks for future content**. Next, we discuss how to implement the anchor and referencing mechanisms in detail.

## Anchoring Expansions with Sat Numbers or Names

A fundamental decision is how to **anchor** your expansions on-chain so that the core can find them. Bitcoin Ordinal theory gives every satoshi a unique identifier (its *ordinal number*), and optionally human-readable *sat names* can be assigned via naming protocols. Using a specific satoshi as an anchor has two big advantages: it’s a **stable reference** (the sat’s identity never changes), and you can inscribe on that same sat multiple times to create a sequence of related inscriptions. In effect, the satoshi becomes a **container or thread** for your expansion content. This approach was proposed as a way to treat a sat as a variable that can hold evolving state via multiple inscriptions.

**Choosing a Sat Anchor:** You can pick a particular satoshi by its number (e.g. sat #123456789) to be the home for expansions. Ideally, this sat would be one you control in your wallet. You might choose a sat with a special significance or rarity, or even register a **Sat Name** for it (using the `.sats` name system) to give it a memorable label. For example, you could name your anchor sat `gamecore.sats` for the base, or separate names like `goetia-expansion.sats` for a specific expansion pack. In practice, Sat Names are resolved via indexers (they map a name to a specific inscription/sat), so the core app would need a way to translate the name to the sat or inscription. If you prefer to avoid external name resolution, **using the raw sat number is simpler** for on-chain lookups.

**Inscribing on the Anchor Repeatedly:** Once you have an anchor sat:

* Inscribe your **core application** on that sat first. This makes the sat the “core inscription” holder (the first inscription on that sat).
* Later, when adding expansions, **re-inscribe on the same satoshi**. Each new inscription on that sat will be linked to the previous (forming a chain). Because the satoshi is the same, Ordinals will recognize the subsequent inscriptions as related (children of the first, conceptually).

Using one satoshi for multiple inscriptions is fully supported. Ordinals indexes can list all inscriptions on a given sat in chronological order. In fact, the Ordinals `ord` client introduced recursive endpoints to query by sat number: you can get the first inscription, nth inscription, or the latest inscription on sat *N* easily. For example:

* `GET /r/sat/123456789` – returns the inscription IDs of (up to) the first 100 inscriptions on sat #123456789.
* `GET /r/sat/123456789/at/-1` – returns the **most recent inscription ID** on that sat (using `-1` as an index from the end).
* `GET /r/sat/123456789/at/-1/content` – fetches the **content** of the latest inscription on that sat directly.

These endpoints (enabled by running `ord` with the `--index-sats` option for full sat indexing) let your core app dynamically pull data from any new inscription on the anchor sat. Using a sat number as the reference is reliable because the sat doesn’t change even as it moves UTXOs or gets re-inscribed – it’s a stable handle.

**Sat Names as Anchors:** If you opt to use a Sat Name, the idea is similar: the name would correspond to a particular sat or inscription. For instance, if `goetia.sats` is registered and points to a certain sat, expansions could be inscribed on that sat. The base app could then know “load expansions from sat name X”. However, natively the Ordinals client **does not resolve sat names in recursion calls** – you would need an indexer or external lookup to convert the name to the sat number or inscription ID. MetaShrew or another indexer could facilitate this (more on MetaShrew later). In summary, sat names can make things human-readable, but under the hood you will still be using sat numbers or inscription IDs to fetch content. So we typically **anchor by sat number** in code, and you can treat the sat name as just a friendly alias if needed.

**Multiple Anchors vs Single Anchor:** Depending on how you want to organize expansions, you can either use **one anchor sat** for all expansions or **separate anchors per expansion category**. A single anchor (e.g. the core sat itself) means every expansion inscription (Ars Goetia, Archangels, etc) will be reinscribed on that one sat in sequence. This creates one linear list of children. The benefit is simplicity – one place to look for anything new. The downside is if you expect hundreds of inscriptions, you might need pagination and it’s less segmented by topic. Alternatively, you could designate distinct sats for each expansion **category**. For example, sat A holds the core, sat B is reserved for all Ars Goetia content, sat C for Archangels, etc. In the base logic you’d predefine those anchor sats (or their names), and expansions for that category would be inscribed there. This approach partitions content logically (making it easy to fetch, say, only Archangel profiles by looking at sat C), but requires managing multiple anchors. It also means the base app needs to know all the relevant sat numbers upfront (or at least a way to discover them, perhaps via a manifest). Many implementations go with a **single anchor (the core’s sat)** for all expansions unless the content volume or separation of concerns suggests otherwise.

In either case, anchoring expansions on known sats is the cornerstone of making an Ordinals app upgradable. We’ll next see how the base inscription can use recursion to reference these anchored expansions.

## Referencing and Discovering Expansion Inscriptions Recursively

With anchors in place, the core inscription needs a strategy to **discover new inscriptions** and load their content. There are a few methods to reference expansion data in an Ordinals context:

### 1. **Using Ordinals Recursion Endpoints (Dynamic Lookup)**

This is the most flexible method. As described earlier, the Ordinals client provides recursive HTTP endpoints that a running inscription can call to query on-chain data. Your base app can utilize these to find expansions by sat or by parent-child relationships:

* **Query by Sat Number:** The base can call `/r/sat/<SAT_NUMBER>` to get a list of inscription IDs on that sat. It can then fetch each inscription’s content by calling `/content/<inscription_id>` (or directly `/r/sat/<SAT>/at/<index>/content`). This effectively scans the anchor for any expansions. For example, if the base’s anchor sat is 987654321, your code can do:

  ```js
  // Pseudocode inside base inscription
  const satNum = 987654321n;
  const res = await fetch(`/r/sat/${satNum}`); 
  const { ids } = await res.json(); 
  // ids is an array of inscription IDs on that sat (first 100 by default)
  for (let id of ids) {
    if (id === CURRENT_INSCRIPTION_ID) continue; // skip the base itself if present
    let content = await fetch(`/content/${id}`).then(r=>r.text());
    processExpansionContent(id, content);
  }
  ```

  This snippet would retrieve up to 100 child inscription IDs on the sat and then fetch each expansion’s content (as text, which could be JSON, HTML, etc.) for the app to integrate. If you expect more than 100 expansions, you can call subsequent pages (`/r/sat/<SAT>/1`, `/2`, etc.) to get more. The ord endpoints provide pagination support in batches of 100.

  Notably, you can also shortcut if you only care about the **latest expansion**: call `/r/sat/<SAT>/at/-1/content` to get the content of the newest inscription on that sat. This is useful if expansions are more like updates (where you only need the latest state). In a game context, however, you likely want *all* content packs available, not just the latest, so listing all IDs is more appropriate.

* **Query by Parent Inscription (Children):** When using a single sat for multiple inscriptions, Ordinals inherently forms a parent-child relationship: the first inscription on that sat can be considered the “parent”, and later ones are “child inscriptions”. The `ord` server also offers a recursion endpoint to list children of a given inscription ID. For example, `GET /r/children/<INSCRIPTION_ID>` returns the first 100 child inscription IDs of that inscription. The base app could call this with its own inscription ID to discover expansions (assuming it is the first inscribed on that sat, which is the usual case). The result is similar to the sat query (a JSON with an `"ids": [...]` array of child IDs). You could then fetch each child’s content. Using `/r/children` has the advantage of not needing the sat number explicitly; it works because ord’s index knows that those later inscriptions share the same sat as the base (hence they are children). However, **be mindful**: this only lists direct children (inscriptions on the same sat). If you chose multiple anchor sats approach, you’d have to use the respective parent IDs for each category.

* **Direct Inscription ID References (Static):** Another approach is to have the base inscription directly reference specific inscription IDs or known content addresses. For example, you could embed an expansion by ID using an `<iframe>` or `<script>` tag like: `<script src="/content/<EXPANSION_ID>"></script>`. This would pull that expansion’s code or data into the page. The catch here is **you need to know the inscription IDs ahead of time**, which is usually not possible for future content (since inscription IDs are essentially a product of the transaction that hasn’t happened yet). One creative workaround is if you pre-register certain inscriptions (e.g., inscribe placeholders or blank content on certain sats so that you know their IDs, then later update them via reinscription). But generally, static ID references are only feasible for content that already exists at the time of the base inscription. Given expansions are “future” content, static hard-coding is inflexible. It’s better to use the dynamic discovery by sat or children as above, unless you’re absolutely sure of the expansion IDs (which in practice, you won’t be unless you inscribe everything upfront or reserve them).

**Example:** Suppose our base game knows about two anchors: sat #1000 for “Goetia” expansion and sat #2000 for “Archangels” expansion. We could preload those references in code:

```js
const expansionAnchors = [1000n, 2000n];
for (let sat of expansionAnchors) {
  let latest = await fetch(`/r/sat/${sat}/at/-1/content`).then(r=>r.text());
  if (latest) { loadExpansion(latest); }
}
```

In this snippet, the base tries to fetch the content of the latest inscription on each anchor sat. If nothing has been inscribed yet, the endpoint might return an empty result or 404 (the code should handle that gracefully). Once you inscribe something on, say, sat 1000, this code will start pulling it in. This is a **preloaded pointer** approach – the base knows where to look, but fetches at runtime whether content is there.

### 2. **Maintaining an On-Chain Manifest (Updatable List)**

Instead of scanning sats or children each time, another pattern is to use a **manifest file** that enumerates expansions. The manifest itself would be on-chain and could be *updated* whenever new expansions are added. How can something immutable be updated? By using reinscription on a known sat – much like how we anchor expansions, we can anchor a manifest. For example, you inscribe a JSON list of expansions (perhaps mapping expansion names to their inscription IDs or other metadata) on a dedicated sat. Later, when adding a new expansion, you inscribe a new JSON that includes the new entry on that *same manifest sat*. The manifest sat’s latest inscription thus always contains the up-to-date list. The base app can then simply fetch the manifest’s content (always hitting the latest version) to get a list of all expansion items.

This approach centralizes the index of expansions in one place (the manifest data structure), which can be easier to manage especially if expansions are scattered or if you want to attach metadata (names, descriptions, categories, etc.). It does, however, introduce one extra step (updating the manifest with each expansion). You can automate that in your workflow: e.g., whenever you inscribe a new expansion, you also produce a new manifest inscription.

Using recursion, retrieving the manifest in the base is straightforward: if the manifest anchor sat is known, call `/r/sat/<manifest_sat>/at/-1/content` to get the latest manifest JSON, then parse it. Or use the parent ID’s children listing similarly. This gives the base a quick summary of expansions without iterating over many sats.

**Example Manifest JSON:** an inscription might look like:

```json
{
  "expansions": [
    { "name": "Ars Goetia", "id": "<inscriptionID1>", "sat": 1000 },
    { "name": "Archangels", "id": "<inscriptionID2>", "sat": 2000 }
  ]
}
```

As new expansions are added, a new version of this JSON is inscribed with additional entries. The base app would fetch this JSON and, for each entry, retrieve the content via the `id` or the `sat` provided. (The manifest could list just IDs if the base then fetches `/content/<id>`, or it could list sat numbers and the base uses those to fetch latest on each – design choice.)

This method is similar in spirit to how an indexer might maintain state, but done *on-chain*. It is inherently limited by the need to parse the manifest and possibly by manifest size (if you had thousands of expansions, the JSON grows). Still, it stays within Ordinals immutability rules because each manifest version is an immutable inscription; you’re just using a stable pointer (sat or name) to always get the newest version. Essentially, the manifest sat acts like a “file” that can be overwritten by creating new versions.

### 3. **External Discovery via Indexer (Offloading to MetaShrew)**

We’ll cover this in detail in a later section, but note here: you do have the option to **not embed full discovery logic on-chain** and instead rely on an external indexer service (like MetaShrew) to find expansions. In that case, the base inscription might contain minimal logic (or static pointers), and your client application would query the indexer to get expansion data. For example, the base could have placeholders that the client fills by calling a MetaShrew GraphQL API to list all inscriptions with a certain tag or parent. This method steps a bit outside the pure on-chain environment (since it needs the indexer), but can simplify things if the indexer does heavy lifting (like searching by sat name, or handling >100 inscriptions easily). We consider this acceptable since MetaShrew is a decentralized indexer that can be self-hosted, but it **does introduce an off-chain dependency** in the data flow, so use it if necessary or advantageous.

**Recommendation:** For a trustless, self-contained approach, **use the Ordinals recursion endpoints (sat or children)** to dynamically discover expansions. That means inscribe expansions on known anchors and have the base fetch them at runtime. This ensures no external service is strictly required to see new content – any user running the `ord` server or compatible viewer will have the base inscription automatically pull in expansions from the Bitcoin blockchain itself.

Now that we have ways to find expansions, let’s look at concrete mechanics and patterns for implementing these, including code examples and loader scripts.

## Dynamic Loading of Expansion Content in the Base App

To actually *use* the expansions, the core inscription’s code must retrieve their content and integrate it (whether that means displaying new data or executing new logic). Here are some patterns and examples for dynamic loading:

* **JavaScript Fetch & Inject:** If the core is an HTML/JS app, you can use the Fetch API (as in the snippets above) to get expansion content from the ord endpoints. Once fetched, what you do with it depends on the content type:

  * *If expansions are data* (e.g. JSON profiles, text, or game data): Parse the data and merge it into the application state. For example, if the base game has a list of characters, and an expansion provides new character stats, the loader can append those to the list. If the expansion is an image or audio (like an asset file), you might create an `<img>` or audio element in the DOM with the source set to a data URL or another fetch call.

  * *If expansions are code/logic* (e.g. a script adding new game mechanics or UI components): You can evaluate the fetched code. For safety and simplicity, one can inscribe expansions as JavaScript modules or scripts, then use `eval()` or create a `<script>` tag with the content to execute it. Another method is inscribing as an ES module and using dynamic `import()`, but direct fetch + eval is straightforward if you trust the code (which you should if it’s your own expansion). For example:

    ```js
    let scriptText = await fetch(`/content/${expansionScriptId}`).then(r=>r.text());
    // Execute the script in global context
    window.eval(scriptText);
    // Assuming the script defines some global function or triggers a registration in the game
    ```

    If the expansions are designed to register themselves (e.g. calling a known global method in the base to add new content), this works well. Alternatively, if the base expects expansions to export something, you might adapt a module pattern.

  * *If expansions are HTML/GUI pieces:* You could also fetch HTML snippet and insert it into the DOM (e.g. `innerHTML`). This might be relevant if an expansion includes a preformatted layout or UI element. Just ensure any associated scripts in that HTML either come through or are separately loaded.

* **Direct `<script src="...">` or `<iframe>` Embeds:** Instead of fetching via JS and eval, you can sometimes use direct embedding in the HTML. For example, you could include in your base HTML something like:

  ```html
  <script src="/content/INSCRIPTION_ID_OF_SOME_EXPANSION.js"></script>
  ```

  If that inscription ID exists, the script will load and execute. If it doesn’t exist yet (because the expansion is not inscribed at the time someone views the base), the request will fail – most likely nothing happens, or an error might be logged. One way to handle this is to include a script that tries a series of known IDs and simply catches failures. However, this approach is clunkier than using a dynamic fetch loop which can be made robust. Similarly, you could embed an `<iframe>` pointing to an expansion’s content (especially if it’s an HTML mini-app itself), though interacting with it from the parent might be complex due to sandboxing. Generally, a controlled fetch gives you more ability to handle “not yet present” scenarios gracefully.

* **Loading Latest vs All Expansions:** Decide if your base app loads *all available expansions* at startup or only loads certain ones on demand. For a game, you might want to load everything so the user sees all content. If the content is heavy (lots of images etc.), you could lazy-load upon user action. For instance, you could show an “Ars Goetia” section in the UI and only fetch its data when the user opens that section. Because all data is on-chain, you can always fetch it later as needed. The recursion endpoints can be called anytime, not just at initial page load.

* **Example – Integrating Expansion Data:** Let’s say an expansion inscription contains a JSON array of new characters (with names, abilities, etc.). The base game’s loader might do:

  ```js
  let dataText = await fetch(`/r/sat/${goetiaSat}/at/-1/content`).then(r=>r.text());
  if (dataText) {
    let newChars = JSON.parse(dataText);
    gameData.characters.push(...newChars);  // merge new characters into core data
    updateCharacterUI(newChars);
  }
  ```

  If `goetiaSat` had no inscription yet, `dataText` might be empty and we simply do nothing. After an expansion is inscribed, this code would start pulling in the JSON and merging it. The function `updateCharacterUI` would be defined in core to add new character entries to whatever interface. Similarly, if the expansion was a script that perhaps calls a `registerCharacters(newChars)` function globally, the base could just load and rely on that.

* **Security and Compatibility:** Because recursion involves fetching data within the context of the Ordinals viewer, there are some considerations:

  * *Same-Origin policy:* Usually, the `ord` server hosts the inscription content at a local address. If your fetch calls are relative (like `/r/sat/...`), they hit the same origin (the ord server), which should be allowed. The Ordinal docs mention that recursive endpoints are whitelisted, meaning the environment running the inscription should permit those calls. If you encounter issues (for example, if viewing via a third-party explorer that doesn’t support recursion calls), you might need to run the content in an environment that does (like `ord` CLI’s own viewer or a wallet that supports recursion). For a truly decentralized app, you can instruct users to use a wallet or PWA that includes an Ordinals-aware viewer or run a local ord server.
  * *Performance:* Each fetch is a call to the Bitcoin node through `ord`. Keep data sizes in mind. Text and scripts are usually fine; large images or media might load slower – though still possible (the 4MB per inscription limit means even the biggest single piece is 4MB). Recursion can drastically save space by reusing assets (one inscription can reference an image in another inscription instead of storing it twice), which is great for expansion packs that might share common logic or art with the base.
  * *Immutability of loaded content:* Because each expansion inscription is immutable, you don’t have to worry about its content changing unexpectedly. But if you do a `/at/-1/content` to always get the latest, note that “latest” will change when a new expansion is added. That’s intended in our case (we want the game to update). Just ensure the base can handle content changing – e.g., if the base caches data, you might need to always fetch fresh or implement a version check.

* **Example – Preloading Pointers vs Runtime Discovery:** Let’s clarify with a concrete scenario:

  * *Preloaded pointer approach:* In your base HTML, you might have something like:

    ```html
    <script>
      const archangelSat = 2000n;
      fetch(`/r/sat/${archangelSat}/at/-1/content`)
        .then(res => res.text())
        .then(content => { if(content) eval(content) });
    </script>
    ```

    Here the base immediately tries to load the Archangel expansion script. If none exists, `content` will be empty and nothing happens. If later an Archangel script is inscribed on sat #2000, any new user (or a user refreshing the app) will now successfully fetch and eval it, activating that expansion. This is simple but requires that you knew to include this pointer (archangelSat) from the start. If new categories come along that you didn’t anticipate, the base wouldn’t have a pointer for them – that’s the drawback of preloading individual anchors.
  * *Dynamic discovery approach:* Instead, if your base doesn’t hardcode the Archangel sat, you could maintain a list of known expansion sats on-chain (manifest) or just decide on one anchor and iterate. Then even new types of expansions would be found. For example:

    ```js
    // Assume base's own sat is the single anchor:
    const baseSat = CURRENT_SAT_NUMBER; 
    const data = await fetch(`/r/sat/${baseSat}`).then(res=>res.json());
    for(let id of data.ids) {
      if(id.endsWith("i0")) continue; // skip the base itself (assuming it's index 0)
      let content = await fetch(`/content/${id}`).then(r=>r.text());
      integrateContent(id, content);
    }
    ```

    This way, if tomorrow you inscribe a brand new category expansion on the same sat, it will show up in `data.ids` and be loaded without the base explicitly knowing about it beforehand. The base can handle each expansion generically (maybe by reading a metadata header or by content type to decide how to integrate). This is the most **flexible** approach, essentially treating expansions as plug-ins discovered at runtime.

In summary, dynamic loading is achieved by using Ordinals recursion calls (`/r/sat`, `/content`, etc.) from within the base inscription to gather expansion data or code, and then programmatically merging it into the running app. Keep expansions’ format such that the base knows what to do with them (e.g., if it’s JSON, the base knows the schema; if it’s a script, the base knows it will call a registration function, etc.).

## Manifest and Index Strategies for Expansion Management

We touched on the idea of a manifest and also the limitations of the built-in methods. Here we compile recommended patterns and how to maintain them:

* **Single-Sat Chain (Implicit Manifest):** If you use one satoshi for everything, the list of inscriptions on that sat *is effectively a manifest*. The Ordinals index will have them ordered, and you can retrieve them as shown. This implicit manifest is simple but has the 100-per-page limit. If you envision more than 100 expansions (which is quite a lot for most cases), you can either handle pagination in the base (which is doable: just call page 1, 2, etc., until `more:false` in the JSON), or use multiple sats to break it up.

* **On-Chain Manifest File:** A JSON or even a simple text file (CSV, etc.) as described. If using JSON, make sure your base inscription includes a JSON parser (if using plain JS, `JSON.parse` is available by default). One could also inscribe a tiny JS snippet that literally contains a list of expansions and simply load that – but JSON is cleaner separation. The manifest should list enough info for the base to fetch the expansion content (IDs or sat numbers or even direct content if small). *Immutable vs Updatable:* Each version of the manifest is immutable, but since you inscribe a new one for updates, we consider it updatable as a whole. The base always fetching “the latest” version via a stable reference (sat or an inscription ID that is itself referenced recursively) ensures the user sees the updated list.

* **Hybrid Approach:** Use the manifest to store *metadata* (like titles, descriptions of expansions, maybe thumbnail image IDs), but still store the bulk content in separate inscriptions. The base could fetch manifest, populate an expansion menu (with names like “Ars Goetia (installed)” or “Archangels (coming soon)” depending on presence), then fetch individual expansions when needed.

* **Updating the Base App UI:** Regardless of manifest or not, consider how the user will know new content is available. If the base app loads dynamically each time, it will automatically show new stuff without needing an update (which is the goal!). If you want some indication like “New expansion detected!”, your code can compare what it loaded now versus maybe what was last loaded (though since it’s stateless, you might not have a memory of that across runs unless you store something in localStorage on the client side). This is more of a UX detail; technically the expansions will appear as soon as they are inscribed and the app is refreshed or reloaded by the user.

* **Example – Implementing an Updatable Manifest:** Let’s say you choose a dedicated sat for the manifest, sat #3000. Initially, you inscribe an empty or base manifest there:

  ```json
  { "expansions": [] }
  ```

  and your base app knows to fetch from sat 3000’s latest content. When you release the Ars Goetia expansion as an inscription on sat 1000, you also update the manifest by inscribing a new JSON on sat 3000:

  ```json
  { "expansions": [
      { "name": "Ars Goetia", "sat": 1000, "id": "<ID_of_Goetia_inscription>" }
    ]
  }
  ```

  Now sat 3000’s latest content includes Ars Goetia. The base app fetches it and sees one expansion entry, then knows to fetch content from the given sat or ID. Later, you inscribe Archangels on sat 2000, and update manifest with a third inscription on sat 3000:

  ```json
  { "expansions": [
      { "name": "Ars Goetia", "sat": 1000, "id": "<ID_of_Goetia_inscription>" },
      { "name": "Archangels", "sat": 2000, "id": "<ID_of_Archangels_inscription>" }
    ]
  }
  ```

  Now the base sees two entries. This process can continue. You might include also a version or timestamp in manifest if needed. Each manifest update is an on-chain event (so consider fees, though JSON text is usually small).

* **Alternate Indexing (MetaShrew or Custom):** If you wanted, you could eschew the manifest and rely on a custom rule: e.g., maybe every expansion inscription includes in its content a tag like `"expansion": true` or a reference to the base. An external indexer could scan all inscriptions for those tags, building a list. The base could then query that via an API. This is not possible using the on-chain recursion alone (since on-chain you can’t search arbitrary content easily), but with something like MetaShrew or Ordlite you could. This is more relevant if expansions were not neatly on one sat or known anchors, which in our plan they are, so probably unnecessary.

Having covered these patterns, you might be wondering about the role of MetaShrew specifically, as it was mentioned as acceptable for dynamic indexing. We will now discuss how MetaShrew can enhance or simplify some of the above.

## Using MetaShrew for Enhanced Expansion Indexing

**MetaShrew** is a powerful open-source indexer framework for Bitcoin meta-protocols (like Ordinals, Alkanes, Runes, etc.). It can index inscriptions and expose flexible query interfaces (including GraphQL and custom “view” functions). While our goal is to minimize reliance on external infrastructure, MetaShrew can act as a **real-time state index** for your game, which includes tracking expansions. Here’s how it can integrate and what benefits it brings:

* **Real-Time Discovery:** MetaShrew can monitor the blockchain and detect when new inscriptions relevant to your project are created. For example, you can configure it to watch a particular sat or inscription lineage. As soon as you inscribe a new expansion, MetaShrew’s index can record it. This means your game client (off-chain component or front-end) could subscribe to a WebSocket or GraphQL subscription and get notified immediately of the new expansion, rather than waiting for a user to refresh an Ordinals view. This is great for live updates.

* **Advanced Queries:** With MetaShrew, you can perform queries that ord’s built-in endpoints might not directly provide. For instance, you could query: *“Give me all inscriptions on sat #X with their content and timestamps”* or *“Find the inscription with sat name ‘goetia.sats’ and get its children”*. MetaShrew’s GraphQL API would let you ask for inscriptions filtered by sat, by content fields (if you index those), etc. The Hiro/Ordhook team noted that indexing Ordinals is non-trivial, but MetaShrew is designed to simplify it with out-of-the-box support for inscriptions and sat ranges. Essentially, MetaShrew extends the ord indexer and allows **custom indexing logic** on top of it.

* **Custom Views/Manifests:** In MetaShrew, you could implement a custom *view function* that aggregates data in a way you need. The MetaShrew docs give an example of a DNS-like system where child inscriptions represent updates, and a view can query a name to get all records (by collecting child inscriptions). We can apply the same concept: a view function could take your base project’s identifier (maybe the base inscription ID or a project name) and return the list of expansion records. Internally, this view would query the MetaShrew ord index for all child inscriptions of the base or all inscriptions on the anchor sat(s) and format them nicely. The client could then just call this single GraphQL query to get the whole manifest of expansions, without the base inscription having to loop or process multiple calls.

* **GraphQL Example:** Imagine a GraphQL schema where `expansions(projectID: ID)` returns a list of expansions with fields like `{name, inscriptionId, content, timestamp}`. Backed by MetaShrew, this query could gather all expansions for the given project. Your PWA or game client could call this on startup to get everything, or even listen on a subscription `expansionAdded(projectID)` that feeds new entries when detected. This brings a level of convenience similar to a traditional API, but it’s powered by an open indexer that you or the community runs (no centralized server required, aside from the indexer you choose to use).

* **Sat Names Resolution:** If you decided to incorporate sat names, MetaShrew could help here as well. The Sats Names System (SNS) inscriptions could be indexed such that a GraphQL query can resolve a name to an inscription or sat number. This would allow your app to accept a sat name and find the corresponding expansion inscription via MetaShrew’s data, rather than hardcoding the number.

* **MetaShrew in Practice:** Given the user’s architecture (from the context we have, they plan to use MetaShrew for game state and Alkanes smart contracts), using it for expansions is natural. For instance, MetaShrew might maintain an index of all “Governor game” inscriptions. You might tag your inscriptions (in the content or just by where they live) so MetaShrew can differentiate them from unrelated inscriptions. Then:

  * When a new expansion inscribes, MetaShrew catches it and updates its index.
  * The game’s back-end (or front-end PWA) queries MetaShrew (GraphQL) to fetch the new data and integrate it. This could even happen automatically via subscriptions – truly “dynamic” content loading without user refresh.
  * Because MetaShrew works with **GraphQL subscriptions for live updates**, one can imagine a scenario where a user’s app is open and an expansion is inscribed by the dev – the MetaShrew subscription pushes the new expansion data to the app in real-time, and the app could call the recursion endpoint to fetch the content and display it instantly. This is a cutting-edge user experience for on-chain games.

* **Indexing Beyond 100 Limit:** MetaShrew does not have the 100-child limit that the ord server endpoints do; it will index everything in the chain. So, if you ever exceeded 100 expansions on one sat, MetaShrew can retrieve all. It essentially removes technical limits at the cost of requiring the indexer to be running.

**Important:** Using MetaShrew means your **base inscription might not need as much discovery code**. If you rely on off-chain queries, the base could even be mostly static and let the client handle injecting expansions. But it’s wise to still include basic recursion support on-chain (so that if someone loads the base in a fully on-chain manner, they can still see expansions). The two approaches can complement each other: on-chain logic for trustlessness and backup, off-chain indexer for efficiency and real-time features.

In summary, MetaShrew integration offers **convenience and power**: you get robust indexing and querying capabilities (GraphQL, etc.) and can implement high-level patterns (like subscribing to new expansions) that would be hard to do purely within an inscription. The trade-off is that you are now depending on an indexing service (which you or others must run). Since the user indicated MetaShrew is acceptable, it can be leveraged especially in the context of a complex game where state (Alkanes smart contracts events, player inventory, etc.) is already being indexed by MetaShrew alongside content. Expansions are just another part of that data model.

## Example: Expanding an RPG On-Chain with Ordinals

To tie everything together, let’s walk through how one would implement an on-chain RPG (like the Enochian Governors game) with expansions step by step:

**1. Core Inscription Deployment:** Suppose we create a Progressive Web App (PWA) for the game and inscribe it as an HTML file on Bitcoin. We choose a special satoshi for this – perhaps a sat from a recent block that we control. For illustration, say sat #500000000000000 is our pick (just a random large number). We inscribe the HTML/JS on that sat via the `ord` client. This is the **immutable core** containing the base 91 Enochian Governors data and all the logic to run the game offline (since it’s a PWA). We might even inscribe necessary libraries (as separate inscriptions) and have the core `fetch()` them by inscription ID – the user’s provided architecture suggests even React libraries were inscribed and loaded by ID. In our core code, we include the expansion loader logic. For now, perhaps we anticipate two expansion anchors (Goetia and Archangels), so we include their sat numbers in a list. We also make sure to include the ability to load any number of expansions on the core’s own sat, in case we drop in additional content there.

**2. Running the Base App:** Users load the core inscription in a wallet or via a web viewer connected to an ord server. The app initializes – it might draw the UI for the base content (the 91 Governors). Then the expansion loader kicks in. It tries to fetch expansion content:

* It queries `/r/sat/500000000000000` (the core sat) for child inscriptions. Initially, there are none (aside from itself). It likely gets back just the base inscription ID. Seeing no new IDs, it doesn’t load any extra content.
* It also perhaps queries `/r/sat/600000000000000/at/-1/content` for sat 600000000000000 (imagine we reserved that for Goetia) and `/r/sat/700000000000000/at/-1/content` for Archangels. These return nothing initially (no content yet).
* The UI perhaps shows placeholders like “Ars Goetia – not installed” and “Archangels – not installed” (since no content was fetched). Or it hides those sections entirely until content is found.

**3. Inscribing an Expansion (Ars Goetia):** Now we prepare the Ars Goetia expansion. This could be, for example, a JSON file containing profiles of 72 demons (name, sigil image link, abilities) or even a JavaScript that, when run, registers these demons into the game’s character roster. Let’s say we go with JSON for data simplicity. We take sat #600000000000000 (which we earmarked for Goetia) – it’s an unused sat we deliberately set aside in our wallet. Using the `ord` client, we inscribe the `goetia.json` on that sat (ensuring the input UTXO is constructed such that this specific sat is the one being inscribed). The result is a new inscription (with some ID like `abcd...i0`). This inscription is now on sat 600000000000000, which previously had none. The first inscription on that sat is the Goetia data.

* Because we pre-baked the base app to look at that sat, any user loading or refreshing the app *after this point* will have the loader fetch `/r/sat/600000000000000/at/-1/content`. Now, `at/-1` finds the just-created Goetia inscription (which is the first and latest on that sat) and returns its content (the JSON). The base app then parses it and, for instance, populates a new “Ars Goetia” section in the game with 72 new characters. If it was a script, the base would eval it to perhaps add new gameplay logic (imagine if Ars Goetia added a new gameplay mode, a script could inject that).

* If we were using a dynamic single-sat approach instead, we might have inscribed the Goetia JSON on the **core’s sat (500000000000000)** as a child. In that case, the base app’s call to `/r/sat/500000000000000` would now see an extra ID (the new one) beyond the base. It would fetch it and similarly update the game. The difference is just whether we isolated expansions on their own sat or not. The workflow of inscribing and the base picking it up is analogous.

* If using a manifest approach: We would also now inscribe an updated manifest on, say, sat #500000000000001 (just another chosen anchor for manifest). But if our base is already coded to directly load Goetia from sat 600000000000000, a manifest might not be necessary in this simple two-expansion scenario. A manifest becomes more useful with many pieces.

**4. Inscribing Another Expansion (Archangels):** We repeat a similar process for Archangels on sat #700000000000000, with either data or code representing archangel profiles. Once inscribed, the base app’s loader will fetch it (since it was pre-pointed to that sat) and integrate the content, e.g., adding the archangels into the game’s character list.

**5. Unplanned Expansions:** Suppose later the developer wants to add a new expansion that wasn’t foreseen, e.g., a set of “Elemental Lords”. If the base app was only coded to check sats for Governors, Goetia, Archangels, it won’t know about this new expansion. This is where having a more generic discovery (like scanning the core sat for any child, or using a manifest which can be updated to include the new category) is important. If the base app did scan its own sat, the developer could simply choose to inscribe Elemental Lords on the core sat (500000000000000) as another child. The base would then find it without needing a code update, because it iterates through all children. If the base was not doing that, the developer could *update the manifest inscription* to include Elemental Lords and inscribe the content on a new sat, and as long as the base always reads the manifest, it will now see a new entry and load it.

This example shows how expansions can be delivered trustlessly: once the user has the core inscription, they automatically get new content by simply being online and connected to the Bitcoin network’s data (through an Ordinals-enabled viewer). **No app update, no server call – just an on-chain content fetch.**

If MetaShrew is in play, the experience could be even smoother:

* The user’s game client might connect to MetaShrew and subscribe to expansion updates. The moment the developer inscribes a new expansion, MetaShrew notices and sends a notification to the client, which then triggers the in-app loader to fetch the new content. The user could see a “New expansion available!” popup in real-time.
* Additionally, the client might query MetaShrew for a list of all expansions on startup rather than relying on the ord server at runtime. MetaShrew might reply with all expansion IDs and meta info, then the client can selectively fetch their content via the ord content API or even MetaShrew could store the content (but typically you’d still fetch from the Bitcoin source to remain trustless).

## Limitations and Considerations

When implementing recursive Ordinals applications with expansions, keep in mind several limitations and design constraints:

* **Immutability vs Upgradability:** Your core inscription is immutable, so the expansion hooks you code into it at the start will determine how flexible your expansion system is. Plan the architecture carefully – e.g., decide if you want one expansion thread or multiple, and include any generic loader logic you might need. If you forget something (like a reference to a particular sat or a parsing routine for a certain data format), you cannot change the core later without making an entirely new inscription (which would split your user base). A good practice is to make the core’s expansion loader as *generic* as possible (e.g., load all children or read a manifest rather than hardcoding specific IDs) to accommodate unforeseen additions.

* **Environment Requirements:** The recursion functionality works when the inscription is executed in an environment aware of it (such as the ord server’s built-in viewer or compatible wallets like Hiro, Xverse, etc., that have added recursion support). If someone simply views the inscription on a block explorer that doesn’t run scripts or support recursion, they might not see the dynamic content. For the full experience, users should use the intended client (a PWA, wallet, or at least the `ord` tool). Documentation and user guidance might be needed so they know how to properly run the on-chain app. Security-wise, the ord server guarantees backward compatibility for those recursion endpoints so your inscription’s calls will continue to work in future versions.

* **Performance and Size:** Each expansion will incur on-chain storage and user bandwidth. While recursion removes the 4 MB limit by allowing linking of multiple files, very large expansions (hundreds of MB across many files) could be slow to load. Optimize your content: perhaps compress JSON, use efficient data formats, or inscribe images in a suitable resolution. The user will be fetching these from a Bitcoin node (potentially via a local indexer), which is generally fine but not as fast as a CDN. Caching strategies can help (browsers will cache fetched inscription content by URL, which is usually the inscription ID or satpoint URL, so subsequent loads are faster as long as the ord server supports HTTP caching). Also consider using incremental loading – don’t block the app from showing base content while expansions load; load them asynchronously so the UI remains responsive.

* **Costs:** Inscribing the core and expansions costs transaction fees. The more data (and the more often you update manifests), the more cost to you as the developer. It’s trivial compared to running servers long-term, but it’s something to budget. Also, if you plan to allow **user-generated expansions** on-chain, consider who bears that cost (likely the user in that case). With your own expansions, you have full control – you choose when and what to inscribe.

* **Sat Ownership and Control:** To re-inscribe on a specific satoshi, you must control the UTXO that contains that sat. In practice, after you inscribe something, the sat will be in the output of the reveal transaction (often locked in a taproot output under a certain script controlled by ord). You need to then spend that output with the ord wallet to inscribe again on the same sat. This means **you cannot easily split the sat off or combine it**; you have to manage it carefully through the ord wallet’s UTXO control features. The ord client’s `--payment` or coin control options let you specify UTXOs for inscribing – use those to target the sat. If you ever accidentally send that sat elsewhere, you’d lose the anchor (though the inscriptions already made on it remain, you just couldn’t add more). So treat your anchor sats as precious and don’t mix them with other funds. Some creators even send the sat to themselves in a separate address after each inscription to maintain a clean state. All this is to say: **operationally manage your anchor sats** diligently.

* **Manifest Size Management:** If you use an on-chain manifest and it grows with each expansion, eventually it could become large (imagine 100 expansions, the JSON might be quite big if each has metadata). A large manifest means more cost to update (because each new version rewrites the whole list). One optimization could be to not include full metadata for older expansions in newer manifest versions if the base already has them cached – but since the base is stateless on each run, that doesn’t quite apply. Alternatively, you might break manifest into sections (like one per category) or stop updating a single manifest at some point in favor of a second manifest. These are edge cases; most likely the number of expansions is moderate.

* **Security of Loaded Code:** If expansions are code, you should only load code you trust (likely authored by you or vetted contributors). An Ordinals inscription can’t inherently hack the user’s machine beyond what a normal web page could do (and they are typically sandboxed similarly), but malicious code could, for instance, phish a user or drain a wallet if the app has access to keys (though ordinarily an inscription would not have direct wallet key access – any signing goes through the wallet’s UI). Since your expansions are part of your game, this is not a big concern, but it’s worth noting for completeness: do not design a system where arbitrary third parties can inject code into your base app via expansions unless you have sandboxing or permission checks in place.

* **MetaShrew Dependency:** If you lean heavily on MetaShrew for real-time features, ensure that the indexer is reliable. You might run multiple nodes or have a fallback to the on-chain method if MetaShrew is down. For example, your client could try a GraphQL query to MetaShrew for expansions; if it fails, fall back to using the ord endpoints directly. This way the app still functions (perhaps a bit less conveniently) even if the indexer is unavailable. MetaShrew itself is simply reading the chain, so it won’t miss anything permanently as long as it catches up later.

* **MetaShrew Customization:** One great thing is you can tailor MetaShrew exactly to your needs. If you find ord’s default indexing lacking, you can add custom index logic (like tracking particular OP\_RETURN patterns or indexing text content) by extending MetaShrew’s ord index module. For example, if each expansion inscription has a line like `project:enochian` in it, you could program MetaShrew to index only those inscriptions. This can speed up queries. The possibilities are many (the MetaShrew docs mention *infinitely many possibilities to extend inscriptions*). This is beyond the scope of on-chain coding, but good to know if you’re building a sophisticated back-end.

In conclusion, deploying an Ordinals-based app with recursive expansion is absolutely feasible with today’s tools. By inscribing your core app immutably and using recursion techniques, you achieve an **“immortal”** application that can grow over time purely through on-chain updates. Users benefit from a trustless, censorship-resistant experience – once they have the base inscription, the Bitcoin blockchain itself delivers all future content.

**Recommended Pattern Summary:** For most use cases, we recommend **using a stable satoshi as the anchor** for your app’s content. Inscribe the base on it, and for each expansion, **reinscribe on that same sat** (or use a small set of known anchors for categorization). In the base inscription, include a loader that **dynamically fetches all child inscriptions** on the anchor(s) via Ordinals recursion (using endpoints like `/r/sat/<sat>/...` to get IDs and content). This gives you maximal flexibility: the base will automatically pick up anything new. If needed, maintain a lightweight manifest or use MetaShrew to organize the content, especially if you want real-time updates or more complex querying. MetaShrew can be integrated to provide a seamless, up-to-date index of expansions, accessible through GraphQL subscriptions and queries, which the client-side can leverage for a better UX.

By following these steps and considerations, your on-chain game (or application) will be able to evolve and expand indefinitely, all while keeping the core logic immutable and verifiable on Bitcoin. This architecture achieves the goal of **an immortal, extensible Ordinals application** with no traditional servers – a milestone for decentralized gaming.

**Sources:**

* Ordinals Protocol Docs – *Recursion Endpoints* (on accessing other inscriptions and satoshis)
* Ordinals GitHub Discussion – *Sat as Stable Variable for Reinscriptions* (concept of using `/sat/N` as an anchor for state)
* Medium Article on Recursive Inscriptions – *Referencing other inscriptions to extend content*
* MetaShrew Documentation – *Custom indexing and child inscription state updates example*
