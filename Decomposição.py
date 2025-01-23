# Import necessary libraries
import numpy as np
from scipy import signal
from sklearn.decomposition import PCA, FastICA
import matplotlib.pyplot as plt

# Generate sample data
np.random.seed(0)
n_samples = 2000
time = np.linspace(0, 8, n_samples)

# Define the source signals
s1 = np.sin(2 * time)  # Signal 1 : sinusoidal signal
s2 = np.sign(np.sin(3 * time))  # Signal 2 : square signal
s3 = signal.sawtooth(2 * np.pi * time)  # Signal 3: saw tooth signal

# Stack the source signals into a matrix
S = np.c_[s1, s2, s3]

# Add noise to the source signals
S += 0.2 * np.random.normal(size=S.shape)

# Standardize the data
S /= S.std(axis=0)

# Define the mixing matrix
A = np.array([[1, 1, 1], [0.5, 2, 1.0], [1.5, 1.0, 2.0]])

# Mix the data
X = np.dot(S, A.T)

# Fit ICA and PCA models
ica = FastICA(n_components=3, whiten="arbitrary-variance")
S_ = ica.fit_transform(X)  # Reconstruct signals
A_ = ica.mixing_  # Get estimated mixing matrix

# Verify that the ICA model applies
assert np.allclose(X, np.dot(S_, A_.T) + ica.mean_)

# Compute PCA
pca = PCA(n_components=3)
H = pca.fit_transform(X)  # Reconstruct signals based on orthogonal components

# Plot results
plt.figure()

# Define the models and their corresponding names
models = [X, S, S_, H]
names = [
    "Observations (mixed signal)",
    "True Sources",
    "ICA recovered signals",
    "PCA recovered signals",
]
colors = ["red", "steelblue", "orange"]

# Plot each model
for ii, (model, name) in enumerate(zip(models, names), 1):
    plt.subplot(4, 1, ii)
    plt.title(name)
    for sig, color in zip(model.T, colors):
        plt.plot(sig, color=color)

plt.tight_layout()
plt.show()