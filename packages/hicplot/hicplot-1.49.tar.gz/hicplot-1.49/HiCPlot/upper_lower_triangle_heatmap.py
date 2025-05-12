#!/usr/bin/env python
import argparse
import os
import pandas as pd
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pyBigWig
import pyranges as pr
import numpy as np
import matplotlib.pyplot as plt
import cooler
from matplotlib.colors import LogNorm
from matplotlib.ticker import EngFormatter
import itertools
import sys
import scipy.sparse
import matplotlib.gridspec as gridspec
import matplotlib.colors as mcolors
from matplotlib.patches import Arc
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
version_py = os.path.join(script_dir, "_version.py")
with open(version_py) as _vf:
    exec(_vf.read())

def plot_genes(ax, gtf_file, region, genes_to_annotate=None, color='blue', track_height=1):
    """
    Plot gene annotations on the given axis.
    Annotate only the specified genes with their names.

    Parameters:
    - ax: Matplotlib axis to plot on.
    - gtf_file: Path to the GTF file.
    - region: Tuple (chromosome, start, end).
    - genes_to_annotate: List of gene names to annotate. If None, no annotations.
    - color: Color for gene lines and exons.
    - track_height: Height of each gene track.
    """
    spacing_factor = 1.5
    chrom, start, end = region
    # Load the GTF file using pyranges
    gtf = pr.read_gtf(gtf_file)
    # Filter relevant region
    region_genes = gtf[(gtf.Chromosome == chrom) & (gtf.Start < end) & (gtf.End > start)]

    if region_genes.empty:
        print("No genes found in the specified region.")
        ax.axis('off')  # Hide the axis if no genes are present
        return

    # Select the longest isoform for each gene
    longest_isoforms = region_genes.df.loc[region_genes.df.groupby('gene_id')['End'].idxmax()]

    y_offset = 0
    y_step = track_height * spacing_factor  # Adjusted vertical step for tighter spacing
    plotted_genes = []

    # Iterate over each gene and plot
    for _, gene in longest_isoforms.iterrows():
        # Determine y_offset to avoid overlap with previously plotted genes
        for plotted_gene in plotted_genes:
            if not (gene['End'] < plotted_gene['Start'] or gene['Start'] > plotted_gene['End']):
                y_offset = max(y_offset, plotted_gene['y_offset'] + y_step)

        # Plot gene line with increased linewidth for better visibility
        ax.plot([gene['Start'], gene['End']], [y_offset, y_offset], color=color, lw=1)

        # Plot exons as larger rectangles for increased height
        exons = region_genes.df[
            (region_genes.df['gene_id'] == gene['gene_id']) & (region_genes.df['Feature'] == 'exon')
        ]
        for _, exon in exons.iterrows():
            ax.add_patch(
                plt.Rectangle(
                    (exon['Start'], y_offset - 0.3 * track_height),  # Lowered to center the exon vertically
                    exon['End'] - exon['Start'],
                    0.6 * track_height,  # Increased height of exon rectangles
                    color=color
                )
            )

        # Conditionally add gene name if it's in the specified list
        if genes_to_annotate and gene['gene_name'] in genes_to_annotate:
            ax.text(
                (gene['Start'] + gene['End']) / 2,
                y_offset - 0.4 * track_height,  # Positioned below the gene line
                gene['gene_name'],
                fontsize=8,  # Increased font size for readability
                ha='center',
                va='top'  # Align text above the specified y position
            )

        # Track the plotted gene's range and offset
        plotted_genes.append({'Start': gene['Start'], 'End': gene['End'], 'y_offset': y_offset})

    # Set y-axis limits based on the final y_offset
    ax.set_ylim(-track_height * 2, y_offset + track_height * 2)  # Expanded lower limit
    ax.set_ylabel('Genes')
    ax.set_yticks([])  # Hide y-ticks for a cleaner look
    ax.set_xlim(start, end)
    ax.set_xlabel("Position (Mb)")

    # Format x-axis to display positions in megabases (Mb)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x / 1e6:.2f}'))

