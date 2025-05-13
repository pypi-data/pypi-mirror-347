# Utilities for generating and handling embeddings 

import os
import numpy as np
from openai import OpenAI
from typing import List, Optional

from . import config

def get_openai_client(api_key: Optional[str] = None) -> OpenAI:
    """Initializes and returns an OpenAI client.

    Args:
        api_key (Optional[str], optional): The OpenAI API key.
            If not provided, it will try to use the OPENAI_API_KEY environment variable.
            Defaults to None.

    Raises:
        ValueError: If no API key is provided and the OPENAI_API_KEY environment variable is not set.

    Returns:
        OpenAI: An initialized OpenAI client.
    """
    if api_key:
        return OpenAI(api_key=api_key)
    else:
        env_api_key = os.environ.get("OPENAI_API_KEY")
        if env_api_key:
            return OpenAI(api_key=env_api_key)
        else:
            raise ValueError(
                "No OpenAI API key provided directly or found in OPENAI_API_KEY environment variable."
            ) 

def generate_embeddings(
    client: OpenAI,
    texts_list: List[str],
    model_name: Optional[str] = None
) -> np.ndarray:
    """Generates embeddings for a list of texts using the specified model.

    Args:
        client (OpenAI): The initialized OpenAI client.
        texts_list (List[str]): A list of texts to embed.
        model_name (Optional[str], optional): The name of the embedding model to use.
            If None, defaults to config.DEFAULT_EMBEDDING_MODEL. Defaults to None.

    Returns:
        np.ndarray: A NumPy array of embeddings.

    Raises:
        Exception: If the OpenAI API call fails or if the input list is empty and an array cannot be formed as expected.
    """
    if not texts_list:
        # Return an empty 2D array with a shape like (0, embedding_dimension) if possible,
        # or handle as appropriate. For now, returning a simple empty array.
        # If a specific dimension is known for the model, it could be np.empty((0, dim)).
        return np.array([]) 

    actual_model_name = model_name if model_name else config.DEFAULT_EMBEDDING_MODEL

    try:
        api_response = client.embeddings.create(input=texts_list, model=actual_model_name)
        # Assuming all embeddings in a batch have the same dimension
        if not api_response.data:
            return np.array([]) # Should ideally match expected dimension if known
        
        embeddings = np.array([item.embedding for item in api_response.data])
        return embeddings
    
    except Exception as e:

        raise Exception(f"OpenAI API call for embeddings failed with model {actual_model_name}: {e}") 

def normalize_embeddings(embeddings_array: np.ndarray) -> np.ndarray:
    """Normalizes embeddings by subtracting the mean embedding.

    If the input array is empty or has no embeddings, it returns the array as is.

    Args:
        embeddings_array (np.ndarray): A NumPy array of embeddings.
            Expected shape is (n_embeddings, embedding_dimension).

    Returns:
        np.ndarray: The normalized NumPy array of embeddings.
    """
    if embeddings_array.size == 0:  
        return embeddings_array
    
    mean_embedding = np.mean(embeddings_array, axis=0)
    normalized_embeddings = embeddings_array - mean_embedding
    return normalized_embeddings 

