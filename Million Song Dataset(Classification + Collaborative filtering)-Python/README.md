This project focusses on building a song recommendation system using different techniques and machine learning models after analyzing dataset
## Dataset
### The Million Song Dataset (MSD)
The main dataset contains the song ID, the track ID, the artist ID, and 51 other fields, such as the year, title, artist tags, and various audio properties such as loudness, beat, tempo, and time signature.

The Million Song Dataset also contains other datasets contributed by organisations and the community,
- SecondHandSongs (cover songs)
- musiXmatch dataset (song lyrics)
- Last.fm dataset (song-level tags and similarity)
- Taste Profile subset (user-song plays)
- thisismyjam-to-MSD mapping (user-song plays, imperfectly joined)
- tagtraum genre annotations (genre labels)
- All Music genre datasets (more genre labels)

We will focus on the Taste Profile and All Music datasets.

**Taste Profile**

The Taste Profile dataset contains real user-song play counts from undisclosed organisations. All songs have been matched to identifiers in the main million song dataset and can be joined with this dataset to retrieve additional song attributes. This is an implicit feedback dataset as users interact with songs by playing them but do not explicitly indicate a preference for the song.

The dataset has an issue with the matching between the Taste Profile tracks and the million song dataset tracks. Some tracks were matched to the wrong songs, as the user data needed to be matched to song metadata, not track metadata. Approximately 5,000 tracks are matched to the wrong songs and approximately 13,000 matches are not verified. 

**MSD AllMusic Genre Dataset (MAGD)**

Many song annotations have been generated for the MSD by sources such as Last.fm, musiXmatch, and the Million Song Dataset Benchmarks by Schindler et al. The latter contains song level genre and style annotations derived from the AllMusic online music guide. We will use the MSD All Music Genre Dataset (MAGD) provided by the Music Information Retrieval research group at the Vienna University of Technology.

This dataset is included on the million song dataset benchmarks downloads page and class frequencies are provided on the MSD AllMusic Genre Dataset (MAGD) details page as well.

## Data processing
The datasets have been stored in different locations within the HDFS and they are structured as follows:

<img width="716" alt="Screenshot 2024-05-24 at 13 42 00" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/391f6ccc-e5df-4933-a1fc-abf29454ada4">

The "Million Song Dataset" contains data for one million songs, but from the data in the table above, it appears that not all secondary datasets, such as audio/features, have the full 1,000,000 songs.

Some of the tracks in the Million Song Dataset were matched to the wrong songs in the Taste Profile dataset and there is a list of song-track mismatches that were automatically identified and a list of mismatches that were manually accepted.

To remove songs that were mismatched. We began by loading two crucial files from the "tasteprofile/mismatches" directory into Spark, creating dataframes named "matches_manual" and "mismatches_automatic.", with one representing manual acceptance and the other automatic identification of mismatches. 

Then we used regular expressions to extract the Song_ID and Track_ID from the "value" column in both DataFrames and performed a check for any common values between them by using inner join. Upon discovering a common value, we removed it from the "mismatches_automatic" dataframe using a left_anti join operation. 

Subsequently, we imported the Taste Profile dataset triplets into Spark, forming the "taste_triplets" dataframe. Another left_anti join operation was employed to effectively remove the data points associated with the mismatches.

In the "data/msd/audio" directory, there are two subdirectories named "attributes" and "features." Both of these directories contain files with attribute information and feature datasets. Importantly, the attribute files and feature datasets share a common prefix, and the attribute types are consistently named.

So, in order to define schemas for the audio feature datasets based on the audio attribute datasets, I defined a function based on the prefix. This function is capable of automatically generating corresponding schemas for different prefixes. One of the requirements for the  schemas is it should include attribute types, and I achieved this by extracting all the attribute types that appear in the files within the audio attribute datasets. ‘StructType’ was used to  define the schema. For each row I extracted the attribute name and type. To maintain consistency, I mapped attribute types to corresponding spark data types using a type_mapping dictionary. If the attribute type was present in this dictionary, I created a StructField and incorporated it into the schema.

## Audio similarity
Explore using numerical representations of a song’s audio waveform to predict its genre.

There are multiple audio feature datasets, with different levels of detail.I selected the smallest one, which is the "msd-jmir-methods-of-moments-all-v1.0.csv to explore.

Features with correlations equal to or greater than 0.95 were considered strongly correlated. Therefore, we could find that Method_of_Moments_Overall_Average_4 and Method_of_Moments_Overall_Average_5 were strongly correlated, with the correlation of 0.98. 

For loading the MAGD, the schema is defined and then data is loaded from the file msd-MAGD-genreAssignment.tsv.

For doing visualisation, we look to the columns track_id and genre. Since both the variables are qualitative, we used a bar plot between track_id ncount and grouped it by genre.

<img width="452" alt="image" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/5e76a0ba-f473-492f-9f3a-7a43f508edd5">

