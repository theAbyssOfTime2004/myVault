---
tags:
  - pytorch
  - data-pipeline
  - dataloader
  - performance
created: 2026-05-02
---

# PyTorch Data Pipeline

## Vì sao data pipeline quan trọng

GPU train rất nhanh, nhưng nếu GPU phải **đứng chờ data** thì throughput giảm nghiêm trọng. Trong thực tế, data pipeline kém là nguyên nhân phổ biến nhất khiến GPU utilization thấp dù đã có card xịn.

Mục tiêu: **GPU không bao giờ idle vì chờ batch mới.**

---

## Dataset — trừu tượng hóa nguồn data

### Map-style Dataset (phổ biến nhất)

```python
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, data, labels, transform=None):
        self.data = data
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = self.data[idx]
        if self.transform:
            x = self.transform(x)
        return x, self.labels[idx]
```

DataLoader gọi `__getitem__` với index ngẫu nhiên → shuffle tự nhiên.

### IterableDataset — khi data không fit vào RAM

Map-style yêu cầu biết `len` và random access. Với dataset streaming (log files, web crawl, dataset hàng TB), dùng `IterableDataset`:

```python
from torch.utils.data import IterableDataset

class StreamingDataset(IterableDataset):
    def __init__(self, file_paths):
        self.file_paths = file_paths

    def __iter__(self):
        for path in self.file_paths:
            with open(path) as f:
                for line in f:
                    yield self.parse(line)
```

**Gotcha với multi-worker:** nếu dùng `num_workers > 0`, mỗi worker clone toàn bộ iterator → data bị lặp. Phải chia shard theo worker:

```python
def __iter__(self):
    worker_info = torch.utils.data.get_worker_info()
    if worker_info is None:
        # single-process, yield all
        yield from self.all_samples()
    else:
        # multi-process: mỗi worker lấy 1 phần
        per_worker = len(self.file_paths) // worker_info.num_workers
        start = worker_info.id * per_worker
        end = start + per_worker
        yield from self.samples_from(self.file_paths[start:end])
```

---

## DataLoader — batch hóa và song song hóa

```python
from torch.utils.data import DataLoader

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=True,
    num_workers=4,       # số process song song tải data
    pin_memory=True,     # tăng tốc CPU→GPU transfer
    prefetch_factor=2,   # mỗi worker prefetch trước 2 batch
    persistent_workers=True,  # giữ worker sống giữa các epoch
    drop_last=False,     # bỏ batch cuối nếu không đủ batch_size
)
```

### num_workers

`num_workers=0`: main process tải data (blocking).  
`num_workers=N`: N subprocess song song tải data trong khi GPU đang train batch hiện tại.

```
GPU đang train batch t
  ↕
Worker 1, 2, 3, 4 đang load batch t+1, t+2, ...
```

**Chọn num_workers bao nhiêu?** Thường bắt đầu với `4` hoặc `num_cpu_cores // 2`. Quá nhiều worker gây overhead (process spawning, memory copy) và có thể chậm hơn.

### pin_memory

RAM có hai vùng: **pageable** (OS có thể swap) và **pinned/page-locked** (không bị swap, DMA-accessible).

`pin_memory=True`: DataLoader cấp phát tensor trong pinned memory → GPU có thể DMA transfer trực tiếp, không cần copy trung gian → tăng tốc `.to(device)` đáng kể.

```python
# Không có pin_memory: CPU pageable → copy → GPU
# Có pin_memory: CPU pinned → DMA trực tiếp → GPU

batch = batch.to(device, non_blocking=True)
# non_blocking=True: transfer async, CPU không chờ GPU
```

`non_blocking=True` chỉ có tác dụng khi `pin_memory=True`.

### persistent_workers

Mặc định mỗi epoch: spawn workers → train → kill workers → lặp lại.  
`persistent_workers=True`: giữ workers sống → tiết kiệm spawn overhead giữa epoch.

---

## collate_fn — kiểm soát cách gộp samples thành batch

