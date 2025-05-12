"""
Module for all plotting classes an functions.
"""

##### IMPORTS #####

# Standard imports
from pathlib import Path
from typing import Optional
from collections.abc import Iterable

# Third party imports
import numpy as np
import seaborn as sns  # type: ignore
from scipy import stats  # type: ignore
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.colors import to_hex

# Local imports

# Import Rules

##### CONSTANTS #####

##### CLASSES #####


##### FUNCTIONS #####
def scatter_plot(
    x_data: Iterable,
    y_data: Iterable,
    groups: Optional[Iterable] = None,
    group_colors: Optional[dict[str, str]] = None,
    density_data: Optional[Iterable] = None,
    density_label: str = "Density",
    x_label: str = "X values",
    y_label: str = "Y values",
    title: str = "Scatter Plot with Regression",
    gridsize: int = 40,
    sort_by_count: bool = False,
    plot_save_path: Optional[Path] = None,
) -> None:
    """Generates a scatter plot with regression line with optional density coloring
    and group coloring.

    Parameters
    ----------
    x_data : Iterable
        X-axis data
    y_data : Iterable
        Y-axis data
    groups : Optional[Iterable], optional
        Grouping data, by default None
    group_colors : Optional[dict[str, str]], optional
        Group colors, by default None
    density_data : Optional[Iterable], optional
        Density data, by default None
    density_label : str, optional
        Density label, by default "Density"
    x_label : str, optional
        X-axis label, by default "X values"
    y_label : str, optional
        Y-axis label, by default "Y values"
    title : str, optional
        Plot title, by default "Scatter Plot with Regression"
    gridsize : int, optional
        Density grid size, by default 40
    sort_by_count : bool, optional
        Sort groups by count, by default False
    plot_save_path : Optional[Path], optional
        Plot save path, by default None

    Raises
    ------
    ValueError
        If the input arrays do not have the same shape.
        If the groups array does not match the x and y data shape.
        If the density array does not match the x and y data shape.
    """
    # Convert to numpy arrays
    x_array = np.asarray(x_data)
    y_array = np.asarray(y_data)
    # Check they are the same dimensions
    if x_array.shape != y_array.shape:
        raise ValueError("All input arrays must have the same shape.")
    # Flatten arrays
    x_array_flatten = x_array.flatten()
    y_array_flatten = y_array.flatten()
    # Process groups if provided
    if groups is not None:
        groups_array = np.asarray(groups).flatten()
        if groups_array.shape != x_array_flatten.shape:
            raise ValueError("Groups array must have the same shape as x and y arrays.")
        groups_array_str = groups_array.astype(str)
        unique_groups = np.unique(groups_array_str)
    else:
        groups_array_str = None
        unique_groups = None
    # Process density data if provided
    if density_data is not None:
        density_array = np.asarray(density_data)
        if density_array.shape != x_array.shape:
            raise ValueError(
                "Density array must have the same shape as x and y arrays."
            )
        density_array_flatten = density_array.flatten()
    else:
        density_array_flatten = None

    # Styling
    sns.set_theme(style="whitegrid", font_scale=1.2)
    plt.rcParams.update(
        {
            "figure.facecolor": "#F8F9FA",
            "axes.facecolor": "#FFFFFF",
            "axes.edgecolor": "#3A3A3A",
            "axes.linewidth": 1.0,
            "xtick.color": "#2D2D2D",
            "ytick.color": "#2D2D2D",
            "legend.frameon": True,
            "legend.facecolor": "#FFFFFF",
            "legend.edgecolor": "#3A3A3A",
            "legend.shadow": True,
        }
    )

    # Create figure layout
    fig, ax = plt.subplots(figsize=(10, 8))
    # Statistics
    slope, intercept, r_value, _, _ = stats.linregress(x_array_flatten, y_array_flatten)
    r_squared = r_value**2
    reg_line = slope * x_array_flatten + intercept
    min_val = min(np.min(x_array_flatten), np.min(y_array_flatten))
    max_val = max(np.max(x_array_flatten), np.max(y_array_flatten))
    padding = 0.05 * (max_val - min_val)
    extent = (
        min_val - padding,
        max_val + padding,
        min_val - padding,
        max_val + padding,
    )
    # Ensure keys are strings
    if group_colors is not None:
        group_colors = {str(k): v for k, v in group_colors.items()}
    # Create color mapping if not provided
    if group_colors is None and unique_groups is not None:
        n_colors = len(unique_groups)
        if n_colors <= 12:
            base_palette = sns.color_palette("Set2", n_colors=n_colors)
        else:
            base_palette = sns.color_palette("Spectral", n_colors=n_colors)
        group_colors = {
            group: to_hex(base_palette[i % len(base_palette)])
            for i, group in enumerate(unique_groups)
        }
    # Plotting
    # Density plot
    if density_array_flatten is not None:
        cmap = sns.cubehelix_palette(rot=-0.4, gamma=0.5, as_cmap=True)
        hb = ax.hexbin(
            x_array_flatten,
            y_array_flatten,
            C=density_array_flatten,
            gridsize=gridsize,
            cmap=cmap,
            extent=extent,
            mincnt=1,
            reduce_C_function=np.sum,
            alpha=0.9,
        )
        cbar = fig.colorbar(hb, ax=ax, label=density_label, shrink=0.8)
        cbar.ax.tick_params(labelsize=10)
        cbar.outline.set_linewidth(0.7)  # type: ignore
        cbar.outline.set_edgecolor("#4D5154")  # type: ignore

    # Grouped scatter plot
    elif groups_array_str is not None:
        group_counts = {
            group: np.sum(groups_array_str == group) for group in unique_groups
        }
        if sort_by_count:
            sorted_groups = sorted(
                unique_groups, key=lambda g: group_counts[g], reverse=True
            )
        else:
            sorted_groups = sorted(unique_groups)

        for i, group in enumerate(sorted_groups):
            mask = groups_array_str == group
            color = group_colors.get(str(group), sns.color_palette("colorblind")[i])  # type: ignore
            ax.scatter(
                x_array_flatten[mask],
                y_array_flatten[mask],
                color=color,
                edgecolor="white",
                linewidth=0.5,
                alpha=0.85,
                s=32,
                label=f"{group} (n={np.sum(mask):,})",
                zorder=i + 2,
            )
    # Standard scatter plot
    else:
        ax.scatter(
            x_array_flatten,
            y_array_flatten,
            alpha=0.85,
            color="#5E8AB4",
            edgecolors="white",
            linewidth=0.5,
            s=32,
            label=f"Data Points (n={len(x_array_flatten):,})",
        )
    # Identity line
    ax.plot(
        [min_val, max_val],
        [min_val, max_val],
        linestyle="--",
        color="#888888",
        linewidth=1.2,
        label="Identity line (y = x)",
        zorder=10,
    )
    # Regression line
    ax.plot(
        x_array_flatten,
        reg_line,
        linestyle="-",
        color="#D7263D",
        linewidth=2,
        alpha=0.9,
        label=f"$y = {slope:.2f}x {'+' if intercept >= 0 else '-'} "
        f"{abs(intercept):.2f}$\n$R^2 = {r_squared:.3f}$",
        zorder=11,
    )
    # Axis limits and labels
    ax.set_xlim(min_val - padding, max_val + padding)
    ax.set_ylim(min_val - padding, max_val + padding)
    ax.set_xlabel(x_label, fontsize=13, labelpad=10)
    ax.set_ylabel(y_label, fontsize=13, labelpad=10)
    ax.set_title(title, fontsize=16, fontweight="semibold", color="#2D3033", pad=15)
    ax.grid(True, linestyle="--", alpha=0.4, color="#CCCCCC", linewidth=0.8)
    ax.legend(loc="upper left", fontsize=10)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda val, _: f"{val:,.1f}"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda val, _: f"{val:,.1f}"))
    ax.tick_params(axis="both", which="major", labelsize=10)

    plt.tight_layout()

    ## Save or show the plot
    if plot_save_path:
        plt.savefig(plot_save_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()


def data_difference_plot(
    x_data: Iterable,
    y_data: Iterable,
    groups: Optional[Iterable] = None,
    group_colors: Optional[dict[str, str]] = None,
    x_label: str = "X values",
    y_label: str = "Y values",
    data_label: str = "Data",
    sort_by_count: bool = False,
    save_path: Path | None = None,
):
    """Plots of differences between two datasets with optional grouping.

    Parameters
    ----------
    x_data : Iterable
        X-axis Data
    y_data : Iterable
        Y-axis Data
    groups : Iterable, optional
        Grouping array for coloring the scatter points, by default None
    group_colors : Dict[str, str], optional
        Dictionary mapping unique group values to specific colors, by default None
    x_label : str, optional
        Label for the x-axis, by default "X values"
    y_label : str, optional
        Label for the y-axis, by default "Y values"
    data_label : str, optional
        Name of the data/attribute being analyzed, by default "Data"
    sort_by_count : bool, optional
        Whether to sort groups by their counts, by default False
    save_path : Path | None, optional
        Path to save the figure, by default None

    Raises
    ValueError
        If the input arrays do not have the same shape.
        If the groups array does not match the x and y data shape.
        If the group colors do not match the number of unique groups.
    """
    # Convert to numpy arrays
    x_array = np.asarray(x_data)
    y_array = np.asarray(y_data)

    # Check they are the same dimensions
    if x_array.shape != y_array.shape:
        raise ValueError("All input arrays must have the same shape.")

    # Flatten arrays
    x_array_flatten = x_array.flatten()
    y_array_flatten = y_array.flatten()

    # Process groups if provided
    if groups is not None:
        groups_array = np.asarray(groups).flatten()
        if groups_array.shape != x_array_flatten.shape:
            raise ValueError("Groups array must have the same shape as x and y arrays.")
        groups_array_str = groups_array.astype(str)
        unique_groups = np.unique(groups_array_str)
        group_counts = {
            group: np.sum(groups_array_str == group) for group in unique_groups
        }
        if sort_by_count:
            sorted_groups = sorted(
                unique_groups, key=lambda g: group_counts[g], reverse=True
            )
        else:
            sorted_groups = sorted(unique_groups)
    else:
        groups_array_str = None
        unique_groups = None
        sorted_groups = None

    # Ensure keys are strings
    if group_colors is not None:
        group_colors = {str(k): v for k, v in group_colors.items()}
    # Create color mapping if not provided
    if group_colors is None and unique_groups is not None:
        n_colors = len(unique_groups)
        if n_colors <= 12:
            base_palette = sns.color_palette("Set2", n_colors=n_colors)
        else:
            base_palette = sns.color_palette("Spectral", n_colors=n_colors)
        group_colors = {
            group: to_hex(base_palette[i % len(base_palette)])
            for i, group in enumerate(unique_groups)
        }

    # Basic statistics
    diff = y_array_flatten - x_array_flatten

    # Styling
    sns.set_theme(style="whitegrid", font_scale=1.2)
    plt.rcParams.update(
        {
            "figure.facecolor": "#F8F9FA",
            "axes.facecolor": "#FFFFFF",
            "axes.edgecolor": "#4D5154",
            "axes.linewidth": 1.0,
            "xtick.color": "#2D3033",
            "ytick.color": "#2D3033",
            "legend.frameon": True,
            "legend.facecolor": "#FFFFFF",
            "legend.edgecolor": "#4D5154",
            "legend.shadow": True,
        }
    )

    # Create figure layout
    fig, axes = plt.subplots(2, 2, figsize=(16, 14))
    fig.suptitle(
        f"{x_label} vs. {y_label} Analysis of {data_label}",
        fontsize=20,
        fontweight="bold",
        color="#2D3033",
    )

    # Tick formatter
    formatter = FuncFormatter(lambda x, _: f"{x:,.1f}")

    # Title style for subplots
    title_font = {"fontsize": 15, "fontweight": "semibold", "color": "#2D3033"}

    # Default Colors
    default_scatter_color = "#5E8AB4"
    default_residual_color = "#5E8AB4"
    default_hist_color = "#5E8AB4"
    default_bland_altman_color = "#5E8AB4"

    # Colors for statistical elements
    regression_line_color = "#DC267F"
    identity_line_color = "#444444"
    mean_diff_line_color = "#000000"
    loa_line_color = "#555555"

    # Store group handles and labels for the shared legend
    group_handles: list[plt.Artist] = []
    group_labels: list[str] = []

    # 1. Scatter plot with regression
    ax1 = axes[0, 0]
    # Calculate regression
    slope, intercept, r_value, _, _ = stats.linregress(x_array_flatten, y_array_flatten)
    r_squared = r_value**2
    reg_line = slope * x_array_flatten + intercept

    # Plot scatter points
    if groups_array_str is not None:
        # Plot each group separately
        for i, group in enumerate(sorted_groups):  # type: ignore
            mask = groups_array_str == group
            group_x = x_array_flatten[mask]
            group_y = y_array_flatten[mask]
            color = group_colors.get(str(group), sns.color_palette("colorblind")[i])  # type: ignore
            scatter = ax1.scatter(
                group_x,
                group_y,
                alpha=0.8,
                color=color,
                edgecolors="white",
                linewidth=0.5,
                s=40,
                zorder=i + 2,
            )

            # Store handle and label only on the first subplot
            if i == 0 or len(group_handles) < len(sorted_groups):  # type: ignore
                group_handles.append(scatter)
                group_labels.append(f"{group} (n={len(group_x):,})")
    else:
        # Plot all points with the same color
        ax1.scatter(
            x_array_flatten,
            y_array_flatten,
            alpha=0.8,
            color=default_scatter_color,
            edgecolors="white",
            linewidth=0.5,
            s=40,
            label=f"Data Points (n={len(x_array_flatten):,})",
        )

    # Identity line
    min_val = min(np.min(x_array_flatten), np.min(y_array_flatten))
    max_val = max(np.max(x_array_flatten), np.max(y_array_flatten))
    identity_line = ax1.plot(
        [min_val, max_val],
        [min_val, max_val],
        "--",
        color=identity_line_color,
        linewidth=1.2,
        label="Identity line (y = x)",
    )[0]

    # Regression line with equation and R-squared
    regression_line = ax1.plot(
        x_array_flatten,
        reg_line,
        color=regression_line_color,
        linewidth=2,
        linestyle="-",
        alpha=0.9,
        zorder=100,
        label=f"$y = {slope:.2f}x {'+' if intercept >= 0 else '-'} "
        f"{abs(intercept):.2f}$\n$R^2 = {r_squared:.3f}$",
    )[0]

    # Labels and title
    ax1.set_xlabel(f"{x_label} {data_label}", fontsize=13)
    ax1.set_ylabel(f"{y_label} {data_label}", fontsize=13)
    ax1.set_title("Pre vs. Post Scatter Plot", fontdict=title_font)

    # Add subplot-specific legend (no group info)
    ax1.legend(
        handles=[identity_line, regression_line],
        loc="upper left",
        fontsize=10,
        shadow=True,
    )

    ax1.grid(True, linestyle="--", alpha=0.4, color="#CCCCCC")
    ax1.tick_params(axis="both", which="major", labelsize=10)
    ax1.xaxis.set_major_formatter(formatter)
    ax1.yaxis.set_major_formatter(formatter)

    # 2. Residual plot
    ax2 = axes[0, 1]
    # Plot residuals with grouping if provided
    if groups_array_str is not None:
        # Plot each group separately
        for i, group in enumerate(sorted_groups):  # type: ignore
            mask = groups_array_str == group
            group_x = x_array_flatten[mask]
            group_diff = diff[mask]
            color = group_colors.get(str(group), sns.color_palette("colorblind")[i])  # type: ignore
            ax2.scatter(
                group_x,
                group_diff,
                alpha=0.8,
                color=color,
                edgecolors="white",
                linewidth=0.5,
                s=30,
                zorder=i + 2,
            )
    else:
        # Plot all points with the same color
        ax2.scatter(
            x_array_flatten,
            diff,
            alpha=0.8,
            color=default_residual_color,
            s=30,
            edgecolors="white",
            linewidth=0.5,
        )

    zero_line = ax2.axhline(
        y=0,
        color=identity_line_color,
        linestyle="--",
        alpha=0.8,
        linewidth=1.2,
        label="Zero difference",
    )
    ax2.set_xlabel(f"{x_label} {data_label}", fontsize=13)
    ax2.set_ylabel(f"Residuals ({y_label} - {x_label})  {data_label}", fontsize=13)
    ax2.set_title("Residual Plot", fontdict=title_font)
    ax2.grid(True, linestyle="--", alpha=0.4, color="#CCCCCC")
    ax2.tick_params(axis="both", which="major", labelsize=10)
    ax2.xaxis.set_major_formatter(formatter)
    ax2.yaxis.set_major_formatter(formatter)

    # Add legend for zero line only
    ax2.legend(handles=[zero_line], loc="best", fontsize=10, shadow=True)

    # 3. Histogram of differences
    ax3 = axes[1, 0]
    if groups_array_str is not None:
        bin_edges = np.histogram_bin_edges(diff, bins=30)
        width = (bin_edges[1] - bin_edges[0]) / len(
            sorted_groups  # type: ignore
        )  # Calculate bar width
        all_percentages: list[float] = (
            []
        )  # Track all percentages to set appropriate y-axis limits

        # Calculate the total count of all data points for overall percentage calculation
        total_count = len(diff)

        for i, group in enumerate(sorted_groups):  # type: ignore
            mask = groups_array_str == group
            group_diff = diff[mask]
            color = group_colors.get(str(group), sns.color_palette("colorblind")[i])  # type: ignore
            # Calculate histogram data for the current group
            hist, _ = np.histogram(group_diff, bins=bin_edges)  # density=False here

            # Calculate percentages relative to the total dataset
            percentages = (hist / total_count) * 100
            all_percentages.extend(percentages)

            # Calculate the x positions for the bars of the current group
            x_positions = bin_edges[:-1] + i * width
            ax3.bar(
                x_positions,
                percentages,
                width=width,
                alpha=0.6,
                color=color,
                edgecolor="#555555",
                linewidth=0.5,
            )
        # Adjust y-axis scale for grouped data too
        max_percentage = max(all_percentages) if all_percentages else 5
        # Add 20% padding above the maximum percentage
        ax3.set_ylim(0, max_percentage * 1.2)
    else:
        # In the non-grouped case, this is already showing percentages of the total
        n, _, patches = ax3.hist(
            diff,
            bins=30,
            alpha=0.6,
            color=default_hist_color,
            edgecolor="#555555",
            linewidth=0.5,
        )
        # Calculate percentages for each bin
        percentages = (n / len(diff)) * 100
        # Override the bar heights with percentages
        for patch, percentage in zip(patches, percentages):
            patch.set_height(percentage)
            patch.set_y(0)  # Ensure bars start from y=0
        # Adjust y-axis scale to better fit the data distribution
        max_percentage = max(percentages) if len(percentages) > 0 else 5  # type: ignore
        # Add 20% padding above the maximum percentage
        ax3.set_ylim(0, max_percentage * 1.2)

    zero_line_hist = ax3.axvline(
        x=0,
        color=identity_line_color,
        linestyle="--",
        alpha=0.8,
        linewidth=1.2,
        label="Zero difference",
    )
    ax3.set_xlabel(f"Difference ({y_label} - {x_label}) {data_label}", fontsize=13)
    ax3.set_ylabel("Frequency (%)", fontsize=13)
    ax3.set_title("Distribution of Differences", fontdict=title_font)
    ax3.grid(axis="y", linestyle="--", alpha=0.4, color="#CCCCCC")
    ax3.tick_params(axis="both", which="major", labelsize=10)
    ax3.xaxis.set_major_formatter(formatter)
    ax3.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f"{y:.1f}%"))

    # Add legend for zero line only
    ax3.legend(handles=[zero_line_hist], loc="best", fontsize=10, shadow=True)

    # 4. Bland-Altman plot
    ax4 = axes[1, 1]
    mean = (x_array_flatten + y_array_flatten) / 2
    # Calculate Bland-Altman statistics for all data
    mean_diff = np.mean(diff)
    std_diff = np.std(diff)
    limit_of_agreement = 1.96 * std_diff

    # Plot scatter points with grouping if provided
    if groups_array_str is not None:
        # Plot each group separately
        for i, group in enumerate(sorted_groups):  # type: ignore
            mask = groups_array_str == group
            group_mean = mean[mask]
            group_diff = diff[mask]
            color = group_colors.get(str(group), sns.color_palette("colorblind")[i])  # type: ignore
            ax4.scatter(
                group_mean,
                group_diff,
                alpha=0.8,
                color=color,
                edgecolors="white",
                linewidth=0.5,
                s=30,
                zorder=i + 2,
            )
    else:
        # Plot all points with the same color
        ax4.scatter(
            mean,
            diff,
            alpha=0.8,
            color=default_bland_altman_color,
            s=30,
            edgecolors="white",
            linewidth=0.5,
        )

    # Draw reference lines (based on all data)
    mean_line = ax4.axhline(
        y=mean_diff,
        color=mean_diff_line_color,
        linestyle="-",
        alpha=0.8,
        linewidth=2.0,
        label=f"Mean diff: {mean_diff:.3f}",
    )
    upper_loa = ax4.axhline(
        y=mean_diff + limit_of_agreement,
        color=loa_line_color,
        linestyle="--",
        alpha=0.8,
        linewidth=1.5,
        label=f"LoA (+1.96 SD): {mean_diff + limit_of_agreement:.3f}",
    )
    lower_loa = ax4.axhline(
        y=mean_diff - limit_of_agreement,
        color=loa_line_color,
        linestyle="--",
        alpha=0.8,
        linewidth=1.5,
        label=f"LoA (-1.96 SD): {mean_diff - limit_of_agreement:.3f}",
    )
    ax4.set_xlabel(f"Mean of {x_label} and {y_label} {data_label}", fontsize=13)
    ax4.set_ylabel(f"Difference ({y_label} - {x_label}) {data_label}", fontsize=13)
    ax4.set_title("Bland-Altman Plot", fontdict=title_font)

    # Create a legend for the statistics lines only
    ax4.legend(
        handles=[mean_line, upper_loa, lower_loa],
        fontsize=10,
        shadow=True,
        loc="best",
    )

    ax4.grid(True, linestyle="--", alpha=0.4, color="#CCCCCC")
    ax4.tick_params(axis="both", which="major", labelsize=10)
    ax4.xaxis.set_major_formatter(formatter)
    ax4.yaxis.set_major_formatter(formatter)

    plt.tight_layout()

    # Create a shared legend for groups at the figure level
    if groups_array_str is not None and group_handles and group_labels:
        # Calculate position for legend
        # Position below the subplots but above the bottom of the figure
        fig.legend(
            handles=group_handles,
            labels=group_labels,
            loc="lower center",
            bbox_to_anchor=(0.5, 0.01),
            ncol=min(
                len(group_handles), 4
            ),  # Adjust number of columns based on group count
            fontsize=10,
            title="Groups",
            title_fontsize=12,
            shadow=True,
            frameon=True,
            facecolor="#FFFFFF",
            edgecolor="#4D5154",
        )
        # Adjust bottom margin to make room for the legend
        plt.subplots_adjust(bottom=0.1)  # Adjust this value as needed

    if save_path is not None:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
