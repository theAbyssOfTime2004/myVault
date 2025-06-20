2025-04-23 00:24


Tags: [[Machine Learning]], [[data scientist]]

# Early Forest-Fire Detection Utilizing Regression Models

*Keyword: forest fire detection, lasso regression, ridge regression, linear regression*

- **Abstract summarized** : 
	- Many methods were proposed, such as Neural network models, 3d otsu method, NMDI methodology,... but all have a certain limitations.
	- Linear, Ridge and Lasso regression have been implemented and utilized for this study since they those have provided a quite decent accurate solution
	
### Introduction summarized:
- The need of early detecting forest fire has been increased since 2020 due to dry days and considerable decrease
- Traditional Models such as GLMs were used to model fire distribution 
- In this study, the authors:
	- **Propose a new approach** for detecting forest fires early.
	- **Motivation:** Previous research methods had _shortcomings_ — maybe in accuracy, speed, or practicality.    
	- **Goal #1:** Detect fires **as early as possible**, ideally _right when they start_.    
	- **Goal #2:** Help **prevent the fire from spreading**, to reduce environmental and economic damage.

- The **limitations of traditional techniques** in:
- *Classification*    
- *Object recognition*    
- *Image segmentation*    
	- Those can be **overcome by using deep learning** in vision-based systems, also the authors **prefer stage 2 models** over **stage 1** for higher accuracy, which is critical in forest fire detection to avoid false alarms or missed detections.
- There are 4 degrees of possible forest-fire:
	- 1. Early response scenario: predicted *damage area < 10ha, not been burning >= 3 hours, windspeed < 2m/s*  
	- 2. The second scenario: *burn area 10 - 30ha, burn length 3 - 8hours, windspeed 2 - 4m/s*
	- 3. The third scenario: *damage area 30 - 100ha, burn length 8 -24hours, windspeed 4-7m/s*
	- 4. The fourth scenario: *burn area >= 100ha, lasted >= 24hours, windspeed >= 7m/s*

### Literature review summarized
#### **[1]**
- **Data**: Canada Fire Database    
- **Goal**: Create new terms to describe wildfire size
- **Method**: Neural network using weather data
- **Result**: Can predict fire size early using weather (meteorological data)    
- **Limit**: Doesn’t work well for all locations
---
#### **[2]**
- **Data**: 400,000 fire images
- **Goal**: Detect fires early and estimate burned area
- **Method**: Bayesian Neural Network    
- **Result**: More accurate estimation and improving generalization
- **Limit**: Hard to train, has complex settings
---
#### **[4]**
- **Data**: Himawari-8 satellite images
- **Goal**: Find hot spots using adaptive thresholds
- **Method**: Otsu’s 3D thresholding
- **Result**: Works for small fires
- **Limit**: Only uses one image, may miss fires
---
#### **[5]**
- **Data**: Satellite data for lighting and aerosols
- **Goal**: Study how smoke affects fire activity
- **Method**: Image analysis with light/smoke data    
- **Result**: Found link between smoke levels (aerosol concentration) and the location of fires
- **Limit**: Less accurate in high-smoke areas
---
#### **[6]**
- **Data**: FLAME2 IR images
- **Goal**: Build new fire detection and modeling tools
- **Method**: MSER fire detection method
- **Result**: Low-cost techniques
- **Limit**: Only works with certain types of data
---
#### **[7]**
- **Data**: MODIS satellite, weather, and plant data
- **Goal**: Monitor global fire risk
- **Method**: NMDI index (for dryness)
- **Result**: Good for watching fire activity
- **Limit**: Doesn’t work well with all data sources
---
#### **[9]**
- **Data**: Public dataset
- **Goal**: Improve fire detection using attention layers
- **Method**: CNN with attention gates  
- **Result**: Reliable fire detection
- **Limit**: Can be confused by lighting or background
---
#### **[10]**
- **Data**: Landsat, MODIS, satellite IRRS
- **Goal**: Suggest better fire warning systems    
- **Method**: FFM-relevant IRRS algorithm
- **Result**: Evaluating the effectiveness of forest fire detection
- **Limit**: Doesn’t work well in high-latitude regions (such as mountains)
---
#### **[11]**
- **Data**: Video frames
- **Goal**: Detect fire in video    
- **Method**: Single Motion-based 
- **Result**: Reducing false alarms while not increasing computational work
- **Limit**: Not clearly stated
---
#### **[12]**
- **Data**: Landsat, MODIS, satellite IRRS    
- **Goal**: Monitor forest temperature and humidity    
- **Method**: Spatial and bi-spectral analysis    
- **Result**: Good for closely monitoring and early warnings    
- **Limit**: High energy usage
### Proposed System Summarized:
- **Techniques:**
1. **Pair Plot**
	- **Purpose**: To explore the relationships between pairs of variables.
	- **Benefit**: Helps identify distinct data clusters or the best attribute combinations for prediction.
 2. **Linear Regression**
	- **Concept**: Predicts the value of a dependent variable (Y) based on one or more independent variables (X).
	- **Formula**: `Y = c + mX`
	- **Method**: Uses the "least squares" approach to fit the best line that minimizes the difference between actual and predicted values.
	- **Limitation**: Can be unstable in the presence of multicollinearity (when predictors are highly correlated).
	![[Pasted image 20250423143331.png]]
	
 3. **Ridge Regression**
	- **Concept**: Linear regression but add Regularization (L2), introduced by Andrey Tikhonov.
	- **Use Case**: Effective when dealing with many correlated features.
	- **Cost Function**: $\min \left( ||Y - X\theta||_2^2 + \lambda ||\theta||_2^2 \right)$
	- **Advantage**: Stabilizes the model by penalizing large coefficients.
	- **Limitation**: Doesn't automatically eliminate irrelevant features.
	![[Pasted image 20250423142450.png]]
	
 4. **Lasso Regression**
	- **Concept**: A regularization method (L1) that also performs feature selection.    
	- **Full Name**: Least Absolute Shrinkage and Selection Operator (LASSO)
	- **Advantage**: Reduces some coefficients to zero, effectively removing unimportant variables.    
	- **Benefit**: Useful when many predictors are present but only a few are significant.

	![[Pasted image 20250423142800.png]]



# References