Mặc định DataLoader stack các tensor có cùng shape. Khi samples có **shape khác nhau** (NLP sequences, variable-length inputs), cần custom `collate_fn`:

```python
def collate_fn(batch):
    # batch = list of (input_ids, label)
    input_ids, labels = zip(*batch)

    # Pad về cùng độ dài
    input_ids = torch.nn.utils.rnn.pad_sequence(
        input_ids,
        batch_first=True,
        padding_value=0
    )
    attention_mask = (input_ids != 0).long()
    labels = torch.stack(labels)

    return {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "labels": labels
    }

loader = DataLoader(dataset, batch_size=32, collate_fn=collate_fn)
```

---

## Bottleneck profiling — CPU-bound hay GPU-bound?

Khi training chậm, cần phân biệt bottleneck nằm ở đâu.

### Kiểm tra nhanh: GPU utilization

```bash
watch -n 0.5 nvidia-smi
```

- **GPU util ~100%** liên tục → pipeline tốt, bottleneck là compute
- **GPU util dao động, hay xuống thấp** → data pipeline là bottleneck

### Dùng torch.profiler

```python
from torch.profiler import profile, record_function, ProfilerActivity

with profile(
    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
    schedule=torch.profiler.schedule(wait=1, warmup=1, active=3),
    on_trace_ready=torch.profiler.tensorboard_trace_handler('./log'),
    record_shapes=True,
    with_stack=True
) as prof:
    for step, (inputs, labels) in enumerate(loader):
        with record_function("data_to_device"):
            inputs = inputs.to(device)
        with record_function("forward"):
            outputs = model(inputs)
        with record_function("backward"):
            loss = criterion(outputs, labels)
            loss.backward()
        prof.step()

print(prof.key_averages().table(sort_by="cuda_time_total", row_limit=10))
```

Tìm dấu hiệu bottleneck trong output:
- `DataLoader` hoặc `__getitem__` chiếm nhiều CPU time → tăng `num_workers` hoặc optimize preprocessing
- `to(device)` chiếm nhiều time → bật `pin_memory + non_blocking`
- `forward/backward` chiếm đa số → pipeline ổn, bottleneck là compute

### Kỹ thuật cô lập bottleneck

```python
import time

# Đo tốc độ DataLoader thuần (không tính compute)
start = time.time()
for batch in loader:
    pass  # không làm gì với batch
print(f"Pure data time: {time.time() - start:.2f}s")

# So sánh với thời gian train thực tế
# Nếu pure data time ≈ train time → pipeline là bottleneck
```

---

## Các pattern tối ưu thường gặp

**1. Preprocessing offline:** augmentation nặng (resize ảnh lớn, tokenization) nên làm trước, lưu vào disk dạng đã processed.

**2. Cache trong RAM:** nếu dataset vừa RAM:

```python
class CachedDataset(Dataset):
    def __init__(self, dataset):
        self.cache = [dataset[i] for i in range(len(dataset))]  # load 1 lần

    def __getitem__(self, idx):
        return self.cache[idx]
```

**3. Memory-mapped files:** dataset lớn hơn RAM, dùng `numpy.memmap` hoặc `HDF5` — đọc từ disk nhưng OS cache thông minh:

```python
data = np.memmap('data.bin', dtype='float32', mode='r', shape=(N, D))
```

**4. Tách augmentation nặng khỏi DataLoader:** augmentation trên GPU nhanh hơn CPU (dùng `torchvision.transforms.v2` hoặc `Kornia`).

---

## Tóm tắt checklist

```
[ ] num_workers > 0  (không để 0 trừ khi debug)
[ ] pin_memory=True + non_blocking=True
[ ] persistent_workers=True
[ ] GPU utilization > 90% khi train
[ ] Preprocessing nặng làm offline
[ ] collate_fn cho variable-length data
```

---

## Liên kết

- [[PyTorch Autograd]]
- [[PyTorch LLM Techniques]]
