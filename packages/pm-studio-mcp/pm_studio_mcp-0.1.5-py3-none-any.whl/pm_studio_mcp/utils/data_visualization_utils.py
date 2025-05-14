import os
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Please install matplotlib: pip install matplotlib")

try:
    import seaborn as sns  # Import Seaborn for color palettes
except ImportError:
    print("Please install seaborn: pip install seaborn")

class DataVisualizationUtils:
    def generate_pie_chart_tool(data: dict, working_path: str):
        try:
            # Validate input data
            if not isinstance(data, dict) or not data:
                return "Error: Input data must be a non-empty dictionary with categories and counts."

            # Separate "Other" category if it exists
            other_count = data.pop("Other", None)

            # Sort the remaining categories by count in descending order
            sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

            # Add "Other" back as the last category if it exists
            if other_count is not None:
                sorted_data.append(("Other", other_count))

            # Extract categories and counts
            categories, counts = zip(*sorted_data)

            # Generate colors using Seaborn's 'Set2' palette
            colors = sns.color_palette('Set2', len(categories))

            # Generate the pie chart
            plt.figure(figsize=(8, 8))
            plt.pie(
                counts,
                labels=categories,
                autopct='%1.1f%%',
                startangle=90,  # Start from 12 o'clock
                colors=colors,
                counterclock=False, 
            )
            plt.title("User Feedback Distribution")

            # Save the pie chart
            output_file = os.path.join(working_path, "userfeedback_piechart.jpg")
            plt.savefig(output_file, dpi=300)
            plt.close()

            return f"Pie chart saved at: {output_file}"
        except Exception as e:
            return f"Error generating pie chart: {str(e)}"