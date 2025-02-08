# TRG WEEK 10

- Evaluating, filtering, and analyzing Beer Ratings & Reviews

- Link to Dataset

- https://www.kaggle.com/datasets/abhaysharma38/beer-rating-reviews

## 1st Commit

- Initiated data.py & load_csv route to load csv in a raw HTML format.

## 2nd Commit

- Filtered the code to remove the "index" "beer/beerId" "beer/brewerId" "beer/name" "user/ageInSeconds" "user/birthdayRaw" "user/birthdayUnix" "user/gender" "user/profileName" "review/timeStruct" "review/timeUnix" "review/text"

- Retrieved every unique value listed in beer/style and printed in a separate list.

- Cleaned "beer/style" to show types of alcohol, without descriptive confusion.

- Terms shown: Ale, Altbier, Amber, Barleywine, Beer, Berliner, Bock, Braggot, Brown, Doppelbock, Dunkel, Dunkelweizen, Eisbock, Hefeweizen, IPA, Lager, Lambic, Maibock, Oatmeal, Pilsener, Pilsner, Porter, Quadrupel, Rauchbier, Saison, Schwarzbier, Scotch, Stout, Tripel, Vienna, Weissbier, Weizenbock, Wheatwine, Witbier

- Adjusted uniformity for the difference between Pilsener and Pilsner. Pilsner is the only unique value now.

## 3rd Commit

- In a bar chart, I want to visualize the average "review/overall" per "beer/style", as a bar chart.

- Route created : /average_review_chart

## 4th Commit

- In a bar chart, I want to visualize the average "review/aroma" per "beer/style", as a bar chart.

- Route created : /average_aroma_chart

## 5th Commit