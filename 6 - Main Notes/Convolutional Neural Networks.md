2024-12-10 12:27


Tags: [[DeepLearning]], [[Object Detection]], [[Computer Vision]], [[Neural Networks]]

# Convolutional Neural Networks

![[Pasted image 20241210124205.png]]

## Introduction:
- CNN is a type of artificial neural networks, paticularly welll-suited for image and video analysis tasks, are widely used in computer vision, driving-cars, facial recognition and other applications.
## Approach:
- An image is made up of pixels arranged in a grid. Unlike traditional neural networks that might flatten images into simple lists, Convolutional Neural Networks (CNNs) understand that pixels next to each other are important
- Think of an image like a puzzle - each pixel is connected to its neighbors. If you break up this puzzle randomly, you lose the picture's meaning. For example, the shape of a cat's eye or a car tire depends on how its pixels are arranged.
- CNNs are smart. They look at small sections of an image at a time, using filters that can capture how pixels relate to each other. A 3x3 filter, for instance, looks at 9 pixels simultaneously, moving across the entire image.
- In digital images, each pixel has a color value between 0 and 255. In black and white images, 0 is black, 255 is white. Color images use three channels - red, green, and blue - with each channel also having values from 0 to 255. This way, CNNs can understand both the structure and the color of an image without losing important details.

The key advantage is that CNNs preserve the spatial relationships between pixels, making them much better at understanding images compared to traditional machine learning approaches.
## How it works:
- Here is a basic architecture of a CNN model:
	1. **Convolutional Layers**: The network consists of multiple convolutional layers that apply filters (small kernels) to the input image, scanning it from left to right and top to bottom. This process detects edges, shapes, and other features in the image.
	2. **Activation Functions**: After each convolutional layer, an activation function is applied to introduce non-linearity into the model. Common choices include ReLU (Rectified Linear Unit) and Sigmoid.
	3. **Pooling Layers**: The output of each convolutional layer is then downsampled using pooling layers, which reduce the spatial dimensions of the feature maps while retaining important information.
	4. **Fully Connected Layers**: The output of the convolutional and pooling layers is fed into fully connected (dense) layers to generate a final prediction.

- CNN Networks are a stack of convolutional layers that use nonlinear activation functions like ReLU and tanh to activate weights in the nodes. Each layer, after passing through activation functions, creates more abstract information for the next layers.
- Unlike traditional fully connected neural networks where every input node connects to every output node, CNNs work differently. In CNNs, layers are connected through convolution mechanisms. Each subsequent layer is the result of convolution calculations from the previous layer, creating local connections. This means each neuron in the next layer is generated from a filter applied to a local image region of the previous neuron.
- Each layer uses hundreds or thousands of different filters and combines their results. Additional layers like pooling/subsampling are used to further filter and extract useful information.
- During training, CNNs automatically learn filter values. In image classification tasks, for example, CNNs try to find optimal filter parameters in a progression from raw pixels to edges, then shapes, facial features, and finally high-level features. The final layer is used for image classification.
- The key difference is that CNNs build increasingly complex and abstract representations of the image by progressively analyzing smaller, more specific details across multiple layers.
## Dissection:
### Convolutional Layer:
- Is the first layer to extract features from the input data. This layer maintaining the correlation between pixel's features by sliding a tiny moving window accros the image. As you slide this window, you're capturing tiny bits of information about what's inside. This helps the computer understand the image's details - like edges, shapes, and patterns - without losing how these details connect to each other.
- The convolution layer works with two main things:
	1. The original image (as a matrix of pixels)
	2. A small filter (like a mini-template) or so-called kernel

- This filter slides across the image, comparing its pattern with different parts of the picture. It's basically asking, "Does this small pattern match anything here?" By doing this repeatedly, the computer learns to recognize important features in the image.
![[Pasted image 20241210130633.png]]

- Considering this 5x5 - Image matrix as input data with pixel range value from 0 - 1, and a 3x3 filter matrix.
![[Pasted image 20241210130829.png]]