def find_drop_off_index(values, method='combined', **kwargs): 

    """
    Find the index at which the first significant drop-off occurs in a descending list of values.
    
    Parameters:
    -----------
    values : list
        List of float values sorted in descending order
    method : str, optional
        Method to use for detecting drop-off:
        - 'absolute': Based on absolute difference threshold
        - 'percentage': Based on percentage change threshold
        - 'kneedle': Based on Kneedle algorithm (finds elbow point)
        - 'second_derivative': Based on maximum change in rate of decrease
        - 'combined': A combination of multiple methods (default)
    **kwargs : dict
        Additional parameters specific to each method:
        - abs_threshold: Threshold for absolute method
        - pct_threshold: Threshold for percentage method
    
    Returns:
    --------
    int
        Index of the first significant drop-off
    """
    
    if not values:
        return 0
    
    # Verify the list is in descending order
    for i in range(1, len(values)):
        if values[i-1] < values[i]:
            raise ValueError("Input list must be sorted in descending order")
    
    # Helper functions for different methods
    def _absolute_method(vals, threshold=None):
        """Find drop-off based on absolute difference between consecutive values."""
        if len(vals) < 2:
            return 0
        
        # If threshold is not provided, calculate a dynamic threshold
        if threshold is None:
            # Use a fraction of the range as the threshold
            threshold = (vals[0] - vals[-1]) / (2 * len(vals))
        
        # Find the first index where the drop exceeds the threshold
        for i in range(1, len(vals)):
            if vals[i-1] - vals[i] > threshold:
                return i
        
        # If no significant drop is found, return the last index
        return len(vals) - 1
    
    def _percentage_method(vals, threshold=0.2):
        """Find drop-off based on percentage change between consecutive values."""
        if len(vals) < 2:
            return 0
        
        # Find the first index where the percentage drop exceeds the threshold
        for i in range(1, len(vals)):
            if vals[i-1] <= 0:  # Handle zero or negative values
                continue
            
            percentage_change = (vals[i-1] - vals[i]) / abs(vals[i-1])
            if percentage_change > threshold:
                return i
        
        # If no significant drop is found, return the last index
        return len(vals) - 1
    
    def _kneedle_method(vals):
        """Find drop-off based on the Kneedle algorithm."""
        if len(vals) < 2:
            return 0
        
        # Normalize values to [0,1]
        min_val = min(vals)
        max_val = max(vals)
        if max_val == min_val:
            return 0
        
        norm_values = [(x - min_val) / (max_val - min_val) for x in vals]
        
        # Generate normalized x-coordinates
        n = len(vals)
        x_coords = [i / (n - 1) for i in range(n)]
        
        # Calculate distance from each point to the line connecting the first and last points
        distances = []
        for i in range(n):
            # Line equation: y = -x + 1 (for normalized points (0,1) to (1,0))
            y_on_line = -x_coords[i] + 1
            distance = norm_values[i] - y_on_line
            distances.append(distance)
        
        # Find the index of the maximum distance (the knee point)
        return distances.index(max(distances))
    
    def _second_derivative_method(vals):
        """Find drop-off based on the maximum change in the rate of decrease."""
        if len(vals) < 3:
            return 0
        
        # Calculate all consecutive differences
        diffs = []
        for i in range(1, len(vals)):
            diffs.append(vals[i-1] - vals[i])
        
        # Calculate changes in consecutive differences
        diff_changes = []
        for i in range(1, len(diffs)):
            diff_changes.append(diffs[i] - diffs[i-1])
        
        # Find the index where the change in differences is largest
        max_change_idx = diff_changes.index(max(diff_changes))
        
        # Return the corresponding index in the original list
        # (adding 2 because we need to offset for the differencing operations)
        return max_change_idx + 2
    
    # Execute the selected method
    if method == 'absolute':
        threshold = kwargs.get('abs_threshold', None)
        return _absolute_method(values, threshold)
    
    elif method == 'percentage':
        threshold = kwargs.get('pct_threshold', 0.2)
        return _percentage_method(values, threshold)
    
    elif method == 'kneedle':
        return _kneedle_method(values)
    
    elif method == 'second_derivative':
        return _second_derivative_method(values)
    
    elif method == 'combined':
        # Use a voting mechanism from multiple methods
        results = [
            _absolute_method(values, kwargs.get('abs_threshold', None)),
            _percentage_method(values, kwargs.get('pct_threshold', 0.2)),
            _kneedle_method(values)
        ]
        
        # If list is long enough, also include second derivative method
        if len(values) >= 3:
            results.append(_second_derivative_method(values))
        
        # Count occurrences of each result
        from collections import Counter
        result_counter = Counter(results)
        
        # Return the most common result (if tie, return the smaller index)
        most_common = result_counter.most_common()
        if len(most_common) > 1 and most_common[0][1] == most_common[1][1]:
            # If there's a tie, choose the smaller index
            candidates = [idx for idx, count in most_common if count == most_common[0][1]]
            return min(candidates)
        else:
            # Return the most common result
            return most_common[0][0]
    
    else:
        raise ValueError(f"Unknown method: {method}")