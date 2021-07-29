# SOMs_algo
Algorithm for Self Organizing Maps

## SOMS algorithm in SOMS.py [class WTU]

*From Antonio Gulli, Amita Kapoor, Sujit Pal - Deep Learning with TensorFlow 2.0 and Keras_ Regression, ConvNets, GANs, RNNs, NLP & more with TF 2.0 and the Keras API-Packt (2019)*

*Also checked (Tensorflow v1):  
http://iamthevastidledhitchhiker.github.io/2016-03-11-TF_SOM*

## How to use the SOMS

There are two examples in the *Examples* directory : 
- Classification of Argentinian meteorological stations depending on the mean annual of some variables
- Classification of the daily "Vertically Integrated Moisture Divergence" over the Pantanal from ERA5

To launch the code : 
1. Definition of the parameters
<pre><code>n_iter = 150
xdim = 5 # m  
ydim = 5 # n

# map_dim is the dimension of each input vector
map_dim = mlin.map_dim # mlin corresponds to the input class
</code></pre>

2. Launch the algorithm
<pre><code># SOM initilization and training
som = WTU(xdim, ydim, map_dim, n_iter)
som.fit(mlin.data) # mlin is the class to construct the input
</code></pre>

3. Get the output

Get the clusters (how the centroid of the cluster are defined) :

<pre><code>out = som.get_centroids()
</code></pre></pre>

Get the map vector (to which cluster does the input vector belong) :

<pre><code> map_vects = som.map_vects(mlin.dat)
</code></pre>

## Create a new project

To create a new project there are two elements to generate : 
1. the input structure which loads the data, process it for the SOMS format (to 1D vectors) and can set the data back to the original format (mostly to convert the centroids of the cluster in the original format).
2. the script to generate a netCDF for the SOMS algorithm, in order to avoir launching the SOMS each time.

In the examples there are different examples of the input structure. The output file is only available for the experiment with the VIMD variable over the Pantanal.
