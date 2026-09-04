import os
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------
# 2D Transformation Matrices
# ---------------------------------------------------------

# 2D Translation
T2D = np.array([
    [1, 0, tx := 2],
    [0, 1, ty := 3],
    [0, 0, 1]
])


# 2D Scaling
S2D = np.array([
    [sx := 2, 0, 0],
    [0, sy := 2, 0],
    [0, 0, 1]
])


# 2D Rotation
theta = np.radians(45)

R2D = np.array([
    [np.cos(theta), -np.sin(theta), 0],
    [np.sin(theta),  np.cos(theta), 0],
    [0, 0, 1]
])


# ---------------------------------------------------------
# 3D Transformation Matrices
# ---------------------------------------------------------

# 3D Translation
T3D = np.array([
    [1, 0, 0, 2],
    [0, 1, 0, 3],
    [0, 0, 1, 4],
    [0, 0, 0, 1]
])


# 3D Scaling
S3D = np.array([
    [2, 0, 0, 0],
    [0, 2, 0, 0],
    [0, 0, 2, 0],
    [0, 0, 0, 1]
])


# 3D Rotation about Z-axis
R3D_Z = np.array([
    [np.cos(theta), -np.sin(theta), 0, 0],
    [np.sin(theta),  np.cos(theta), 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])


# ---------------------------------------------------------
# Print matrices in terminal
# ---------------------------------------------------------

print("\n========== 2D TRANSFORMATION MATRICES ==========")

print("\n2D Translation Matrix:")
print(T2D)

print("\n2D Scaling Matrix:")
print(S2D)

print("\n2D Rotation Matrix:")
print(R2D)


print("\n========== 3D TRANSFORMATION MATRICES ==========")

print("\n3D Translation Matrix:")
print(T3D)

print("\n3D Scaling Matrix:")
print(S3D)

print("\n3D Rotation about Z-axis Matrix:")
print(R3D_Z)


# ---------------------------------------------------------
# Create comparison figure
# ---------------------------------------------------------

fig, axes = plt.subplots(2, 3, figsize=(13, 8))

# 2D matrices
matrices_2d = [
    ("2D Translation", T2D),
    ("2D Scaling", S2D),
    ("2D Rotation", R2D)
]

# 3D matrices
matrices_3d = [
    ("3D Translation", T3D),
    ("3D Scaling", S3D),
    ("3D Rotation (Z-axis)", R3D_Z)
]


# Display 2D matrices
for ax, (title, matrix) in zip(axes[0], matrices_2d):

    ax.axis("off")

    ax.set_title(
        title,
        fontsize=12,
        fontweight="bold"
    )

    text = np.array2string(
        matrix,
        precision=2,
        suppress_small=True
    )

    ax.text(
        0.5,
        0.5,
        text,
        ha="center",
        va="center",
        fontsize=13,
        family="monospace"
    )


# Display 3D matrices
for ax, (title, matrix) in zip(axes[1], matrices_3d):

    ax.axis("off")

    ax.set_title(
        title,
        fontsize=12,
        fontweight="bold"
    )

    text = np.array2string(
        matrix,
        precision=2,
        suppress_small=True
    )

    ax.text(
        0.5,
        0.5,
        text,
        ha="center",
        va="center",
        fontsize=13,
        family="monospace"
    )


# Main title
fig.suptitle(
    "Comparison of 2D and 3D Transformation Matrices",
    fontsize=16,
    fontweight="bold"
)


# Explanation at bottom
fig.text(
    0.5,
    0.03,
    "2D transformations use 3×3 homogeneous matrices, "
    "while 3D transformations use 4×4 homogeneous matrices.",
    ha="center",
    fontsize=11
)


plt.tight_layout(rect=[0, 0.07, 1, 0.93])


# ---------------------------------------------------------
# Save output image in the same folder
# ---------------------------------------------------------

folder = os.path.dirname(os.path.abspath(__file__))

output_path = os.path.join(
    folder,
    "Q22_compare_2D_3D_matrices.png"
)

plt.savefig(
    output_path,
    dpi=150,
    bbox_inches="tight"
)

plt.show()

print("\nOutput image saved at:")
print(output_path)