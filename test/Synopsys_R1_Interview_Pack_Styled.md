
# Synopsys Round‑1 Interview Pack — **Top 50** (Styled)

> **Format legend:**  
> **Q** – the actual interview question (how they might ask)  
> **Answer** – short, easy explanation (beginner-friendly)  
> **Interview level answer** – crisp, recruiter/engineer-facing points you’d say in the interview  
> **Explanation** – quick reasoning/intuition  
> **Example** – tiny code or concrete illustration

---

## Section A — **DSA / Coding**

### **Q1. Merge two sorted arrays in place (A has buffer at end).**  
**Answer:** Start from the ends; place the bigger element at the end of A.  
**Interview level answer:** Two pointers `i=m-1`, `j=n-1`, `k=m+n-1`. While `j>=0`, write the larger of `A[i]` and `B[j]` into `A[k]`. Time **O(m+n)**, extra space **O(1)**. Handle `i<0`.  
**Explanation:** Filling from the back avoids overwriting unseen data.  
**Example (C++):**
```cpp
void merge(vector<int>& A, int m, const vector<int>& B, int n){
  int i=m-1, j=n-1, k=m+n-1;
  while (j>=0){
    if (i>=0 && A[i] > B[j]) A[k--] = A[i--];
    else                     A[k--] = B[j--];
  }
}
```

### **Q2. Add two numbers as linked lists (MSB first), don’t modify inputs.**  
**Answer:** Use stacks (or recursion) to add from the tail with carry.  
**Interview level answer:** Push digits of both lists into stacks; pop, add with carry, and prepend nodes. **O(m+n)** time, **O(m+n)** space.  
**Explanation:** Emulates pen‑and‑paper addition from right to left.  
**Example (C++):**
```cpp
ListNode* add(ListNode* a, ListNode* b){
  stack<int> s1, s2; 
  for (; a; a=a->next) s1.push(a->val);
  for (; b; b=b->next) s2.push(b->val);
  int c=0; ListNode* head=nullptr;
  while (!s1.empty() || !s2.empty() || c){
    int x = s1.empty()?0:s1.top(); if(!s1.empty()) s1.pop();
    int y = s2.empty()?0:s2.top(); if(!s2.empty()) s2.pop();
    int s = x + y + c; c = s/10;
    auto* n = new ListNode(s%10); n->next = head; head = n;
  }
  return head;
}
```

### **Q3. Detect a cycle and return the cycle’s start node.**  
**Answer:** Floyd’s tortoise–hare; then move one pointer to head and step both by 1.  
**Interview level answer:** Meet point exists iff cycle; re‑walking meets at entry. **O(n)** time, **O(1)** space.  
**Explanation:** Distance equations show equal steps from meet and head to entry.  
**Example:** Standard Floyd implementation.

### **Q4. Topological sort (and detect a cycle).**  
**Answer:** Use Kahn’s algorithm (BFS with in‑degrees).  
**Interview level answer:** Push all 0‑in‑degree nodes; pop, reduce neighbors; if output size < N → cycle. **O(V+E)**.  
**Explanation:** DAG must have at least one 0‑in‑degree node.  
**Example:** `queue<int>` for nodes, `vector<int> indeg` for counts.

### **Q5. Longest substring without repeating characters.**  
**Answer:** Sliding window with last‑seen index.  
**Interview level answer:** Expand `r`; on repeat set `l = max(l, last[ch]+1)`. **O(n)** with hash map.  
**Explanation:** Maintain a duplicate‑free window.  
**Example (C++):**
```cpp
int lengthOfLongestSubstring(const string& s){
  vector<int> last(256, -1); int best=0, l=0;
  for (int r=0; r<(int)s.size(); ++r){
    if (last[s[r]] >= l) l = last[s[r]] + 1;
    last[s[r]] = r; best = max(best, r-l+1);
  }
  return best;
}
```

### **Q6. Binary search: first index ≥ target (lower_bound).**  
**Answer:** Standard binary search with right‑bias.  
**Interview level answer:** While `l<r`, `mid=l+(r-l)/2`; if `a[mid] < x` → `l=mid+1` else `r=mid`.  
**Explanation:** Converges to first not‑less‑than position.  
**Example:** Manual `lower_bound`.