def read_bigwig(file_path, region):
    """Read BigWig or bedGraph file and return positions and values."""
    chrom, start, end = region
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in ['.bw', '.bigwig']:
        # Open the BigWig file
        bw = pyBigWig.open(file_path)
        # Fetch values from the region
        values = bw.values(chrom, start, end, numpy=True)
        bw.close()  # Close the BigWig file
        positions = np.linspace(start, end, len(values))
    elif file_extension in ['.bedgraph', '.bg']:
        # Read the bedGraph file using pandas
        # Assuming bedGraph files have columns: chrom, start, end, value
        bedgraph_df = pd.read_csv(file_path, sep='\t', header=None, comment='#', 
                                  names=['chrom', 'start', 'end', 'value'])
        # Filter the data for the specified region
        region_data = bedgraph_df[
            (bedgraph_df['chrom'] == chrom) &
            (bedgraph_df['end'] > start) &
            (bedgraph_df['start'] < end)
        ]
        if region_data.empty:
            return None, None
        # Prepare the positions and values
        positions = np.sort(np.unique(np.concatenate([region_data['start'].values, 
                                                      region_data['end'].values])))
        values = np.zeros_like(positions, dtype=float)
        for idx in range(len(region_data)):
            s = region_data.iloc[idx]['start']
            e = region_data.iloc[idx]['end']
            v = region_data.iloc[idx]['value']
            mask = (positions >= s) & (positions <= e)
            values[mask] = v
    else:
        raise ValueError(f"Unsupported file format: {file_extension}. Supported formats are BigWig (.bw) and bedGraph (.bedgraph, .bg).")
    return positions, values

def get_track_min_max(bigwig_files_sample1, bigwig_labels_sample1,
                      bigwig_files_sample2, bigwig_labels_sample2,
                      region):
    """
    Compute the minimum and maximum values for BigWig tracks per type to ensure consistent y-axis scaling.

    Parameters:
    - bigwig_files_sample1: List of BigWig files for sample 1.
    - bigwig_labels_sample1: List of labels corresponding to BigWig files for sample 1.
    - bigwig_files_sample2: List of BigWig files for sample 2.
    - bigwig_labels_sample2: List of labels corresponding to BigWig files for sample 2.
    - region: Tuple containing (chromosome, start, end).

    Returns:
    - type_min_max: Dictionary with BigWig types as keys and (min, max) tuples as values.
    """
    type_min_max = defaultdict(lambda: {'min': np.inf, 'max': -np.inf})

    # Function to extract type from label (assumes type is the first part before a space)
    def extract_type(label):
        return label.split("_")[1] if label and "_" in label else 'Unknown'

    # Combine sample1 and sample2 BigWig files and labels
    combined_files = bigwig_files_sample1 + bigwig_files_sample2
    combined_labels = bigwig_labels_sample1 + bigwig_labels_sample2

    for file, label in zip(combined_files, combined_labels):
        bw_type = extract_type(label)
        positions, values = read_bigwig(file, region)
        if values is not None and len(values) > 0:
            current_min = np.nanmin(values)
            current_max = np.nanmax(values)
            type_min_max[bw_type]['min'] = min(type_min_max[bw_type]['min'], current_min)
            type_min_max[bw_type]['max'] = max(type_min_max[bw_type]['max'], current_max)

    # Replace infinities with None if no data was found for a type
    for bw_type in type_min_max:
        if type_min_max[bw_type]['min'] == np.inf and type_min_max[bw_type]['max'] == -np.inf:
            type_min_max[bw_type] = (None, None)
        else:
            type_min_max[bw_type] = (type_min_max[bw_type]['min'], type_min_max[bw_type]['max'])

    return type_min_max

