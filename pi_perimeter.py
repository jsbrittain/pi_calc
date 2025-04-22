#!/usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt


def matching_decimal_places(estimate, reference=np.pi):
    est_str = f"{estimate:.16f}"
    ref_str = f"{reference:.16f}"

    est_dec = est_str.split(".")[1]
    ref_dec = ref_str.split(".")[1]

    count = 0
    for e_digit, r_digit in zip(est_dec, ref_dec):
        if e_digit == r_digit:
            count += 1
        else:
            break
    return count


def calc_pi(polygon, radius=1, last_dp: int = None, plot=False):
    outer_side_length = 2 * radius * np.tan(np.pi / polygon)
    outer_perimeter = polygon * outer_side_length
    outer_pi_calc = outer_perimeter / (2 * radius)

    inner_side_length = 2 * radius * np.sin(np.pi / polygon)
    inner_perimeter = polygon * inner_side_length
    inner_pi_calc = inner_perimeter / (2 * radius)

    accuracy = np.min(
        [
            matching_decimal_places(inner_pi_calc),
            matching_decimal_places(outer_pi_calc),
        ]
    )

    if last_dp is None or accuracy > last_dp:
        print(
            f"Pi [{inner_pi_calc:.8f}, {outer_pi_calc:.8f}]"
            f" [{accuracy} dp] ({polygon}-polygon)"
        )

    # Plot inner and outer polygons
    if plot:
        angles = np.linspace(0, 2 * np.pi, polygon + 1) + np.pi / polygon
        outer_x = radius / np.cos(np.pi / polygon) * np.cos(angles)
        outer_y = radius / np.cos(np.pi / polygon) * np.sin(angles)
        inner_x = radius * np.cos(angles)
        inner_y = radius * np.sin(angles)

        angles = np.linspace(0, 2 * np.pi, 10000 + 1)
        x = radius * np.cos(angles)
        y = radius * np.sin(angles)

        plt.fill(outer_x, outer_y, "skyblue", label=f"{polygon}-polygon")
        plt.plot(outer_x, outer_y, "dodgerblue")
        plt.fill(x, y, "powderblue", label="Circle")
        plt.fill(inner_x, inner_y, "w", label=f"{polygon}-polygon")
        plt.plot(inner_x, inner_y, "darkturquoise")
        plt.plot(x, y, "slategrey", label="Circle")

        ax = plt.gca()
        ax.set_aspect("equal", "box")
        ax.set_title(f"{polygon}-polygon")
        plt.show()

    return accuracy


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--skip",
        action="store_true",
        help="Skip calculations with ths same accuracy",
    )
    parser.add_argument(
        "-r", "--radius", type=float, default=1, help="Radius of the polygon"
    )
    parser.add_argument(
        "-pmin",
        "--polygon_min",
        type=int,
        default=4,
        help="Minimum number of sides of the polygon",
    )
    parser.add_argument(
        "-pmax",
        "--polygon_max",
        type=int,
        default=10,
        help="Maximum number of sides of the polygon",
    )
    parser.add_argument("--plot", action="store_true", help="Plot the polygons")
    args = parser.parse_args()

    if args.plot:
        plt.figure()

    accuracy = -1
    for polygon in range(args.polygon_min, args.polygon_max + 1):
        accuracy = calc_pi(
            polygon,
            radius=args.radius,
            last_dp=accuracy if args.skip else None,
            plot=args.plot,
        )