### **Q7. LRU Cache design.**  
**Answer:** Doubly‑linked list for recency + hash map key→node.  
**Interview level answer:** **O(1)** get/put; move node to front on access; evict tail on overflow; discuss thread‑safety.  
**Explanation:** Map gives O(1) lookup; list maintains order.  
**Example:** `list<pair<int,int>> dll; unordered_map<int, list<...>::iterator> pos;`

### **Q8. Kth smallest in a data stream.**  
**Answer:** Maintain a max‑heap of size k.  
**Interview level answer:** Push until size k; if new < top, pop & push. **O(n log k)**.  
**Explanation:** Keep only best k candidates.  
**Example:** `priority_queue<int>` in C++.

---

## Section B — **Modern C++ / Concurrency**

### **Q9. unique_ptr vs shared_ptr vs weak_ptr.**  
**Answer:** `unique_ptr` = single owner; `shared_ptr` = ref‑counted; `weak_ptr` = non‑owning to break cycles.  
**Interview level answer:** Prefer `unique_ptr`; use `shared_ptr` only when needed; use `weak_ptr` for observers/parents.  
**Explanation:** Avoid leaks from reference cycles.  
**Example:**
```cpp
struct Node { vector<unique_ptr<Node>> child; weak_ptr<Node> parent; };
```

### **Q10. Move semantics & why `noexcept` matters.**  
**Answer:** Moves transfer ownership; containers prefer moving if move is `noexcept`.  
**Interview level answer:** Mark move ctor/assign `noexcept` so `vector` can move on reallocation.  
**Explanation:** Without `noexcept`, containers may fall back to copying.  
**Example:**
```cpp
struct Buf { Buf(Buf&&) noexcept; Buf& operator=(Buf&&) noexcept; };
```

### **Q11. Prevent deadlocks when locking multiple mutexes.**  
**Answer:** Use a global lock order or `std::scoped_lock(m1,m2)`.  
**Interview level answer:** Reduce lock scope; consider try‑lock/backoff; prefer lock‑free when appropriate.  
**Explanation:** Break circular wait.  
**Example:**
```cpp
std::mutex a,b;
void f(){ std::scoped_lock lk(a,b); /* work */ }
```

### **Q12. Data race vs race condition.**  
**Answer:** Data race = unsynchronized conflicting access → UB. Race condition = timing‑dependent outcome.  
**Interview level answer:** Use atomics/mutexes; speak about happens‑before edges.  
**Explanation:** All data races are bugs in C++.  
**Example:** `std::atomic<int> x{0}; x.fetch_add(1);`

### **Q13. `string_view` lifetime trap.**  
**Answer:** Non‑owning; don’t return/view a temporary string.  
**Interview level answer:** Store as `std::string` if persistence is needed.  
**Explanation:** Never let a view outlive the data.  
**Example:**
```cpp
std::string_view bad(){ return std::string("tmp"); } // dangling
```

### **Q14. Rule of 5 (why).**  
**Answer:** If you manage resources, define dtor, copy/move ctors, copy/move assigns.  
**Interview level answer:** Ensures correct ownership & avoids double‑free; prefer RAII; default where possible.  
**Explanation:** Be explicit about lifecycle.  
**Example:** Buffer wrapper that defines all five.

---

## Section C — **Python / Automation (EDA‑style)**

### **Q15. When to use Python vs C++ in EDA automation.**  
**Answer:** Python for orchestration/parsing/reporting; C++ for heavy numeric kernels.  
**Interview level answer:** Prototype in Python, profile, port hotspots to C++ (bindings).  
**Explanation:** Balances dev speed and performance.  
**Example (Python):**
```python
import subprocess, json
rc = subprocess.run(["primetime","-file","run.tcl"], capture_output=True, text=True)
report = parse_timing(rc.stdout)   # custom parser
print(json.dumps(report, indent=2))
```

### **Q16. Multiprocessing vs asyncio for tool pipelines.**  
**Answer:** CPU‑bound sims → multiprocessing; I/O‑bound logs/download → asyncio.  
**Interview level answer:** GIL limits CPU threads; parallelize PVT corners with processes.  
**Explanation:** Choose the right concurrency model.  
**Example (Python):**
```python
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor() as ex:
    futures = [ex.submit(run_corner, c) for c in corners]
```

---

## Section D — **Linux / OS**

