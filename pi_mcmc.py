#!/usr/bin/env python3

import numpy
import matplotlib.pyplot as plt


def pi_mcmc(num_samples, a=1, plot=False, inside_circle=0, inside_box=0):
    """
    Monte Carlo method to estimate the value of pi.

    Fun fact: the box and circle don't even have to be spatially separated for counting!
    """
    # Generate random points in the box
    a = 1
    x = numpy.random.uniform(-a, a, num_samples)
    y = numpy.random.uniform(-a, a, num_samples)
    x2 = x**2
    y2 = y**2

    # Calculate the distance from the center
    d2 = x2 + y2

    # Count the number of points inside the circle
    a2 = a**2
    inside_circle += numpy.sum(d2 <= a2)

    # Count the number of points in the box
    half_a2 = a2 / 4
    inside_box += numpy.sum((x2 <= half_a2) & (y2 <= half_a2))

    # Estimate pi
    pi_estimate = (inside_circle / inside_box)

    # Plot the points if requested
    if plot:
        samples = numpy.min([num_samples, 10_000])
        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        ax.set_xlim(-a, a)
        ax.set_ylim(-a, a)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        ax.add_patch(plt.Circle((0, 0), a, color="green", fill=False))
        ax.add_patch(plt.Rectangle((-a / 2, -a / 2), a, a, color="green", fill=False))
        ax.add_patch(
            plt.Rectangle(
                (-a, -a),
                2 * a,
                2 * a,
                color="black",
                fill=False,
                linestyle='--',
            )
        )
        ax.scatter(x[:samples], y[:samples], s=1, alpha=0.5)
        plt.title(f"Estimated pi: {pi_estimate:.4f}")
        plt.show()

    return pi_estimate, (inside_circle, inside_box)


if __name__ == "__main__":
    inside_box = 0
    inside_circle = 0
    num_samples = 10**6
    for k in range(1_000):
        pi_estimate, (inside_circle, inside_box) = pi_mcmc(num_samples, inside_circle=inside_circle, inside_box=inside_box)
        print(f"Estimated value of pi ({k * num_samples}): {pi_estimate}")
    pi_mcmc(5_000, inside_circle=inside_circle, inside_box=inside_box, plot=True)
