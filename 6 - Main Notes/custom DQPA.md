2026-01-24 20:13


Tags: [[seminar HCMUS]]
 
# custom DQPA

**DEQA (Gốc):**
```
3 Experts riêng biệt:
├── Text-Only Expert (DeBERTa)
├── Text+Description Expert (DeBERTa + GPT-4 caption)
└── Text+Vision Expert (CLIP)
→ Ensemble: Weighted voting/averaging
```

**custom-DEQA**: 
```
Single Unified Model:
├── Text Encoder (mDeBERTa-v3) - term + context
├── Image Encoder (SigLIP/ResNet-152)
└── Gated-Attention Fusion
→ Direct classification
```


# References
