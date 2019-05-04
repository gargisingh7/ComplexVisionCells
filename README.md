This was coded as an assignment for course in IITK. 

The first part consisted of designing complex cells that could recognize (a) triangles and (b) squares using a bank of orientation-selective 2D Gabor filters.

The second part included simulation of the visual search paradigm of Triesman (1980), where the task is to find the odd stimulus in a set of objects.

The third part has implementation of a simple version of feature integration theory, viz. assume there is a matrix each for color and shape information, and that responses must be delayed until information from all relevant stores has been retrieved.

For first part command is:
	python3 use_test.py filename
where filename can be result1.png, result2.png, result3.png, result4.png.(The filter can be used only for images with a black background and shape of colour red or blue)

For second part command is:
	python3 sim.py object_number feature_kind
where the object_number will take the number of objects(integer value>0 and <100) and type of search has to be specified as 1 for feature search and 2 for conjunction search.

For third part commannd is:
	python3 time_calc.py
This will generate a plot with reaction time on y-axis and number of objects on the x-axis.


The command:
	python3 gen.py width object_kind color
where width specifies width of grid of image, object_kind specifies triangle with 1 and square with 2, color specifies colour of image with red as 1 and blue as 2. This can be used to form single images of red/blue square/triangle.
