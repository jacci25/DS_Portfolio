# Background
Neural networks, especially in computer vision, excel at complex tasks. They're composed of layers of interconnected nodes (neurons) that learn from input data. In image classification, they automatically extract features from raw pixel values.

Fashion-MNIST dataset has 60,000 training images, 10,000 testing images, in 10 classes. Each is a grayscale 28x28 pixel image representing different fashion items like T-shirts, trousers, dresses, etc.

# Experimental Setup
Fashion-MNIST was accessed via the Keras API, which offers an easy way to load the dataset. Before training, images were scaled to a range of [0, 1] and reshaped to fit the neural network's input dimensions. We considered four key aspects in our experiments:
- Learning Rates: We tested a range of learning rates to assess their impact on training dynamics and final accuracy. Learning rates of 0.001, 0.01 and 0.1 were chosen for comparison.
- Optimizers: Four different optimizers were investigated: Stochastic Gradient Descent (SGD), Adam, Nadam and RMSprop. Each optimizer was evaluated to determine its influence on convergence and final performance.
- Batch Sizes: We experimented with batch sizes of 128 and 256. Varying batch sizes can affect the stability and speed of training, as well as the generalization capabilities of the model.
- Architectures: We designed and trained for distinct neural network architectures. These varied in terms of depth and complexity, a convolutional neural network (CNN), and CNN with dropout techniques.

# Experiments
## Building The Architecture
The architecture consists of two densely connected layers. The input layer has 32 units and uses the sigmoid activation function. The input_shape parameter is specified to match the shape of our training data, which is 784 (28x28) in this case.

The output layer consists of 10 units, representing the ten unique classes in the Fashion-MNIST dataset. The activation function used in the output layer is softmax, which is suitable for multi-class classification tasks.

<img width="390" alt="image" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/3622d25b-e2d8-483a-b317-5c929ee31055">

The following will be experimenting with different settings to compile, train the network architecture as defined above with different hyperparameters 

<img width="785" alt="Screenshot 2024-05-24 at 12 16 55" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/3faad515-05f8-4a2a-918d-efb2d7d8594d">

Validation accuracy is slightly higher than training, suggesting no overfitting. Test accuracy being slightly lower is normal as it's unseen data. Loss values align with accuracy. Lower loss is better performance. Next, we'll increase epochs for more learning time. Longer training helps capture complex patterns, but watch for overfitting.

<img width="754" alt="Screenshot 2024-05-24 at 12 17 27" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/9a928340-f3fd-4146-952d-728dbfe11580">

Accuracy improved in all sets (training, validation, test) from the last run, indicating better learning of complex patterns. Lower loss values show improved prediction accuracy. Next, we'll increase the batch size for faster training, processing more samples at once. But, be cautious, very large batches can cause convergence problems.

<img width="757" alt="Screenshot 2024-05-24 at 12 18 02" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/82f3e1ad-2ceb-418a-9f43-248bb750a959">

Similar performance to the last run with a batch size of 128. Slight drop in accuracy, small rise in loss, but marginal differences. Increasing batch size didn't yield significant improvements, the model may not benefit much. Next, we'll try a higher learning rate (0.1) for faster convergence, but risk overshooting. It's a trade-off between speed and precision.

<img width="768" alt="Screenshot 2024-05-24 at 12 18 31" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/7119a367-ab3b-4b45-8e13-909cb568ed4b">

At a learning rate of 0.1, the model shows substantial improvement in training and validation accuracy. Lower loss values indicate better error minimization. In the next model, we experimented with the Adam optimizer.

<img width="765" alt="Screenshot 2024-05-24 at 12 19 12" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/add5300c-73d7-4c94-9eb2-c9cf520cb915">

With the Adam optimizer, despite significant improvements in all metrics compared to previous runs, the increasing gap between the training loss and validation loss curves suggests the presence of overfitting. As the number of epochs increases, the disparity between these two curves becomes more pronounced, and there are even instances where the validation loss surpasses the training loss. This indicates that while the model performs well on the training data, its performance on unseen data is declining, which is a possible sign of overfitting. Next, we'll try increasing the batch size.

