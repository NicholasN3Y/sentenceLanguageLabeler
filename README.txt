This is the README file for A0112224B's submission
contactable at a0112224@u.nus.edu

== General Notes about this assignment ==

Place your comments or requests here for Min to read.  Discuss your
architecture or experiments in general.  A paragraph or two is usually
sufficient.

First, I read in the input file. For each line of the input file, the respective labels 
are detected based on the first character of the label.
The line excluding the label is split into 4-character gram. I chose not to use paddings.
The window is slided across the line to extract the 4 grams.
The gram is stored into the respective language dictionary as the key which values increments 
upon repeated encouter.
The gram is also placed into the gramSet which is to contain all the 4-grams encountered 
throughout the input file.

After all lines are read and processed, the LM is smoothen by doing add-one smoothing.
The cumulative count for gram instances for each Language is computed.

When input test in read, each line is converted into seperate list of 4-grams.
For each language model, we check the compute the probability by summing up the logarithmic 
probability of the gram in the resp language model.

The language model that yields the highest value is the language label of the sentence.
At the same time, we take note of the misses ( where the gram is not found in the language model)
if the ratio of misses to the number of gram in the sentence is above the threshold, then we 
label the sentence under "other".

By default, the threshold is 0.5.

We then print the result into the outputfile.


== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

build_test_LM.py
ESSAY.txt
eval.py
input.correct.txt
input.test.txt
input.train.txt
README.txt
results.txt - output upon running the program.


== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0112224B, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

I suggest that I should be graded as follows:

<Please fill in>

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>

To check on the correct syntax.
http://www.tutorialspoint.com/python/number_log.htm  
