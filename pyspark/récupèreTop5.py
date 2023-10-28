# Table in which the top 5 of pagerank will be stored
data = []

# pyspark_result__part-00000(1).txt is the file of pyspark pagerank results used here 
with open('pyspark_result__part-00000(1).txt', 'r') as file:
    for line in file:
        # Split each line in an tuple (id, value) 
        parts = line.strip().strip("('<>").split(', ')
        value = float(parts[1].rstrip(')'))  # Delete the ')' at the end of the value
        id_value = (parts[0], value)
        data.append(id_value)

# Sort data in a decreasing way according to the pagerank value 
sorted_data = sorted(data, key=lambda x: x[1], reverse=True)

# Get top 5 lines
top_5 = sorted_data[:5]

for item in top_5:
    print(item)
