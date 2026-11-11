
import random
import math


def forward(
    observation: list[int], hidden_layer: list[dict], output_layer: list[dict]
) -> list[float]:
    """Computes three action scores by passing observations through the neural network."""

    hidden_outs = hidden_outputs(hidden_layer, observation)
    outs = outputs(output_layer, hidden_outs)

    return outs


def outputs(
    output_layer: list[dict], hidden_outputs: list[float]
) -> list[float]:
        """Computes the outputs of the three out neurons."""

        output_values = []

        for output in output_layer:
            s = sigmoid_neuron(hidden_outputs, output["weights"], output["bias"])
            output_values.append(s)
        
        return output_values

def initialize_output_layer() -> list[dict]:
    """Creates three output neurons with random weights and zero biases."""

    output_layer = []

    for out_index in range(3):
        weights = [random.uniform(-1, 1) for _ in range(6)]
        bias = 0.0
        output_neuron = {"weights" : weights, "bias" : bias}
        output_layer.append(output_neuron)

    return output_layer

def hidden_outputs(
    hidden_layer: list[dict],
    observation: list[int]
) -> list[float]:
    """Computes the outputs of the six hidden neurons."""

    hidden_out = []

    for neuron_parameters in hidden_layer:
        activation = leaky_relu_neuron(
            observation,
            neuron_parameters["weights"],
            neuron_parameters["bias"]
        )
        hidden_out.append(activation)

    return hidden_out

def initialize_hidden_layer() -> list[dict]:
    """Creates six hidden neurons with random weights and zero biases."""

    hidden_layer = []

    for h_index in range(6):
        weights = [random.uniform(-1, 1) for _ in range(6)]
        bias = 0.0

        neuron_parameters = {"weights": weights, "bias": bias}
        hidden_layer.append(neuron_parameters)

    return hidden_layer


def sigmoid_neuron(inputs, weights, bias):
    return sigmoid(weighted_sum(inputs, weights, bias))

def sigmoid(z):
    s = 1/(1 + math.e ** -z)
    return s

def leaky_relu_neuron(inputs, weights, bias):
    """Computes a neuron's output using Leaky ReLU activation."""
    return leaky_relu (weighted_sum(inputs, weights, bias))

def leaky_relu(z):
    """Applies Leaky ReLU activation to a numerical input."""
    if z < 0:
        return 0.1 * z
    return z
    
def weighted_sum(inputs, weights, bias):
    """
    Calculates a neuron's weighted sum of inputs and bias.
    """
    z = 0
    for x, w in zip(inputs, weights):
        z += x * w

    z += bias

    return z



weights_h1 = [random.uniform(-1, 1) for _ in range(6)]
weights_h2 = [random.uniform(-1, 1) for _ in range(6)]
bias_h1 =  0.0
bias_h2 = 0.0
observation = [0, 1, 0, 1, 0, 0]







hidden_layer = initialize_hidden_layer()
output_layer = initialize_output_layer()
scores = forward(observation, hidden_layer, output_layer)
print(scores)