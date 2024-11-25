2024-11-25 14:08


Tags:

# Creating ML pipeline from scratch
### Step 1: Data collection
- Sources of data:
	- Databases(SQL, NoSQL)
	- APIs
	- Web scraping 
	- Sensors or IoT data
- Notices: 
	- Ensure data relevance to the problem.
	- Check for data licensing and compliance.
### Step 2: Data extraction and analysis
- Key questions:
	- What is the data distribution?
	- Are there missing values or outliers?
	- What are the correlations between variables?
- Visualization:
	- Histograms, box plots, scatter plots, heatmaps.
- Data cleaning:
	- Handle missing values (e.g mean imputation, removal)
	- Treat outliers (e.g., clipping, scaling)
	- Normalize or standardize features.
	- Encode categorical variables.

### Step 3: Feature engineering
- Tasks:
	- Feature selection: Identify and keep the most relevant features.
	- Feature transformation: Apply log, scaling, or binning.
	- Create new features: Combine or extract information from existing ones

### Step 4: Model building 
- Process: 
	- Choose an approriate algorithm (e.g., linear regression, decision trees,...).
	- Split data into training, validation and testing sets.
	- Train the model using training data.


### Step 5: Model evaluation
- Metrics:
	- Regression: $RMSE$, $MAE$, $R^2$.
	- Classification: Accuracy, Precision, Recall, F1-score, ROC-AUC.
- Steps:
	- Test model on unseen data.
	- Analyze overfitting or underfitting.
### Step 6: Deployment and Monitoring
- Process:
	- Deploy model usin APIs (e.g,. Flask, FastAPI).
		- Integrate into production environment.
		- Monitor model performance and drift.
- Tools: Flask, FastAPI, Docker, MLFlow, Airflow
- 

# References
