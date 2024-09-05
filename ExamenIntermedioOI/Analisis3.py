import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('diamond_data.csv')

# Create the figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Define colors for each step
colors = ['#1f77b4', '#63aad1', '#ff7f0e', '#ff9e4a']

# Iterate through each attribute
for i, attr in enumerate(df['attribute']):
    values = df.loc[i, ['minus_one_step', 'minus_half_step', 'plus_half_step', 'plus_one_step']]
    left = -values['minus_one_step'] - values['minus_half_step']

    # Plot the bars
    ax.barh(attr, values['minus_one_step'], left=left, color=colors[0], height=0.5)
    ax.barh(attr, values['minus_half_step'], left=left + values['minus_one_step'], color=colors[1], height=0.5)
    ax.barh(attr, values['plus_half_step'], left=0, color=colors[2], height=0.5)
    ax.barh(attr, values['plus_one_step'], left=values['plus_half_step'], color=colors[3], height=0.5)

# Customize the plot
ax.set_xlabel('Change in average diamond price [%]')
ax.set_ylabel('Diamond attribute')
ax.set_title('Impact of Diamond Attributes on Price')
ax.grid(axis='x', linestyle='--', alpha=0.7)

# Add legend
legend_elements = [plt.Rectangle((0, 0), 1, 1, color=colors[i], label=label)
                   for i, label in enumerate(['-1 step', '-1/2 step', '+1/2 step', '+1 step'])]
ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig('diamond_price_change.png', dpi=300, bbox_inches='tight')
plt.close()

print("Graph has been saved as 'diamond_price_change.png'")