def plot_seq(ax, file_path, region, color='blue', y_min=None, y_max=None):
    """Plot RNA-seq/ChIP-seq expression from BigWig or bedGraph file on given axis."""
    chrom, start, end = region
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in ['.bw', '.bigwig']:
        # Open the BigWig file
        bw = pyBigWig.open(file_path)
        # Fetch values from the region
        values = bw.values(chrom, start, end, numpy=True)
        bw.close()  # Close the BigWig file
        positions = np.linspace(start, end, len(values))
    elif file_extension in ['.bedgraph', '.bg']:
        # Read the bedGraph file using pandas
        # Assuming bedGraph files have columns: chrom, start, end, value
        bedgraph_df = pd.read_csv(file_path, sep='\t', header=None, comment='#', 
                                  names=['chrom', 'start', 'end', 'value'])
        # Filter the data for the specified region
        region_data = bedgraph_df[
            (bedgraph_df['chrom'] == chrom) &
            (bedgraph_df['end'] > start) &
            (bedgraph_df['start'] < end)
        ]
        if region_data.empty:
            print(f"No data found in the specified region ({chrom}:{start}-{end}) in {file_path}")
            ax.axis('off')  # Hide the axis if no data
            return
        # Prepare the positions and values
        positions = np.sort(np.unique(np.concatenate([region_data['start'].values, 
                                                      region_data['end'].values])))
        values = np.zeros_like(positions, dtype=float)
        for idx in range(len(region_data)):
            s = region_data.iloc[idx]['start']
            e = region_data.iloc[idx]['end']
            v = region_data.iloc[idx]['value']
            mask = (positions >= s) & (positions <= e)
            values[mask] = v
    else:
        raise ValueError(f"Unsupported file format: {file_extension}. Supported formats are BigWig (.bw) and bedGraph (.bedgraph, .bg).")
    
    # Plot the RNA-seq/ChIP-seq expression as a filled line plot
    ax.plot(positions, values, color=color, alpha=0.7)
    ax.set_xlim(start, end)
    if y_min is not None and y_max is not None:
        ax.set_ylim(y_min, y_max)
    elif y_max is not None:
        ax.set_ylim(0, y_max)
    elif y_min is not None:
        ax.set_ylim(y_min, 1)  # Default upper limit if only y_min is provided
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x / 1e6:.2f}'))

def plot_bed(ax, bed_file, region, color='green', linewidth=1, label=None):
    """Plot BED file annotations on the given axis."""
    chrom, start, end = region
    # Read the BED file
    bed_df = pd.read_csv(bed_file, sep='\t', header=None, comment='#', 
                         names=['chrom', 'start', 'end'] + [f'col{i}' for i in range(4, 10)])
    # Filter for the region and chromosome
    region_bed = bed_df[
        (bed_df['chrom'] == chrom) &
        (bed_df['end'] > start) &
        (bed_df['start'] < end)
    ]
    if region_bed.empty:
        print(f"No BED entries found in the specified region ({chrom}:{start}-{end}) in {bed_file}")
        ax.axis('off')
        return
    
    for _, entry in region_bed.iterrows():
        bed_start = max(entry['start'], start)
        bed_end = min(entry['end'], end)
        ax.add_patch(
            plt.Rectangle(
                (bed_start, 0.1),  # y-coordinate fixed
                bed_end - bed_start,
                0.8,  # Height of the BED feature
                color=color,
                linewidth=linewidth
            )
        )
    
    ax.set_xlim(start, end)
    ax.set_ylim(0, 1)
    ax.axis('off')  # Hide axis for BED tracks
    if label:
        ax.set_title(label, fontsize=8)

def pcolormesh_square(ax, matrix, start, end, cmap='autumn_r', vmin=None, NORM=True,vmax=None, *args, **kwargs):
    """
    Plot the matrix as a heatmap on the given axis.
    """
    if matrix is None:
        return None
    if NORM:
        log_vmin = vmin if vmin is not None and vmin > 0 else None
        norm = LogNorm(vmin=log_vmin, vmax=vmax, clip=False)
        im = ax.imshow(matrix, aspect='auto', origin='upper',norm=norm,
                extent=[start, end, end, start], cmap=cmap, *args, **kwargs)
    else:
        im = ax.imshow(matrix, aspect='auto', origin='upper',
                   extent=[start, end, end, start], cmap=cmap, vmin=vmin, vmax=vmax, *args, **kwargs)
    return im

