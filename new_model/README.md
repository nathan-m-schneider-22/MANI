## New Model
## Getting Started
To test the new model, `cd new_model` and run `python mp_webcam.py`. 

Then hold up one hand, and begin signing! The model's instantaneous prediction is displayed in the upper left side of the image and the output sentence is displayed on the lower left. 

Currently, we do not allow words with double letters (due to simplicity of sentence prediciton set up) and do not include the letters J or Z because those require movement. 

To allow the user to enter spaces and backspaces, we include a space character which is illustrated in the demo video and we use the letter X as the backspace character. This also means you cannot enter any words with the letter X. X was selected as the backspace character because it is used infrequently and 'x-ing out' something is like pressing the backspace key. 

The model is not the best at distinguishing some characters, namely a, t, and s. So the user should examine the models current output and adjust their hand position accordingly to get it to predict the correct letter. However, it is good enough that it is still possible to sign words with these letters, although the user may occasionally have to use the backspace key to ammend the model output. 


## How does the model work? 
The model has two steps - image level prediction and sentence level character additions. 

In the image level prediction stage, the model takes in an image and outputs a character. To do this, we pass the image to mediapipe, a library from Google for pose recognition, and get back locations of different landmarks on a hand, e.g., the position of an index finger. 

Next, we extract three features from the landmarks. First, we compute the normalized distance between each landmark (210 features). Next, we compute the pairwise cos(angle) between the vectors defined by each landmark. Finally, we compute the pairwise angle between the 3 unit vectors (1, 0, 0), (0, 1, 0) and (0, 0, 1) and each of the landmarks. 

TODO: For step two, we should probably be computing pairwise angle between all of hand connection vectors instead. So this is something that still needs to be added and tested.

Finally, we pass these features into an MLP that we've trained which outputs a vector with probabilites of each class. 

In the sentence level prediction step, we use a simple function (state = state + alpha*(prediction-state)), to average predictions over time (this is just exponentially weighted average) where the weights of recent vs old observations is controlled by the parameter alpha. The prediction in the above funciton is the output of the model. Then, we add a charcter to our sentence if max(state) is greater than some threshold theta. Here, I found theta = .35 and alpha = .04 to be a solid combination.  

