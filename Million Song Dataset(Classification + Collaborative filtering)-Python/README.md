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