- To perform the convolution operation:

	1. The 3x3 filter is "slid" across the 5x5 image matrix.
	2. At each position, the corresponding elements of the filter and image matrix are multiplied, and the sum of these products is calculated.
	3. This sum is then placed in the corresponding position in the "Convolved Feature" matrix shown in the third image.
	
	![Alt Text](https://images.viblo.asia/full/f7fdeef5-7191-4de9-9938-2238490064ca.gif)

- The combination of an image and different filters can be used to perform various image processing operations like edge detection, blurring, and sharpening.
	- When you apply different types of filters (also called kernels or convolution matrices) to an image during the convolution process, you can achieve different visual effects:
		1. Edge Detection Filters: These types of filters are designed to highlight the edges or boundaries in an image. They work by detecting rapid changes in pixel intensity, which often correspond to edges. Applying an edge detection filter can help identify the outlines of objects in the image.
		2. Blurring Filters: Blurring filters work by averaging the pixel values in a local neighborhood. This has the effect of smoothing out small-scale details and noise in the image, creating a more softened, defocused appearance. Blurring can be useful for reducing unwanted artifacts or preparing an image for further processing.
		3. Sharpening Filters: Sharpening filters do the opposite of blurring - they enhance the contrast between neighboring pixels, making edges and details appear more pronounced. This can help bring out fine textures and make the image appear more crisp and focused.
		![[Pasted image 20241210132550.png]]

### Stride:
- Stride is the number of pixels changed on the input matrix. When stride is 1, we move the kernels 1 pixel. When stride is 2, we move the kernels 2 pixels, and so on. The image below shows a convolution layer working with a stride of 2.
![[Pasted image 20241210133648.png]]

### Padding: 
- CNN Padding means adding extra pixels around the input before doing operations. This keeps the spatial info intact and prevents data loss at the edges. It also helps to keep the output size consistent with the input and makes training more stable. Padding is important for maintaining spatial integrity in CNNs.
- Padding in CNNs keeps important details, prevents problems at the edges, and controls the output size. It ensures the input data's size stays the same through the CNN layers, stopping any loss of information. Also, it is super important for making training stable, improving how well the model works, and keeping everything organized in the network.
- Types of padding:
	1. **Same Padding:** Also, the same padding adds zeros around the input image. To keep the output size equal to the input size after convolution.
	2. **Valid Padding in CNN:** Valid padding, also called 'no padding,' doesn't add any extra pixels to the input image. Causing the output feature map to shrink compared to the input. It is handy when you only want the convolution. Portion to focus on the actual data without any additional padding.
	3. **Causal Padding:** Causal padding is mainly used in tasks like natural language processing (NLP) and time-series analysis. It adds padding only to the left side of the input sequence. Also, ensuring that each output only depends on the current and past inputs, not the future ones.
	4. **Memory Foam Carpet Padding (Non-standard):** This type of padding is used under carpets, even though it's not directly related to CNNs. Its mention here shows how padding is used in various contexts. Not just in deep learning, it highlights how the term applies universally.
### Activation function:
- Activation functions in CNNs add non-linearity, helping the network learn complex patterns. They are used after the convolutional layer and before the next layer.
	- ReLU (Rectified Linear Unit) is the most common activation function in Convolutional Neural Networks because:
		1. It's super simple: f(x) = max(0, x)
		    - Keeps positive values as they are
		    - Turns negative values to zero
		2. Helps networks learn better by:
		    - Speeding up training
		    - Preventing information loss
		    - Allowing deeper networks to work effectively
		3. Computationally cheap
		    - Very fast to calculate
		    - Requires minimal processing power
	- Think of ReLU like a gatekeeper that:
		- Lets positive signals pass through
		- Blocks negative signals
		- Helps the network focus on what's important
=> This makes ReLU a go-to choice for most deep learning models, especially in computer vision tasks.
### Pooling Layers:
- Purpose:
	1. Reduce spatial dimensions of feature maps
	2. Decrease computational complexity
	3. Extract dominant features
	4. Provide translation invariance
- Main Types:
	1. Max Pooling
		- Selects the maximum value in each pooling window
		- Most commonly used
		- Retains the most important features
		- Helps capture dominant features
	2. Average Pooling
		- Calculates the average of values in each window
		- Provides smoother feature representation
		- Less aggressive than max pooling
- Common Characteristics:
	- Typically use 2x2 or 3x3 window sizes
	- Stride usually matches the window size
	- Reduces feature map dimensions by 50-75%
	- Comes after convolutional layers
	- Helps prevent overfittings
- Example
	- Input: 224x224 feature map
	- 2x2 max pooling with stride 2
	- Output: 112x112 feature map
## Summary: 
- Here is the typical workflow of a CNN for image classification:
	1. Start with input image
	 2. Apply convolution with filters and ReLU activation
	3. Reduce image size with pooling
	4. Repeat convolutional layers
	5. Flatten the data into a fully connected layer
	6. Use final activation layer (softmax) for classification
# References