### **Q17. Debug a hanging job on Linux.**  
**Answer:** `top/htop` → `strace -p` → `gdb -p` → inspect locks/syscalls.  
**Interview level answer:** If I/O wait: disk/NFS; if CPU: `perf record -g`; examine threads/FDs; collect core.  
**Explanation:** Start from OS view, drill down to code.  
**Example:**
```bash
strace -p 12345
gdb -p 12345 -ex "thread apply all bt" -ex q
```

### **Q18. Find a memory leak in C++.**  
**Answer:** ASan/UBSan builds or Valgrind; fix ownership/RAII.  
**Interview level answer:** Minimal repro, symbolized stack, regression test.  
**Explanation:** Most leaks are ownership mistakes.  
**Example:**
```bash
g++ -g -fsanitize=address main.cpp && ./a.out
```

---

## Section E — **EDA / Std‑Cell Automation Basics**

### **Q19. What is Liberty `.lib` and LVF?**  
**Answer:** `.lib` describes timing/power/constraints; LVF adds variation tables.  
**Interview level answer:** Pins, timing arcs, slew/load tables, PVT; LVF works with AOCV/POCV for variation.  
**Explanation:** Tools (synthesis/STA) rely on `.lib` accuracy.  
**Example:** Parse `cell (INVX1)` delay table and pin caps.

### **Q20. STA essentials: setup/hold, WNS, TNS.**  
**Answer:** Check data meets setup/hold around clock edge. WNS = worst (most negative) slack; TNS = sum of negatives.  
**Interview level answer:** MCMM, OCV/crosstalk; gate sign‑off with WNS/TNS thresholds.  
**Explanation:** Ensures timing closure.  
**Example:** Script that parses top violating paths from `report_timing`.

### **Q21. What is SPEF and why it changes timing.**  
**Answer:** SPEF contains net R/C parasitics after routing.  
**Interview level answer:** Extracted by PEX (e.g., StarRC); STA uses `.lib` + SPEF to compute delays.  
**Explanation:** Wires dominate delay at advanced nodes.  
**Example:** Compare slack with/without SPEF.

### **Q22. LEF vs DEF vs GDS (library context).**  
**Answer:** LEF = abstract cell geometry; DEF = design placement/routing; GDS = full layout polygons.  
**Interview level answer:** Library = LEF+GDS+Verilog+Liberty; P&R uses LEF; sign‑off uses GDS/DRC/LVS; STA uses `.lib`+SPEF.  
**Explanation:** Different formats for different engines.  
**Example:** Script checks LEF pin consistency with GDS/Verilog.

### **Q23. DRC vs LVS in library QA.**  
**Answer:** DRC checks geometry rules; LVS checks layout vs schematic.  
**Interview level answer:** Must be clean before characterization; gate pipeline on sign‑off results.  
**Explanation:** Prevents downstream timing/power issues.  
**Example:** Fail build if `drc_errors>0 || lvs_mismatch`.

### **Q24. Automate characterization + timing diff.**  
**Answer:** Python pipeline: per PVT → run extractor → characterize → STA → collect WNS/TNS → compare to baseline → HTML/CSV.  
**Interview level answer:** Parallelize by corner; cache SPICE; JSON schema; thresholds to fail regressions; unique run IDs.  
**Explanation:** Turns manual steps into CI.  
**Example (Python skeleton):**
```python
def run_corner(cell, corner):
    run_starrc(cell, corner)      # PEX
    run_chars(cell, corner)       # SiliconSmart or wrapper
    rpt = run_sta(cell, corner)   # PrimeTime
    return summarize(rpt)         # {corner, WNS, TNS}

baseline = load_json("baseline.json")
current  = aggregate([run_corner(c, crn) for crn in corners])
emit_html_diff(baseline, current)
```

### **Q25. AOCV vs POCV (one‑liner).**  
**Answer:** AOCV = depth‑based derates; POCV = statistical/parametric per arc/cell.  
**Interview level answer:** Prefer LVF+POCV at advanced nodes; correlate to sign‑off STA; choose corners & σ carefully.  
**Explanation:** Better variation modeling → fewer surprises.  
**Example:** Flag regression if `ΔWNS < −0.02 ns` or `ΔTNS < −0.05 ns`.

---

