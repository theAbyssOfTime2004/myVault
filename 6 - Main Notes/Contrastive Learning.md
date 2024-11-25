2024-11-25 20:43


Tags: [[DeepLearning]], [[Machine Learning]], [[Self-Supervised Learning]], [[supervised learning]]

# Contrastive Learning

### What is Constrative Learning?
- Contrastive learning is a machine learning technique that involves learning representations of data by contrasting positive and negative examples. The key idea is to learn representations that can distinguish between similar but different data samples.
### The importance of Contrastive Learning
- Supervised Learning trains models using labeled data, but acquiring high-quality labels, especially in domains like biomedical imaging, is costly and time-consuming. In fact, 80% of the time in supervised ML projects is spent on data preparation. To address this, recent Deep Learning research focuses on reducing the need for supervision through methods like Semi-Supervised, Unsupervised, and Self-Supervised Learning (SSL).

- Semi-Supervised Learning combines small labeled datasets with large unlabeled ones, while Unsupervised Learning analyzes unstructured data without labels. SSL, a hybrid approach, allows models to annotate their own data, using high-confidence predictions as ground truths for further training. This iterative process improves model accuracy and has gained attention for outperforming traditional supervised methods.

- Contrastive Learning, a key SSL technique, trains models using “positive” and “negative” sample pairs. Originally used in SSL, Contrastive Learning has since evolved further and is now being used in fully supervised and semi-supervised settings as well giving a boost in performance to existing state-of-the-art.
### How does Contrastive Learning work in Vision AI
- Contrastive Learning mimics human learning by comparing similarities and differences. For instance, even if we don’t know what otters or grizzly bears are, we can group images of the same animal by comparison.
	![[Pasted image 20241125205814.png]]

- In this approach, a sample is chosen as the “anchor,” with a “positive” sample from the same group and a “negative” sample from a different group. The model is trained to bring the anchor and positive closer together in the representation space while pushing the anchor and negative further apart.
	![[Pasted image 20241125205942.png]]

	- As shown in the example above, two images belonging to the same class lie close to each other in the embedding space (“_d+_”), and those belonging to different classes lie at a greater distance from each other (“_d-_”). Thus, a contrastive learning model (denotes by “_theta_” in the example above) tries to minimize the distance “_d+_” and maximize the distance “_d-_.”

Several techniques exist to select the positive and negative samples with respect to the anchor.

### Instance Discrimination Method
- This Contrastive Learning technique uses transformed versions of an image as positive samples and other images in the dataset as negatives. For instance, an image of a dog can be mirrored or converted to grayscale as a positive sample, while any unrelated image serves as a negative. The model minimizes the distance between the anchor and its transformed positives while maximizing the distance from negatives.
-  ![[Pasted image 20241125210550.png]]
- Some image augmentation methods popularly used for Instance Discrimination-based Contrastive Learning is listed as follows:
	-  **Color Jittering**: Randomly changes brightness, contrast, and saturation of the image, helping the model focus on shapes and edges instead of colors.
	- **Image Rotation**: Rotates images randomly (0-90°), ensuring models are rotation invariant.
	- **Image Flipping**: Mirrors images vertically or horizontally, an extension of rotation-based augmentation.
	- **Image Noising**: Adds random noise (e.g., salt-and-pepper) to teach the model to separate meaningful features from noise.
	- **Random Affine**: Applies geometric transformations that maintain lines and parallelism but alter distances and angles.
	- These augmentations enhance model robustness and improve generalization.
	- ![[Pasted image 20241125210651.png]]

### Image Subsampling/Patching method
- This class of Contrastive Learning methods breaks a single image into multiple patches of a fixed dimension (say, 10x10 patch windows). There might be some degree of overlap between the patches.
- Now, suppose we take the image of a cat and use one of its patches as the anchor while leveraging the rest as the positive samples. Patches from other images (say, one patch each of a raccoon, an owl, and a giraffe) are used as negative samples.
- ![[Pasted image 20241125210917.png]]
- 
# References
