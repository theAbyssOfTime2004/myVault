2024-12-10 12:27


Tags:

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
	2. A small filter (like a mini-template)

- This filter slides across the image, comparing its pattern with different parts of the picture. It's basically asking, "Does this small pattern match anything here?" By doing this repeatedly, the computer learns to recognize important features in the image.
![[Pasted image 20241210130633.png]]

- Considering this 5x5 - Image matrix as input data with pixel range value from 0 - 1, and a 3x3 filter matrix.
![[Pasted image 20241210130829.png]]

- To perform the convolution operation:

	1. The 3x3 filter is "slid" across the 5x5 image matrix.
	2. At each position, the corresponding elements of the filter and image matrix are multiplied, and the sum of these products is calculated.
	3. This sum is then placed in the corresponding position in the "Convolved Feature" matrix shown in the third image.
	
	![Alt Text](https://images.viblo.asia/full/f7fdeef5-7191-4de9-9938-2238490064ca.gif)
	
	
# References