Then merge the genres dataset and the audio features dataset so that every song has a label.

Three classification models that are used are: 
- Logistic Regression
- Random Forests
- Gradient-Boosted Trees (GBT)

These models are used as they have high predictive accuracy and easy interpretability. Moreover, the existance of multicollinearity so using other models is not a good choice.

Moreover, I removed one of the highly correlated columns-- "Method_of_Moments_Overall_Average_4" when conducting Logistic Regression, then data scaling was applied as well for all three models

**When building the model, first try a binary classification model.** I converted the genre column into a binary column that represents if the song is ”Electronic” or some other genre.

<img width="344" alt="Screenshot 2024-05-24 at 14 36 25" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/368061ce-d0a6-4bbb-abdf-c7f2c06dae33">

It is obvious that both datasets exhibit an imbalanced class distribution. In both cases, Class 0 (representing songs of other genres) significantly outweighs Class 1 (Electronic genre).

To ensure that the class balance is preserved, I employed stratified random sampling when splitting the dataset into training and test sets. This approach is crucial when dealing with imbalanced datasets, as it guarantees that both classes (Electronic genre and other genres) are adequately represented in both the training and test sets. For the training set, I selected 80% of the rows for each class using the calculated row numbers and the remaining 20% for the testing set.

I tried resampling method such as subsampling, oversampling, or observation weighting.

<img width="732" alt="Screenshot 2024-05-24 at 14 39 30" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/abab0229-9858-4470-b6bb-05ff5923b9cd">

Since our goal is to predict the genre of songs, especially in scenarios involving class imbalance, Precision and Recall should be the good performance metric. 

Logistic Regression consistently demonstrated modest performance across all sampling methods. Its precision remained low, indicating a high false positive rate, while recall was extremely low, suggesting it struggled to capture true positive cases. 

Random Forest showed mixed results. Without any sampling, it performed poorly with an F1 score of 0, signifying its inability to classify the Electronic genre correctly. Subsampling and oversampling improved its performance somewhat, with better precision, recall, and F1 score. However, the improvements were not sufficient for it to excel. 

GBT consistently outperformed other algorithms in terms of F1 score, precision, and recall. It exhibited the most balanced performance across all sampling methods. GBT's capability to capture complex relationships and adapt to class imbalance contributed to its superior performance. However, GBT was not immune to the effects of class imbalance, and its performance varied based on sampling methods. Subsampling notably improved its performance, making it the most successful algorithm in addressing the class imbalance issue.

Class balance significantly affected the performance of the algorithms. In scenarios where the Electronic genre was underrepresented, as seen in the imbalanced class distribution, models struggled to identify and classify Electronic genre samples. This led to low recall rates, high false negatives, and ultimately lower F1 scores. The class imbalance skewed the models' predictions toward the majority class, resulting in suboptimal performance, especially for Logistic Regression and Random Forest.

Hyperparameter tuning was not conducted due to the system capacity. But I got to think about this in theory.

Steps to tune GBT hyperparameters:

1.	Define the hyperparameter grid
I will tune three hyperparameters: learning_rate, max_depth, and the n_estimators.
learning_rate = [0.01, 0.1, 1, 5, 10, 100]
max_depth = [1, 3, 5, 7, 9, 11]
n_estimators = [5, 20, 50, 100, 200, 500]
I choose a wide range of hyperparameter values with the intention of finding the optimal value.

2.	Perform cross-validation
Use 10-Fold Cross-Validation to evaluate the GBT model's performance with different hyperparameter combinations.

3.	Grid search
The grid search will train and evaluate the GBT model with all possible combinations of hyperparameters in the grid.

4.	Compare the performance metrics (e.g., precision, accuracy, recall, F1 score) for different hyperparameter combinations. Then select the hyperparameter combination that maximizes the highest F1 score. Finally train a final GBT model on the entire dataset using the chosen hyperparameters.

I expect hyperparameter tuning can lead to a moderate improvement in accuracy if it can better capture the underlying patterns within the data and balance precision and recall.

**Next to predict across all genres instead.**
GBT and random forest can both handle multiclass classification, however the GBTClassifier in Spark ML currently only supports binary classification. So I choose random forest to explain how it can predict one class out of multiple classes.

- Convert the genre column into an integer index that encodes each genre consistently.
- Split dataset into training and test sets, then train by using random forest

Based on the results of the metrics_df dataframe, the model showed a relatively strong performance for Class 0, with high precision (approximately 99.28%) and moderate recall (around 57.16%). This indicated that the model can accurately predict and identify instances of Class 0. In addition, for Class 1, the model's performance was notably limited, with a precision of approximately 10.13% and a recall of around 52.05%. This implied that the model had a relatively low ability to make accurate positive predictions for Class 1 instances. Additionally, it could only identify about half of the actual Class 1 instances, which results in a lower recall. For the remaining classes (e.g., Classes 2 to 20), the model's performance was very poor, as both precision and recall were essentially zero. This implied that the model struggled to make accurate predictions or correctly identify positive instances for these classes.