def plot_loops(ax, loop_file, region, color='purple', alpha=0.5, linewidth=1, label=None):
    """
    Plot chromatin loops as arcs on the given axis.

    Parameters:
    - ax: Matplotlib axis to plot on.
    - loop_file: Path to the loop file.
    - region: Tuple (chromosome, start, end).
    - color: Color for the loop arcs.
    - alpha: Transparency level for the arcs.
    - linewidth: Width of the arc lines.
    - label: Label for the loop track (sample name).
    """
    chrom, start, end = region
    # Read the loop file
    loop_df = pd.read_csv(loop_file, sep='\t', header=0, usecols=[0,1,2,3,4,5],
                          names=['chrom1', 'start1', 'end1', 'chrom2', 'start2', 'end2'])

    # Filter loops where both anchors are within the region and on the same chromosome
    loop_df = loop_df[
        (loop_df['chrom1'] == chrom) &
        (loop_df['chrom2'] == chrom) &
        (loop_df['start1'] >= start) & (loop_df['end1'] <= end) &
        (loop_df['start2'] >= start) & (loop_df['end2'] <= end)
    ]

    if loop_df.empty:
        print(f"No loops detected in the specified region ({chrom}:{start}-{end}) in {loop_file}.")
        ax.axis('off')
        return
    else:
        print(f"Loops detected in the specified region ({chrom}:{start}-{end}) in {loop_file}.")

    max_height = 0  # Keep track of the maximum arc height for y-axis scaling

    # Add rectangle background to make arcs stand out
    ax.add_patch(
        plt.Rectangle(
            (start, 0),  # Position of the rectangle
            end - start,
            1.0,  # Height of the rectangle
            #color='black',
            alpha=1,  # Adjusted alpha for visibility
            zorder=3,  # Draw behind other elements
            edgecolor='black',  # Border color
            linewidth=1.0,  # Width of the border line
            facecolor="none",
        )
    )

    # Plot each loop as an arc
    for _, loop in loop_df.iterrows():
        a1 = (loop['start1'] + loop['end1']) / 2  # Midpoint of anchor1
        a2 = (loop['start2'] + loop['end2']) / 2  # Midpoint of anchor2
        if a1 == a2:
            continue  # Skip loops where both anchors are the same

        # Calculate the width and height of the arc
        width = abs(a2 - a1)
        height = width / 2  # Adjust this factor to change the curvature

        # Update max_height
        if height > max_height:
            max_height = height

        # Determine the center of the arc
        mid = (a1 + a2) / 2

        # Create the Arc
        arc = Arc((mid, 0), width=width, height=height*2, angle=0, theta1=0, theta2=180,
                  edgecolor=color, facecolor='none', alpha=alpha, linewidth=linewidth)
        ax.add_patch(arc)

    # Adjust x-limits and y-limits
    ax.set_xlim(start, end)
    ax.set_ylim(0, max_height * 1.1)  # Adjust y-limits based on maximum arc height
    ax.axis('off')  # Hide axis for loop tracks
    if label:
        ax.set_title(label, fontsize=8,pad=10)  # Add sample name above the loop track

