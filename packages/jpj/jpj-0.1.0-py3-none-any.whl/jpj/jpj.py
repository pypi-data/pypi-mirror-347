#!/usr/bin/env python3
import argparse

import matplotlib.pyplot as plt
import numpy as np


def draw_jpj_symbol(
    radius=1,
    alpha=15,
    colored=False,
    show_plot=True,
    save_fig=True,
    show_support_points=False,
    show_support_circles=False,
    verbose=False,
    LW=15,  # LineWidth
    MS=30,  # MarkerSize
):
    def _print(x):
        if verbose:
            print(x)

    def point_on_circle(center, radius, angle_deg):
        angle_rad = np.radians(angle_deg)
        return np.array(
            [
                center[0] + radius * np.cos(angle_rad),
                center[1] + radius * np.sin(angle_rad),
            ]
        )

    def find_circle_centers(A, B, r):
        mid = (A + B) / 2
        d = np.linalg.norm(B - A)

        if d > 2 * r:
            raise ValueError(
                "No circle can pass through the points with the given radius."
            )

        h = np.sqrt(r**2 - (d / 2) ** 2)

        # Perpendicular direction
        dir = B - A
        perp = np.array([-dir[1], dir[0]]) / d

        center1 = mid + h * perp
        center2 = mid - h * perp

        return center1, center2

    def plot_circle(ax, center, radius, **kwargs):
        circle = plt.Circle(center, radius, fill=False, **kwargs)
        ax.add_artist(circle)

    def arc(cx=0, cy=0, r=1, angle_start_deg=0, angle_end_deg=180):
        # Convert degrees to radians
        angle_start = np.radians(angle_start_deg)
        angle_end = np.radians(angle_end_deg)

        # Arc points
        theta_arc = np.linspace(angle_start, angle_end, 100)
        x_arc = cx + r * np.cos(theta_arc)
        y_arc = cy + r * np.sin(theta_arc)

        return x_arc, y_arc

    def find_circumcircle(A, B, C):
        # From: https://en.wikipedia.org/wiki/Circumscribed_circle#Cartesian_coordinates_2
        z1 = A[0] + 1j * A[1]
        z2 = B[0] + 1j * B[1]
        z3 = C[0] + 1j * C[1]

        w = (z3 - z1) / (z2 - z1)

        if abs(w.imag) <= 0:
            raise ValueError(f"Points are collinear: {z1}, {z2}, {z3}")

        c = (z2 - z1) * (w - abs(w) ** 2) / (2j * w.imag) + z1
        r = abs(z1 - c)

        return np.array([c.real, c.imag]), r

    # Step 0: Define properties
    alpha_rad = np.radians(alpha)
    angle_B = 90 + alpha
    angle_C = 90 - alpha
    angle_D = 180 - alpha

    # Step 1: Define circle 1
    center1 = np.array([0.0, 0.0])

    # Step 2: Compute points on Circle 1
    point_A = point_on_circle(center1, radius, alpha)  # Point A at alpha°
    point_B = point_on_circle(
        center1, radius, angle_B
    )  # Point B at (90 + alpha)° on Circle 1

    # Step 3: Find center(s) of circle passing through A and B
    _, center2 = find_circle_centers(point_A, point_B, radius)

    # Step 4: Compute points for the third circle
    point_C = point_on_circle(
        center1, radius, angle_C
    )  # Point C at (90 - alpha)° on C1
    point_D = point_on_circle(
        center1, radius, angle_D
    )  # Point D at (180 - alpha)° on C1

    # Step 5: Find center(s) of the third circle passing through C and D
    _, center3 = find_circle_centers(point_C, point_D, radius)

    # Step 6: Find points on C2
    angle_E = np.degrees(
        np.arccos(np.sin(alpha_rad) - np.cos(alpha_rad) - center1[0] / radius)
    )
    point_E = point_on_circle(center2, radius, angle_E)

    # Step 7: Get arcs
    arc1x, arc1y = arc(*center1, radius, alpha, angle_D)
    arc2x, arc2y = arc(*center2, radius, angle_E, 270 + alpha)  # See calculations
    arc3x, arc3y = arc(*center3, radius, -90 - alpha, 180 - angle_E)  # See calculations

    # Step 9: Find circumcircle
    circumcenter, circumradius = find_circumcircle(center1, center2, center3)

    # Step 8: Plot everything
    _, ax = plt.subplots()
    plt.get_current_fig_manager().full_screen_toggle()
    ax.set_aspect("equal")
    ax.grid(False)
    ax.axis("off")
    ax.set_ylim(center1[1] - 0.125 * radius, center1[1] + 2 * radius)
    ax.set_xticks([])
    ax.set_yticks([])

    # Plot circles
    if show_support_circles:
        ax.set_xlim(center1[0] - 2 * radius, center1[0] + 2 * radius)
        ax.set_ylim(center1[1] - 1.25 * radius, center1[1] + 2.5 * radius)
        plot_circle(
            ax,
            center1,
            radius,
            color="red" if colored else "black",
            linestyle="--",
            label="Circle 1",
        )
        plot_circle(
            ax,
            center2,
            radius,
            color="green" if colored else "black",
            linestyle="-.",
            label="Circle 2",
        )
        plot_circle(
            ax,
            center3,
            radius,
            color="blue" if colored else "black",
            linestyle=":",
            label="Circle 3",
        )

    # Plot arcs
    ax.plot(
        arc1x,
        arc1y,
        color="red" if colored else "black",
        linestyle="-",
        linewidth=LW,
        label="Arc 1",
    )
    ax.plot(
        arc2x,
        arc2y,
        color="green" if colored else "black",
        linestyle="-",
        linewidth=LW,
        label="Arc 2",
    )
    ax.plot(
        arc3x,
        arc3y,
        color="blue" if colored else "black",
        linestyle="-",
        linewidth=LW,
        label="Arc 3",
    )
    plot_circle(
        ax,
        circumcenter,
        0.9 * circumradius,
        color="black",
        linestyle="-",
        linewidth=LW,
        label="Circle",
    )

    # Plot points
    if colored:
        ax.plot(
            *point_A,
            "<",
            color="green" if colored else "black",
            markersize=MS,
            label=f"Point A ({alpha}° on Circle 1)",
        )
        ax.plot(
            *point_D,
            ">",
            color="red" if colored else "black",
            markersize=MS,
            label=f"Point D ({angle_D}° on Circle 1)",
        )
        ax.plot(
            *point_E,
            "v",
            color="blue" if colored else "black",
            markersize=MS,
            label=f"Point E ({angle_E:.2f}° on Circle 2)",
        )

    if show_support_points:
        ax.plot(
            *point_B,
            "o",
            color="silver" if colored else "black",
            fillstyle="none",
            markersize=MS,
            linewidth=LW,
            label=f"Point B ({angle_B}° on Circle 1)",
        )
        ax.plot(
            *point_C,
            "o",
            color="silver" if colored else "black",
            fillstyle="none",
            markersize=MS,
            linewidth=LW,
            label=f"Point C ({angle_C}° on Circle 1)",
        )

    # Plot centers
    if show_support_circles:
        ax.plot(
            *center1,
            "o",
            color="red" if colored else "black",
            markersize=MS,
            label="Center of Circle 1",
        )
        ax.plot(
            *center2,
            "o",
            color="green" if colored else "black",
            markersize=MS,
            label="Center of Circle 2",
        )
        ax.plot(
            *center3,
            "o",
            color="blue" if colored else "black",
            markersize=MS,
            label="Center of Circle 3",
        )
        ax.plot(*circumcenter, "o", color="black", markersize=MS, label="Circumcenter")

    # Show the plot
    if colored:
        leg = ax.legend(loc="upper left", bbox_to_anchor=(1, 1))
        for legend_handle in leg.legendHandles:
            try:
                legend_handle.set_linewidth(1)
                legend_handle.set_markersize(7)
            except AttributeError:
                pass

    if save_fig:
        FIGURE_NAME = "jpj_symbol.svg"
        plt.savefig(FIGURE_NAME, bbox_inches="tight")
        print(f"Figure saved as {FIGURE_NAME}")

    if show_plot:
        plt.title(f"Led Zeppelin's John Paul Jones' symbol")
        plt.show()
    elif save_fig:
        plt.close()

    _print(
        f"""
---------------
>>> CIRCLES <<<
---------------
Circle 1:
    x: {center1[0]}
    y: {center1[1]}
Circle 2:
    x: {center2[0]}
    y: {center2[1]}  
Circle 3:
    x: {center3[0]}
    y: {center3[1]}

--------------
>>> POINTS <<<
--------------
Point A:
    x: {point_A[0]}
    y: {point_A[1]}
Point B:
    x: {point_B[0]}
    y: {point_B[1]}
Point C:
    x: {point_C[0]}
    y: {point_C[1]}
Point D:
    x: {point_D[0]}
    y: {point_D[1]}
Point E:
    x: {point_E[0]}
    y: {point_E[1]}
"""
    )