The results further highlight the challenge posed by class imbalance. Since there is an uneven distribution of data among the classes, the model may become skewed toward predicting the majority class (Class 0) and may not effectively learn the minority classes due to limited data. So I tried the downsampling the training set to ensure that the proportion of each class is approximately equal and the new output suggested that the model was now capable of making positive predictions for a greater number of classes.

<img width="594" alt="Screenshot 2024-05-24 at 14 59 54" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/5c9a8e99-0670-44bc-8be6-7a25f5fd0ac8">

## Song recommendations based on collaborative filtering
Taste Profile dataset was used to develop a song recommendation service based on collaborative filtering.

There are 378310 unique songs and 1019318 unique users in the dataset.

To determine how many different songs the most active user has played, first I identified the most active user based on the total song play counts, then calculate the number of different songs played by this most active user. So the most active user has played 195 different songs, which makes up 0.05% of the total unique songs in the dataset.

**Visualize the distribution of song popularity and the distribution of user activity**

The distributions in the plots can be described as heavy-tailed power law distributions. The first plot, “Distribution of Song Popularity , there are a few songs with very high popularity, but most songs have lower popularity. The long tail indicates that there are a few songs with extremely high popularity. While for the second plot, “Distribution of User Activity”, suggests that most users have low activity counts, but there are a few users with very high activity counts. 

<img width="683" alt="Screenshot 2024-05-24 at 15 04 38" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/10efc069-dcab-412d-bca8-d21ee4d89016">

**train the collaborative filtering model**

Collaborative filtering determines similar users and songs based on their combined play history. Songs which have been played only a few times and users who have only listened to a few songs will not contribute much information and are unlikely to improve the model.

- I created a clean dataset of user-song plays by removing songs which have been played less than 38 times and users who have listened to fewer than 102 songs in total. These values represent the top 0.01% of the total number of songs and users respectively.
- Split the dataset into training and test sets.

Note that due to the nature of the collaborative filtering model, we must ensure that every user in the test set has some user-song plays in the training set as well. Because collaborative filtering models identify patterns in user behavior by analyzing historical user interactions with songs. If a user has no historical interactions in the training set, the model has no basis for understanding their preferences. Without this information, it's challenging to make meaningful recommendations for such users. Also, to evaluate the model's performance, it's necessary to compare the model's recommendations to the actual user interactions. If a user has no plays in the training set but appears in the test set, it becomes impossible to assess the model's ability to recommend items for that user. 

So I performed a left-anti join between the test set and the training set on the "User" column to identify users from the test set that do not exist in the training set. Then I did another left-anti join to exclude the users who were identified in the previous step to get the new test set.

- ALS recommendation model was trained for implicit feedback with parameters like the maximum number of iterations (5), regularization strength (0.01), and specified columns for users, items (songs), and ratings (PlayCount).

From the output, we noticed that there was little or no overlap between the recommendations and the relevant songs, indicating that the model is not providing relevant suggestions. To some extent, it does raise concerns about the effectiveness of the collaborative filtering model, especially for the users in this particular small sample.

- Performance metrics
  
<img width="442" alt="Screenshot 2024-05-24 at 15 14 52" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/9a7e4084-7351-46b0-aa59-0a95b42b8dfa">

According to the metrics, on average, about 3.24% of the top 10 recommendations are relevant to users, demonstrating the precision of the recommendations. However, the MAP at 10 is relatively low, indicating that the ranking quality of the top 10 recommendations is not very high, considering both precision and ranking. On the other hand, the NDCG at 10 is higher, suggesting a relatively better ranking quality for the top 10 recommendations, considering both relevance and position in the ranking.

These three metrics are all offline metric, which based on historical interactions and do not directly consider real-time user feedback or the actual impact on users. Metrics are based on the assumption that users provide implicit feedback, which may not always reflect their true preferences. In addition, metrics like Precision and NDCG are highly influenced by the choice of K, which can be somewhat arbitrary and can significantly affect the results. Different K values may lead to different assessments of recommendation quality, making it challenging to determine the "best" value.

In a real-world scenario, it's valuable to compare two recommendation services using A/B testing. Randomly assign users to two groups: one exposed to Service A recommendations and the other to Service B recommendations. Measure user engagement, conversion rates, and other relevant business metrics over time, which can provide direct insights into how users react to the recommendations in a real-world context.

Conversion rate and user retention can be useful. The conversion rate measures how effectively recommendations drive user interactions, such as song clicks or listens, providing a direct indicator of recommendation success. Simultaneously, user retention evaluates whether recommendations contribute to keeping users engaged and returning to the platform over time, highlighting the long-term impact of the recommendation system on user satisfaction and platform loyalty.