def plot_heatmaps(cooler_file1, sampleid1=None,format="balance",
                 bigwig_files_sample1=[], bigwig_labels_sample1=[], colors_sample1="red",
                 bed_files_sample1=[], bed_labels_sample1=[],
                 loop_file_sample1=None, loop_file_sample2=None,
                 gtf_file=None, resolution=None, chrid=None,start=None, end=None,
                 cmap='autumn_r', vmin=None, vmax=None,
                 track_min=None,track_max=None,
                 output_file='comparison_heatmap.pdf',
                 cooler_file2=None, sampleid2=None,
                 bigwig_files_sample2=[], bigwig_labels_sample2=[], colors_sample2="blue",
                 bed_files_sample2=[], bed_labels_sample2=[], 
                 track_size=5, track_spacing=0.5, normalization_method='raw',
                 genes_to_annotate=None,title=None):
    plt.rcParams['font.size'] = 8
    # Set parameters
    region = (chrid, start, end)
    
    # Load cooler data for Sample1
    clr1 = cooler.Cooler(f'{cooler_file1}::resolutions/{resolution}')
    if format == "balance":
        data1 = clr1.matrix(balance=True).fetch(region).astype(float)
    elif format == "ICE":
        data1 = clr1.matrix(balance=False).fetch(region).astype(float)
    else:
        print("input format is wrong")
    # Load cooler data for Sample2 if provided
    single_sample = cooler_file2 is None
    if not single_sample:
        clr2 = cooler.Cooler(f'{cooler_file2}::resolutions/{resolution}')
        if format == "balance":
            data2 = clr2.matrix(balance=True).fetch(region).astype(float)
        elif format == "ICE":
            data2 = clr2.matrix(balance=False).fetch(region).astype(float)
        else:
            print("input format is wrong")
    
    # Apply normalization to Hi-C matrices
    if normalization_method == 'raw':
        normalized_data1 = data1
        normalized_data2 = data2 if not single_sample else None
    elif normalization_method == 'logNorm':
        normalized_data1 = np.maximum(data1, 0)
        if not single_sample:
            normalized_data2 = np.maximum(data2, 0)
    elif normalization_method == 'log2':
        normalized_data1 = np.log2(data1)
        if not single_sample:
            normalized_data2 = np.log2(data2)
    elif normalization_method == 'log2_add1':
        normalized_data1 = np.log2(data1 + 1)
        if not single_sample:
            normalized_data2 = np.log2(data2 + 1)
    elif normalization_method == 'log':
        normalized_data1 = np.log(data1)
        if not single_sample:
            normalized_data2 = np.log(data2)
    elif normalization_method == 'log_add1':
        normalized_data1 = np.log(data1 + 1)
        if not single_sample:
            normalized_data2 = np.log(data2 + 1)
    else:
        raise ValueError(f"Unsupported normalization method: {normalization_method}")
    
    # Create combined matrix: upper triangle from data1, lower triangle from data2, diagonal set to np.nan
    combined_matrix = np.full_like(data1, np.nan)
    triu_indices = np.triu_indices_from(data1, k=1)
    tril_indices = np.tril_indices_from(data1, k=-1)

    combined_matrix[triu_indices] = normalized_data1[triu_indices]
    if not single_sample:
        combined_matrix[tril_indices] = normalized_data2[tril_indices]
    else:
        combined_matrix[tril_indices] = 0  # If single sample, set lower triangle to zero
    # Diagonal is already set to np.nan

    # Determine color limits for combined heatmap
    if vmin is None:
        vmin_combined = np.nanmin(combined_matrix)
    else:
        vmin_combined = vmin
    if vmax is None:
        vmax_combined = np.nanmax(combined_matrix)
    else:
        vmax_combined = vmax

    # Define GridSpec for vertical layout
    # Layout:
    # Row0: Combined Hi-C Heatmap
    # Row1: Colorbar for combined heatmap
    # Row2: Chromatin Loops for sample1
    # Row3: Chromatin Loops for sample2 (if provided)
    # Rows4 to (4 + max_bigwig_bed_tracks): BigWig and BED tracks
    # Last Row: Gene Annotations
    num_colorbars = 1
    num_loops = 0
    if loop_file_sample1:
        num_loops += 1
    if loop_file_sample2:
        num_loops += 1
    num_genes = 1 if gtf_file else 0
    # Calculate the number of BigWig and BED tracks
    max_num_bigwig_files = len(bigwig_files_sample1) + len(bigwig_files_sample2)
    max_num_bed_files = len(bed_files_sample1) + len(bed_files_sample2)
    max_bigwig_bed_tracks = max_num_bigwig_files + max_num_bed_files

    num_rows = 2 + num_loops + max_bigwig_bed_tracks + num_genes

    # Define height ratios
    small_colorbar_height = 0.1  # Adjust as needed
    track_height_ratio = 0.5  # Adjust as needed for BigWig/BED tracks
    loop_track_height = 0.3
    if num_genes !=0:
        height_ratios = [1] + [small_colorbar_height] + [loop_track_height]*num_loops+[track_height_ratio] * (max_bigwig_bed_tracks) + [track_height_ratio * num_genes]
    else:
        height_ratios = [1] + [small_colorbar_height] + [loop_track_height]*num_loops+[track_height_ratio] * (max_bigwig_bed_tracks)
    gs = gridspec.GridSpec(num_rows, 1, height_ratios=height_ratios, hspace=0.3)
    # Define default figsize
    width = track_size
    height = sum(height_ratios) * (track_size / height_ratios[0]) + (num_rows -1)*track_spacing
    figsize = (width, height)

    # Create figure with calculated size
    f = plt.figure(figsize=figsize)

    # Plot Combined Hi-C Heatmap
    ax_combined = f.add_subplot(gs[0, 0])
    if normalization_method == "logNorm":
        im_combined = pcolormesh_square(ax_combined, combined_matrix, region[1], region[2], cmap=cmap,NORM=True, vmin=vmin_combined, vmax=vmax_combined)
    else:
        im_combined = pcolormesh_square(ax_combined, combined_matrix, region[1], region[2], cmap=cmap, NORM=False,vmin=vmin_combined, vmax=vmax_combined)
    # Format x-axis ticks
    ax_combined.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, pos: f'{x / 1e6:.2f}'))
    ax_combined.set_title(title if title else "Combined Hi-C Heatmap", fontsize=10)
    ax_combined.set_ylim(end, start)  # Flip y-axis to match genomic coordinates
    ax_combined.set_xlim(start, end)
    #ax_combined.set_aspect('equal')  # Ensure square aspect
    # Add labels for Sample1 and Sample2
    #label_offset = (end - start) * 0.02  # 2% of the region length
    #ax_combined.text(end - label_offset,start + label_offset, 'Sample1', color='black', fontsize=8, ha='right', va='top')
    #ax_combined.text(end - label_offset, start + label_offset, 'Sample2', color='black', fontsize=8, ha='left', va='bottom')
    # Add labels for Sample1 and Sample2 using axes fraction
    ax_combined.text(0.95, 0.95, sampleid1, transform=ax_combined.transAxes, 
                color='black', fontsize=8, ha='right', va='top', 
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    ax_combined.text(0.05, 0.05, sampleid2, transform=ax_combined.transAxes, 
                color='black', fontsize=8, ha='left', va='bottom', 
                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

    # Create a colorbar for the combined heatmap
    cax_combined = f.add_subplot(gs[1, 0])
    cbar_combined = plt.colorbar(im_combined, cax=cax_combined, orientation='horizontal')
    cbar_combined.ax.tick_params(labelsize=8)
    cax_combined.xaxis.set_label_position('bottom')
    cax_combined.xaxis.set_ticks_position('bottom')
    cbar_combined.set_label(normalization_method, labelpad=10)
    cbar_combined.ax.xaxis.set_label_position('top')

    current_row = 2
    # Plot Chromatin Loops for Sample1
    if loop_file_sample1:
        ax_loop1 = f.add_subplot(gs[current_row, 0])
        plot_loops(ax_loop1, loop_file_sample1, region, color=colors_sample1, alpha=0.7, linewidth=1, label=f"{sampleid1} Loops")
        current_row += 1
    # Plot Chromatin Loops for Sample2 if provided
    if loop_file_sample2:
        ax_loop2 = f.add_subplot(gs[current_row, 0])
        plot_loops(ax_loop2, loop_file_sample2, region, color=colors_sample2, alpha=0.7, linewidth=1, label=f"{sampleid2} Loops")
        current_row += 1

    # Compute global min and max per BigWig type
    if track_min is not None and track_max is not None:
        type_min_max = defaultdict(lambda: (track_min, track_max))
    else:
        type_min_max = get_track_min_max(bigwig_files_sample1, bigwig_labels_sample1,
                                        bigwig_files_sample2, bigwig_labels_sample2,
                                        region=region)

    # Plot BigWig and BED tracks
    # Plot BigWig tracks for Sample1
    current_row = 2 + num_loops
    if bigwig_files_sample1:
        for i in range(len(bigwig_files_sample1)):
            ax_bw = f.add_subplot(gs[current_row + i, 0])
            # Extract type from label
            bw_type = bigwig_labels_sample1[i].split("_")[1] if "_" in bigwig_labels_sample1[i] else 'Unknown'
            y_min, y_max = type_min_max[bw_type]
            plot_seq(ax_bw, bigwig_files_sample1[i], region, color=colors_sample1, 
                     y_min=y_min, y_max=y_max)
            ax_bw.set_title(f"{bigwig_labels_sample1[i]}", fontsize=8,pad=10)
            ax_bw.set_xlim(start, end)
            if y_min is not None and y_max is not None:
                ax_bw.set_ylim(y_min, y_max * 1.1)
    current_row = 2 + num_loops + len(bigwig_files_sample1)
    # Plot BigWig tracks for Sample2 if provided
    if bigwig_files_sample2:
        for j in range(len(bigwig_files_sample2)):
            ax_bw = f.add_subplot(gs[current_row + j, 0])
            # Extract type from label
            bw_type = bigwig_labels_sample2[j].split("_")[1] if "_" in bigwig_labels_sample2[j] else 'Unknown'
            y_min, y_max = type_min_max[bw_type]
            plot_seq(ax_bw, bigwig_files_sample2[j], region, color=colors_sample2, 
                     y_min=y_min, y_max=y_max)
            ax_bw.set_title(f"{bigwig_labels_sample2[j]}", fontsize=8,pad=10)
            ax_bw.set_xlim(start, end)
            if y_min is not None and y_max is not None:
                ax_bw.set_ylim(y_min, y_max * 1.1)

    # Update current_row after BigWig tracks
    current_row = 2 + num_loops + len(bigwig_files_sample1) + len(bigwig_files_sample2)
    # Plot BED tracks for Sample1
    if bed_files_sample1:
        for k in range(len(bed_files_sample1)):
            ax_bed = f.add_subplot(gs[current_row + k, 0])
            plot_bed(ax_bed, bed_files_sample1[k], region, color=colors_sample1, label=bed_labels_sample1[k])
            ax_bed.set_title(f"{bed_labels_sample1[k]}", fontsize=8,pad=10)

    current_row = 2 + num_loops + len(bigwig_files_sample1) + len(bigwig_files_sample2) + len(bed_files_sample1)
    # Plot BED tracks for Sample2 if provided
    if bed_files_sample2:
        for l in range(len(bed_files_sample2)):
            ax_bed = f.add_subplot(gs[current_row+ l, 0])
            plot_bed(ax_bed, bed_files_sample2[l], region, color=colors_sample2, label=bed_labels_sample2[l])
            ax_bed.set_title(f"{bed_labels_sample2[l]}", fontsize=8,pad=10)

    # Plot Genes if GTF file is provided
    if gtf_file:
        ax_genes = f.add_subplot(gs[num_rows-1, 0])
        plot_genes(ax_genes, gtf_file, region, genes_to_annotate=genes_to_annotate, color='blue', track_height=1)
        ax_genes.set_xlim(start, end)

    # Adjust layout and save the figure
    plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)
    f.savefig(output_file, bbox_inches='tight')
    plt.close(f)

def main(argv: list[str] | None = None):
    if argv is None:
        argv = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Plot combined Hi-C heatmap from two cooler files with BigWig, BED tracks, gene annotations, and chromatin loops.')

    # Required arguments
    parser.add_argument('--cooler_file1', type=str, required=True, help='Path to the first sample .cool or .mcool file.')
    parser.add_argument('--cooler_file2', type=str, required=True, help='Path to the second sample .cool or .mcool file.')
    parser.add_argument('--format', type=str, default='balance', choices=['balance', 'ICE'], help='Format of .mcool file.')

    parser.add_argument('--sampleid1', type=str, required=True, help='sample1 name.')
    parser.add_argument('--sampleid2', type=str, required=True, help='sample2 name.')
    parser.add_argument('--resolution', type=int, required=True, help='Resolution for the cooler data.')
    parser.add_argument('--start', type=int, required=True, help='Start position for the region of interest.')
    parser.add_argument('--end', type=int, required=True, help='End position for the region of interest.')
    parser.add_argument('--chrid', type=str, required=True, help='Chromosome ID.')
    parser.add_argument('--gtf_file', type=str, required=False, help='Path to the GTF file for gene annotations.', default=None)

    # Optional arguments
    parser.add_argument('--cmap', type=str, default='autumn_r', help='Colormap to be used for the combined heatmap.')
    parser.add_argument('--vmin', type=float, default=None, help='Minimum value for normalization of the combined heatmap.')
    parser.add_argument('--vmax', type=float, default=None, help='Maximum value for normalization of the combined heatmap.')
    parser.add_argument('--output_file', type=str, default='combined_hic_heatmap.pdf', help='Filename for the saved combined heatmap PDF.')

    # BigWig arguments
    parser.add_argument('--bigwig_files_sample1', type=str, nargs='*', help='Paths to BigWig files for sample 1.', default=[])
    parser.add_argument('--bigwig_labels_sample1', type=str, nargs='*', help='Labels for BigWig tracks of sample 1.', default=[])
    parser.add_argument('--colors_sample1', type=str, default="red", help='Colors for sample 1 BigWig tracks.')
    parser.add_argument('--bigwig_files_sample2', type=str, nargs='*', help='Paths to BigWig files for sample 2.', default=[])
    parser.add_argument('--bigwig_labels_sample2', type=str, nargs='*', help='Labels for BigWig tracks of sample 2.', default=[])
    parser.add_argument('--colors_sample2', type=str, default="blue", help='Colors for sample 2 BigWig tracks.')

    # BED arguments
    parser.add_argument('--bed_files_sample1', type=str, nargs='*', help='Paths to BED files for sample 1.', default=[])
    parser.add_argument('--bed_labels_sample1', type=str, nargs='*', help='Labels for BED tracks of sample 1.', default=[])
    parser.add_argument('--bed_files_sample2', type=str, nargs='*', help='Paths to BED files for sample 2.', default=[])
    parser.add_argument('--bed_labels_sample2', type=str, nargs='*', help='Labels for BED tracks of sample 2.', default=[])

    # Loop file arguments
    parser.add_argument('--loop_file_sample1', type=str, help='Path to the chromatin loop file for sample 1.', default=None)
    parser.add_argument('--loop_file_sample2', type=str, help='Path to the chromatin loop file for sample 2.', default=None)

    # Normalization Method Argument
    parser.add_argument('--normalization_method', type=str, default='raw', choices=['raw', 'logNorm','log2', 'log2_add1','log','log_add1'],
                        help="Method for normalization: 'raw', 'logNorm','log2', 'log2_add1', 'log', or 'log_add1'.")

    parser.add_argument('--track_size', type=float, default=5, help='Height of the heatmap track (in inches).')
    parser.add_argument('--track_spacing', type=float, default=0.5, help='Spacing between tracks (in inches).')

    parser.add_argument('--track_min', type=float, default=None, help='Global minimum value for all BigWig tracks.')
    parser.add_argument('--track_max', type=float, default=None, help='Global maximum value for all BigWig tracks.')

    # Gene annotation arguments
    parser.add_argument('--genes_to_annotate', type=str, nargs='*', help='Gene names to annotate.', default=None)
    parser.add_argument('--title', type=str, nargs='*', help='title of the heatmap.', default=None)
    parser.add_argument("-V", "--version", action="version",version="SquHeatmap {}".format(__version__)\
                      ,help="Print version and exit")
    args = parser.parse_args(argv)

# Call the plotting function
    plot_heatmaps(
        cooler_file1=args.cooler_file1,
        sampleid1=args.sampleid1,
        bigwig_files_sample1=args.bigwig_files_sample1,
        bigwig_labels_sample1=args.bigwig_labels_sample1,
        colors_sample1=args.colors_sample1,
        bed_files_sample1=args.bed_files_sample1,
        bed_labels_sample1=args.bed_labels_sample1,
        loop_file_sample1=args.loop_file_sample1,
        loop_file_sample2=args.loop_file_sample2,
        gtf_file=args.gtf_file,
        resolution=args.resolution,
        start=args.start,
        end=args.end,
        chrid=args.chrid,
        cmap=args.cmap,
        vmin=args.vmin,
        vmax=args.vmax,
        track_min=args.track_min,
        track_max=args.track_max,
        output_file=args.output_file,
        cooler_file2=args.cooler_file2,
        sampleid2=args.sampleid2,
        bigwig_files_sample2=args.bigwig_files_sample2,
        bigwig_labels_sample2=args.bigwig_labels_sample2,
        colors_sample2=args.colors_sample2,
        bed_files_sample2=args.bed_files_sample2,
        bed_labels_sample2=args.bed_labels_sample2,
        track_size=args.track_size,
        track_spacing=args.track_spacing,
        normalization_method=args.normalization_method,
        genes_to_annotate=args.genes_to_annotate,
        title=args.title,
        format=args.format
    )

if __name__ == '__main__':
    main()