## Section F — **More DSA / Systems / Advanced C++ (Q31–Q50)**

### **Q31. Reverse nodes of a linked list in groups of k.**  
**Answer:** Reverse each k‑block with three‑pointer technique; connect tails; leave remainder.  
**Interview level answer:** **O(n)** time, **O(1)** space; handle `k=1`, length<k, head updates.  
**Explanation:** Count k nodes; reverse in place; maintain `prevTail` and `blockHead`.  
**Example (C++ sketch):**
```cpp
ListNode* reverseK(ListNode* h,int k){
  ListNode *cur=h,*chk=h; for(int i=0;i<k && chk;i++) chk=chk->next;
  if(!chk) return h; // fewer than k
  ListNode *prev=nullptr,*tail=h; int c=k;
  while(c-- && cur){auto nxt=cur->next; cur->next=prev; prev=cur; cur=nxt;}
  tail->next = reverseK(cur,k);
  return prev;
}
```

### **Q32. Design an LRU Cache.**  
**Answer:** DLL for recency + hash map key→node.  
**Interview level answer:** O(1) get/put; eviction at tail; talk concurrency & eviction policy.  
**Explanation:** Classic system design building block.  
**Example:** `std::list<pair<K,V>>` + `unordered_map<K, list<...>::iterator>`.

### **Q33. Range sums with updates — Fenwick vs Segment Tree.**  
**Answer:** Both **O(log n)**; Fenwick for prefix sum/add; Segment Tree for general ops & range updates (lazy).  
**Interview level answer:** If only sum/add → Fenwick (simpler); else Segment Tree.  
**Explanation:** Choose by operation needs.  
**Example (Fenwick):** lowbit trick.

### **Q34. Next Greater Element with a monotonic stack.**  
**Answer:** Traverse from right; pop ≤ current; top is answer; push current.  
**Interview level answer:** **O(n)**; reuse pattern for daily temps/stock span.  
**Explanation:** Maintain strictly decreasing stack.  
**Example:** Standard NGE code.

### **Q35. Union‑Find (DSU) with path compression & union by rank.**  
**Answer:** Amortized ~constant for `find`/`unite`.  
**Interview level answer:** α(n) inverse Ackermann; used in Kruskal/connectivity.  
**Explanation:** Flatten trees on finds; attach smaller rank under larger.  
**Example:** parent/rank arrays.

### **Q36. Bit hacks to know.**  
**Answer:** `x & -x` (lowest set bit), `x & (x-1)` (clear lowest set bit), power‑of‑2 test `x && !(x & (x-1))`.  
**Interview level answer:** Used in Fenwick, subsets, popcount.  
**Explanation:** Two’s complement properties.  
**Example:** count bits by clearing lowest set bit loop.

### **Q37. Preventing deadlocks with multiple locks.**  
**Answer:** Global ordering or `std::scoped_lock`.  
**Interview level answer:** Backoff with try‑lock; shrink critical section; avoid shared state.  
**Explanation:** Remove circular wait.  
**Example:** `std::scoped_lock(a,b);`

### **Q38. Lock‑free basics: CAS & ABA.**  
**Answer:** `compare_exchange_(weak|strong)`; ABA when value changes A→B→A unnoticed.  
**Interview level answer:** Mitigate with tagged pointers/versioning or hazard pointers/SMR.  
**Explanation:** Weak CAS can fail spuriously; loop with reload.  
**Example:** CAS increment loop.

### **Q39. C++ memory model: acquire/release vs seq_cst.**  
**Answer:** Release on writer + acquire on reader creates happens‑before; `seq_cst` is stronger global order.  
**Interview level answer:** Use acq_rel for perf unless you need total order.  
**Explanation:** Prevents reordering issues.  
**Example:**
```cpp
data = 42;
flag.store(true, std::memory_order_release);
if (flag.load(std::memory_order_acquire)) use(data);
```

### **Q40. False sharing & cache locality.**  
**Answer:** Two hot fields on same cache line cause ping‑pong.  
**Interview level answer:** `alignas(64)`, separate hot/cold, SoA.  
**Explanation:** Cache‑line granularity (often 64B).  
**Example:** padded counters per thread.

