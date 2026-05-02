---
tags: [zalo-prep, entry-test, phase-2]
---

# Phase 2 — Entry Test Sprint

**Khi nào bắt đầu**: Sau khi nộp CV và nhận email thông báo Entry Test date
**Cường độ**: 2.5h/ngày DSA + 1.5h thesis + 30 phút finals warmup (Option A constraint)

> **Option A pre-load:** ~80% nội dung tuần 1 + đầu tuần 2 đã refresh trong Phase A (11/5 → 31/5, 30 phút/ngày). Phase 2 sprint focus chính vào: Security, SQL, CV deep dive, mock test 200 câu, mock interview. Master timeline: [[01_Master_Timeline]].

---

## Tuần 1 — DSA MCQ

### Ngày 1–2 — Complexity + Array + Linked List + Stack/Queue

- [ ] Big-O — vòng lặp đơn O(n), lồng O(n²), chia đôi O(logn)
- [ ] Array operations, Linked List (trace reverse tay)
- [ ] Stack — infix to postfix, trace `A+B*C` → `ABC*+`
- [ ] Quiz: [Analysis of Algorithms](https://www.geeksforgeeks.org/algorithms-gq/analysis-of-algorithms-gq/) · [Linked List](https://www.geeksforgeeks.org/data-structures-gq/linked-list-gq/) · [Stacks](https://www.geeksforgeeks.org/data-structures-gq/stacks-gq/)

### Ngày 3–4 — Tree + BST + Heap

- [ ] Binary Tree — vẽ cây 7 node, duyệt tay cả 4 kiểu (pre/in/post/level)
- [ ] BST — insert [5,3,7,1,4], in-order = sorted
- [ ] Heap — MaxHeap insert/extract

> ⚠️ **Câu hay ra**: findMin trong MaxHeap = O(n) · findMax trong MinHeap = O(n)

- [ ] Quiz: [Trees GQ](https://www.geeksforgeeks.org/data-structures-gq/trees-gq/) · [Heap GQ](https://www.geeksforgeeks.org/data-structures-gq/heap-gq/)

### Ngày 5–6 — Sorting + Graph + Bit

- [ ] Bảng complexity — ghi tay không nhìn:

| Algorithm | Worst | Ghi chú |
|---|---|---|
| Bubble / Insertion | O(n²) | |
| Merge Sort | O(nlogn) | Stable |
| Quick Sort | **O(n²)** | Worst = dãy đã sorted |
| Heap Sort | O(nlogn) | In-place |

- [ ] Graph BFS + DFS — vẽ đồ thị 5 node, trace thứ tự duyệt từ node 1
- [ ] Bit ops: trace `5&3`, `5|3`, `5^3`, `5<<1`, `5>>1`
- [ ] Quiz: [Sorting GQ](https://www.geeksforgeeks.org/algorithms-gq/sorting-gq/) · [Graph GQ](https://www.geeksforgeeks.org/algorithms-gq/graph-traversals-gq/)

### Ngày 7 — Mock test DSA

- [ ] Vào Daynhauhoc #125201 và #112997, chép câu ra giấy
- [ ] Timer 60 phút, làm không xem tài liệu
- [ ] Phân loại câu sai: **không biết / hiểu nhầm / không chắc** → weakness list

---

## Tuần 2 — CS Fundamentals + CV Prep

### Ngày 8–9 — OOP + OS

- [ ] OOP 4 tính chất — viết tay ví dụ không nhìn. Singleton pattern — viết lại từ đầu
- [ ] Abstract class vs Interface — 5 điểm khác biệt
- [ ] Process vs Thread (5 điểm), Deadlock (4 điều kiện: Mutual Exclusion · Hold and Wait · No Preemption · Circular Wait)
- [ ] Semaphore vs Mutex
- [ ] Quiz: [OOP GQ](https://www.geeksforgeeks.org/oops-gq/) · [OS GQ](https://www.geeksforgeeks.org/operating-systems-gq/)

### Ngày 10–11 — Networking + Security

- [ ] OSI 7 layers (mnemonic: *All People Seem To Need Data Processing*), TCP vs UDP, TCP 3-way handshake, GET vs POST
- [ ] DNS flow, HTTPS vs HTTP, IPv4 vs IPv6
- [ ] AES vs RSA, SHA (one-way), SQL Injection + prevent, XSS, CSRF
- [ ] Quiz: [Networks GQ](https://www.geeksforgeeks.org/computer-networks-gq/)

### Ngày 12 — Toán rời rạc cơ bản + SQL

- [ ] SQL: JOIN types, GROUP BY vs HAVING vs WHERE, index tại sao nhanh
- [ ] LeetCode SQL: [175](https://leetcode.com/problems/combine-two-tables/) · [182](https://leetcode.com/problems/duplicate-emails/) · [183](https://leetcode.com/problems/customers-who-never-order/)

### Ngày 13 — CV Deep Dive

- [ ] Mở lại code Solazu + Tiger Tribe, viết câu trả lời ra giấy cho từng bullet CV
- [ ] MLOps project: tại sao chọn KServe/Loki/Evidently, trade-offs là gì, số liệu cụ thể

### Ngày 14 — Full mock test + Mock Interview

- [ ] Full mock 200 câu MCQ timed
- [ ] Mock interview với bạn ZTF 2025 — record lại, phân tích câu ấp úng
