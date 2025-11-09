=== Run information ===

Scheme:       weka.classifiers.trees.Id3 
Relation:     restaurant
Instances:    12
Attributes:   11
              alt
              bar
              fri_sat
              hungry
              patrons
              price
              rain
              reservation
              type
              wait_est
              will_wait
Test mode:    evaluate on training data

=== Classifier model (full training set) ===

Id3


patrons = Full
|  type = Burger
|  |  alt = No: No
|  |  alt = Yes: Yes
|  type = French: No
|  type = Italian: No
|  type = Thai
|  |  fri_sat = No: No
|  |  fri_sat = Yes: Yes
patrons = None: No
patrons = Some: Yes

Time taken to build model: 0 seconds

=== Evaluation on training set ===

Time taken to test model on training data: 0 seconds

=== Summary ===

Correctly Classified Instances          12              100      %
Incorrectly Classified Instances         0                0      %
Kappa statistic                          1     
Mean absolute error                      0     
Root mean squared error                  0     
Relative absolute error                  0      %
Root relative squared error              0      %
Total Number of Instances               12     

=== Detailed Accuracy By Class ===

                 TP Rate  FP Rate  Precision  Recall   F-Measure  MCC      ROC Area  PRC Area  Class
                 1,000    0,000    1,000      1,000    1,000      1,000    1,000     1,000     No
                 1,000    0,000    1,000      1,000    1,000      1,000    1,000     1,000     Yes
Weighted Avg.    1,000    0,000    1,000      1,000    1,000      1,000    1,000     1,000     

=== Confusion Matrix ===

 a b   <-- classified as
 6 0 | a = No
 0 6 | b = Yes