def main():
    parser = argparse.ArgumentParser(
        description="Draw Led Zeppelin's John Paul Jones' symbol.",
        epilog="\N{COPYRIGHT SIGN} 2025 Vincenzo Petrone",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-r",
        "--radius",
        metavar="R",
        type=float,
        default=1,
        help="radius of the circles (default: 1)",
    )
    parser.add_argument(
        "-a",
        "--angle",
        metavar="A",
        type=float,
        default=15,
        help="Angle in degrees (default: 15)",
    )
    parser.add_argument(
        "-c", "--colored", action="store_true", help="The symbol is plotted as colored"
    )
    parser.add_argument(
        "-n",
        "--no-plot",
        dest="show_plot",
        action="store_false",
        help="Do not show the plot window",
    )
    parser.add_argument(
        "-o", "--save-fig", dest="save_fig", action="store_true", help="Save the figure"
    )
    parser.add_argument(
        "-p",
        "--show-support-points",
        action="store_true",
        help="Show support points",
    )
    parser.add_argument(
        "-s",
        "--show-support-circles",
        action="store_true",
        help="Show support circles",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show debug prints"
    )

    args = parser.parse_args()

    draw_jpj_symbol(
        radius=args.radius,
        alpha=args.angle,
        colored=args.colored,
        show_plot=args.show_plot,
        save_fig=args.save_fig,
        show_support_points=args.show_support_points,
        show_support_circles=args.show_support_circles,
        verbose=args.verbose,
        LW=15,
        MS=30,
    )


__all__ = ["main"]
if __name__ == "__main__":
    main()