<img width="754" alt="Screenshot 2024-05-24 at 12 19 42" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/7f257b86-c2f6-424a-9f7c-56ed834fda94">

Batch size of 256 yielded similar results to a batch size of 128. Slight drop in accuracy, a small rise in loss, but differences are marginal. Changing batch size didn't bring significant gains; the dataset or model may not benefit much. But overfitting has improved to some extent. Next, we'll raise the learning rate to 0.1 in the next training.

<img width="777" alt="Screenshot 2024-05-24 at 12 20 11" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/97fa0ecd-ef02-42b9-b04a-ac88b84b4d4b">

At a learning rate of 0.1, the model's performance changed significantly. Accuracy dropped, loss increased noticeably. This might be too high a learning rate for this dataset given both the loss curve and accuracy curve exhibit non-smooth, fluctuating patterns, causing instability and lower accuracy. Next, we'll switch to the Nadam optimizer for faster convergence.

<img width="779" alt="Screenshot 2024-05-24 at 12 20 53" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/4341a9c8-d11f-4a81-a060-980c7ac1935e">

Nadam optimizer led to overall improvement in metrics, however the increasing gap between the training loss and validation loss curves suggests the presence of overfitting. We'll experiment with the rmsprop optimizer in the next model.

<img width="771" alt="Screenshot 2024-05-24 at 12 21 43" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/2d1f0ec6-c028-4a0d-9cf1-69c59e6d81a1">

With RMSprop optimizer, the model didn't show significant improvement compared to the Nadam optimiser and it also suggests bit of overfitting given the increasing gap between the training loss and validation loss curves.

At this stage, Model 4 is the best-performing model since its test accuracy is higher than the other models, and it exhibits no overfitting compared to the others. We are considering using Optuna, an automated approach to assess if our current architecture has reached its capacity.

## Optuna – Trial
The goal of utilizing Optuna was to ascertain whether our model had reached its capacity.

We use Optuna - Trial to define different learning rates, optimizers, and batch sizes, allowing the model to automatically run and select the best combination. The Optuna best trial achieves the highest test accuracy of 0.858 when tuning the optimizer. However, when we manually tuned the hyperparameters to train our model, we observed that the test accuracy exceeded what was obtained through Optuna (Model 4 has a test accuracy of 0.867).

This discrepancy suggests that manual hyperparameter tuning led to a more effective configuration for our model. Furthermore, we can infer that the network we constructed has likely reached its maximum capacity based on the observed convergence of models to approximately 87% accuracy. This suggests that the current neural network structure is performing optimally given its architecture and the nature of the dataset. Please refer to Appendix 1 for detailed information.

## Building a Deeper Architecture
The new architecture utilizes four Dense layers with 64, 32, 32, and 10 neurons respectively, designed for a 10-class task. This deep structure, totaling 53,706 trainable parameters, enhances the model's capacity to learn intricate features and relationships in the data, leading to improved performance.

<img width="396" alt="image" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/dc7fd156-d07c-420c-821d-624c53a08f8c">

Using the best hyperparameter we obtained from the previous section to train on this deeper architecture.

<img width="736" alt="Screenshot 2024-05-24 at 12 25 39" src="https://github.com/jacci25/Data-Science-Portfolio/assets/137580685/ba834e7e-9f86-4f59-960d-d0e0d6212bab">

After increasing the complexity, the evaluation metrics show that this model has outperformed Model 4 but it has a higher validation loss which may indicate overfitting. To address this, we will introduce a dropout technique in combination with CNN.

## Building a Convolutional Neural Network (CNN) Architecture
CNNs are well-suited for tasks where there are spatial hierarchies of features. For instance, in images, features at higher levels often represent more complex patterns that are built upon simpler patterns at lower levels.







