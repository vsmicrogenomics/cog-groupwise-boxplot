import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
from scipy.stats import mannwhitneyu
from statsmodels.stats.multitest import multipletests

# Directories
input_dir = "./input"
output_dir = "./output"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Input file paths
combined_file_path = os.path.join(input_dir, "combined_classifier_count.tsv")
isolate_file_path = os.path.join(input_dir, "isolate_colors.tsv")

# Load data
combined_data = pd.read_csv(combined_file_path, sep='\t')
isolate_data = pd.read_csv(isolate_file_path, sep='\t', header=None)
isolate_data.columns = ['Isolate', 'Color', 'Group']

# Process data
isolate_values = combined_data.melt(id_vars=['LETTER', 'COLOR', 'Category', 'Class'], 
                                    var_name='Isolate', value_name='Count')
merged_data = isolate_values.merge(isolate_data, on='Isolate', how='left')

# Filter for valid LETTER and Group values
valid_letters = combined_data['LETTER'].unique()
valid_groups = isolate_data['Group'].unique()
category_data = merged_data[(merged_data['LETTER'].isin(valid_letters)) &
                            (merged_data['Group'].isin(valid_groups))]

# Function to calculate pairwise comparisons
def pairwise_tests(data, group_col, y_col):
    groups = data[group_col].unique()
    pairwise_results = []
    for pair in itertools.combinations(groups, 2):
        group1 = data[data[group_col] == pair[0]][y_col]
        group2 = data[data[group_col] == pair[1]][y_col]
        if not group1.empty and not group2.empty:
            stat, p_value = mannwhitneyu(group1, group2, alternative='two-sided')
            pairwise_results.append((pair[0], group1.mean(), pair[1], group2.mean(), p_value))
    return pairwise_results

# Perform pairwise tests
categories = category_data['Category'].unique()
stats_output = []

for category in categories:
    category_subset = category_data[category_data['Category'] == category]
    letters = category_subset['LETTER'].unique()

    for letter in letters:
        letter_data = category_subset[category_subset['LETTER'] == letter]
        pairwise_results = pairwise_tests(letter_data, 'Group', 'Count')
        
        # Save results to output
        for group1, mean1, group2, mean2, p_value in pairwise_results:
            stats_output.append({
                'Category': category,
                'LETTER': letter,
                'Group1': group1,
                'Mean1': mean1,
                'Group2': group2,
                'Mean2': mean2,
                'P-value': p_value,
                'Significant': p_value < 0.05
            })

    # Plotting
    plt.figure(figsize=(16, 10))
    sns.boxplot(data=category_subset, x='LETTER', y='Count', hue='Group', showfliers=False, dodge=True, width=0.8, palette='tab10')
    sns.stripplot(data=category_subset, x='LETTER', y='Count', hue='Group', dodge=True, marker='o', alpha=0.6, palette='tab10', linewidth=0.5)

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))  # Dynamic legend based on groups
    plt.legend(by_label.values(), by_label.keys(), title='Group', loc='upper right', bbox_to_anchor=(1.15, 1), fontsize=14)

    # Add significance lines based on stats_output
    y_offsets = {}  # Dictionary to track y-offset for each LETTER
    for stat_entry in stats_output:
        if stat_entry['Category'] == category and stat_entry['Significant']:
            letter = stat_entry['LETTER']
            group1 = stat_entry['Group1']
            group2 = stat_entry['Group2']

            # Ensure group1 and group2 are valid and present in the hue order
            hue_order = list(category_subset['Group'].unique())
            if group1 not in hue_order or group2 not in hue_order:
                continue

            # Get x-coordinates of the groups being compared
            x_positions = list(category_subset['LETTER'].unique())
            x_letter = x_positions.index(letter)  # Horizontal position of the letter on the x-axis
            group1_x = x_letter - 0.4 + 0.8 / len(hue_order) * hue_order.index(group1)
            group2_x = x_letter - 0.4 + 0.8 / len(hue_order) * hue_order.index(group2)

            # Determine y-coordinate dynamically with per-letter spacing
            if letter not in y_offsets:
                y_offsets[letter] = category_subset[category_subset['LETTER'] == letter]['Count'].max() + 20
            else:
                y_offsets[letter] += 20

            y = y_offsets[letter]

            # Plot horizontal line and ticks for significant comparisons
            if group1_x != group2_x:  # Ensure the groups are different
                plt.plot([group1_x, group2_x], [y, y], color='black', lw=1.5)
                plt.plot([group1_x, group1_x], [y - 2, y], color='black', lw=1.0)
                plt.plot([group2_x, group2_x], [y - 2, y], color='black', lw=1.0)
                plt.text((group1_x + group2_x) / 2, y + 1, '*', ha='center', color='black', fontsize=14)

    plt.title(f'Box-Scatter Plot for {category}', fontsize=18)
    plt.xlabel('LETTER', fontsize=16)
    plt.ylabel('Count', fontsize=16)
    plt.xticks(rotation=0, fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()

    plot_path = os.path.join(output_dir, f"boxplot_{category.replace(' ', '_')}.pdf")
    plt.savefig(plot_path, format='pdf')
    plt.close()

# Save statistics to TSV
stats_df = pd.DataFrame(stats_output)
stats_file_path = os.path.join(output_dir, "statistics.tsv")
stats_df.to_csv(stats_file_path, sep='\t', index=False)

print("Plots and statistics generated in the 'output' directory.")
