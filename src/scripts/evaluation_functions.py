from sklearn.metrics.pairwise import cosine_similarity

from caching import check_cache

def calculate_node_metrics(ground_truth_nodes, generated_nodes):
    """
    This function calculates the FP, FN, TP, for two sets of nodes, the ground truth nodes, and the generated nodes.
    """
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    
    # Convert node lists to sets for easier comparison
    ground_truth_set = set(tuple(node) for node in ground_truth_nodes)
    generated_set = set(tuple(node) for node in generated_nodes)
    
    # True Positives: Nodes present in both ground truth and generated set
    true_positives = len(ground_truth_set.intersection(generated_set))
    
    # False Positives: Nodes present in generated set but not in ground truth set
    false_positive_nodes = generated_set - ground_truth_set
    false_positives = len(false_positive_nodes)
    
    # False Negatives: Nodes present in ground truth set but not in generated set
    false_negative_nodes = ground_truth_set - generated_set 
    false_negatives = len(ground_truth_set - generated_set)
    
    return true_positives, false_positives, false_negatives, false_positive_nodes, false_negative_nodes

def calculate_node_metrics_semantic(ground_truth_nodes, generated_nodes, embed_query, cache):
    """
    This function calculates the FP, FN, TP, for two sets of nodes, the ground truth nodes, and the generated nodes. This time nodes are considered matching if they have a cosine similarity of 0.8 or higher.
    """
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    false_positive_nodes = []
    false_negative_nodes = []
    
    # Function to compute semantic similarity between two node descriptions
    def compute_similarity(node1, node2, cache):

        if not check_cache(node1, cache):
            embedding1 = embed_query(node1)
            cache[node1] = embedding1
        else:
            embedding1 = cache[node1]

        if not check_cache(node2, cache):
            embedding2 = embed_query(node2)
            cache[node2] = embedding2
        else:
            embedding2 = cache[node2]
        
        # Compute the cosine similarity between the two embeddings
        similarity_score = cosine_similarity([embedding1], [embedding2])[0, 0]
        return similarity_score, cache
    
    # Convert node lists to sets for easier comparison
    ground_truth_set = set(tuple(node) for node in ground_truth_nodes)
    generated_set = set(tuple(node) for node in generated_nodes)
    
    # Loop through generated nodes and find matches in ground truth using semantic similarity
    for gen_node in generated_set:
        match_found = False
        for gt_node in ground_truth_set:
            similarity_score, cache = compute_similarity(gen_node[0], gt_node[0], cache)
            # You can adjust this threshold as needed
            if similarity_score > 0.8:  # Example threshold
                true_positives += 1
                match_found = True
                break
        if not match_found:
            false_positives += 1
            false_positive_nodes.append(gen_node)

    
    # Count false negatives (ground truth nodes not matched by generated nodes)
    for gt_node in ground_truth_set:
        match_found = False
        for gen_node in generated_set:
            similarity_score, cache = compute_similarity(gen_node[0], gt_node[0], cache)
            if similarity_score > 0.8:  # Example threshold
                match_found = True
                break
        if not match_found:
            false_negatives += 1
            false_negative_nodes.append(gt_node)
    
    return true_positives, false_positives, false_negatives, false_positive_nodes, false_negative_nodes, cache