### **Q41. SFINAE / enable_if vs C++20 Concepts.**  
**Answer:** SFINAE hides invalid overloads; Concepts give readable constraints.  
**Interview level answer:** Prefer Concepts; keep constraints in headers.  
**Explanation:** Cleaner errors & intent.  
**Example:**
```cpp
template<class T> requires std::integral<T>
T add(T a,T b){ return a+b; }
```

### **Q42. `std::string_view` pitfalls with forwarding.**  
**Answer:** Non‑owning; don’t store it unless backing string outlives it.  
**Interview level answer:** If you store, copy to `std::string`.  
**Explanation:** Avoid dangling views.  
**Example:** Returning `string_view` to a temporary is UB.

### **Q43. pImpl idiom — why/when.**  
**Answer:** Hide implementation, cut rebuilds, stabilize ABI.  
**Interview level answer:** Header has pointer; source defines impl; implement deep copy/move.  
**Explanation:** Reduces include churn & binary breakage.  
**Example:**
```cpp
class Lib { struct Impl; std::unique_ptr<Impl> p; public: Lib(); ~Lib(); Lib(Lib&&) noexcept=default; };
```

### **Q44. Polymorphic base: virtual dtor & slicing.**  
**Answer:** Make base dtor virtual; avoid passing polymorphic objects by value.  
**Interview level answer:** Use refs/pointers; NVI if needed.  
**Explanation:** Deleting via base* without virtual dtor ⇒ UB/leak.  
**Example:** `struct Base{ virtual ~Base(){} }; struct Der:Base{};`

### **Q45. Move‑only types in containers; `emplace` vs `push_back`.**  
**Answer:** `unique_ptr` fits containers; prefer `emplace` to construct in place; mark moves `noexcept`.  
**Interview level answer:** Containers use move only if noexcept to keep strong guarantees.  
**Explanation:** Better perf and safety.  
**Example:** `vec.emplace_back(std::make_unique<Foo>(x));`

### **Q46. Robust Python `subprocess` runner for EDA tools.**  
**Answer:** `subprocess.run(..., timeout, capture_output)`; sanitize env; stream logs.  
**Interview level answer:** Retries, kill process groups, structured result (rc/out/err/duration).  
**Explanation:** Tools may hang or spam logs.  
**Example:**
```python
cp = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
if cp.returncode != 0: raise RuntimeError(cp.stderr[:200])
```

### **Q47. Python testing with `pytest`.**  
**Answer:** Fixtures, `tmp_path`, `monkeypatch`, `parametrize`.  
**Interview level answer:** Golden files for log parsers; mark slow; CI matrix.  
**Explanation:** Keeps automation robust.  
**Example:**
```python
@pytest.mark.parametrize("line,ok",[("INV WNS=-0.12",True),("bad",False)])
def test_parse(line, ok): assert (parse(line) is not None) == ok
```

### **Q48. Linux perf basics & Flamegraphs.**  
**Answer:** `perf record -g` then `perf report` or flamegraph.  
**Interview level answer:** Sample with real inputs; compile with frame pointers; filter kernel/user.  
**Explanation:** Guides hotspot optimization.  
**Example:**
```bash
perf record -F 99 -g -- ./char_runner
perf script | stackcollapse-perf.pl | flamegraph.pl > flame.svg
```

### **Q49. LEF / DEF / GDS / SPEF — quick mapping.**  
**Answer:** LEF: abstract cells; DEF: design placement/routing; GDS: full geometry; SPEF: parasitics.  
**Interview level answer:** Library: LEF+GDS+Verilog+Liberty; P&R uses LEF; sign‑off uses GDS/DRC/LVS; STA uses `.lib`+SPEF.  
**Explanation:** Each serves a different stage.  
**Example:** Pipeline checks name/pin consistency across views.

### **Q50. LVF / AOCV / POCV & timing diffs automation.**  
**Answer:** LVF = statistical timing tables; AOCV = depth‑based derates; POCV = parametric σ‑based.  
**Interview level answer:** Choose sign‑off corners; parallelize by PVT; diff WNS/TNS vs baseline; set pass/fail thresholds.  
**Explanation:** Catch regressions early across cells/corners.  
**Example (pseudo):**
```python
for rpt in reports:
  for path in parse_timing(rpt):
    agg[(corner,group)].update(path.slack)
fail_if(delta.wns < -0.02 or delta.tns < -0.05)
```
